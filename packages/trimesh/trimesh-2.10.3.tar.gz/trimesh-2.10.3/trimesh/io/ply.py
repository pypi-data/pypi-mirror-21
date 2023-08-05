import numpy as np

from distutils.spawn import find_executable
from collections import OrderedDict
from string import Template

import tempfile
import subprocess

from ..util import is_shape, distance_to_end
from ..resources import get_resource


def load_ply(file_obj, *args, **kwargs):
    '''
    Load a PLY file from an open file object.

    Parameters
    ---------
    file_obj: an open file- like object

    Returns
    ---------
    mesh_kwargs: dictionary of mesh info which can be passed to
                 Trimesh constructor, eg: a = Trimesh(**mesh_kwargs)
    '''

    # OrderedDict which is populated from the header
    elements, is_ascii = read_ply_header(file_obj)

    # functions will fill in elements from file_obj
    if is_ascii:
        ply_ascii(elements, file_obj)
    else:
        ply_binary(elements, file_obj)

    kwargs = elements_to_kwargs(elements)
    return kwargs


def export_ply(mesh):
    '''
    Export a mesh in the PLY format.

    Parameters
    ----------
    mesh: Trimesh object

    Returns
    ----------
    export: bytes of result
    '''
    dtype_face = np.dtype([('count', '<u1'),
                           ('index', '<i4', (3))])
    dtype_vertex = np.dtype([('vertex', '<f4', (3))])

    faces = np.zeros(len(mesh.faces), dtype=dtype_face)
    faces['count'] = 3
    faces['index'] = mesh.faces

    vertex = np.zeros(len(mesh.vertices), dtype=dtype_vertex)
    vertex['vertex'] = mesh.vertices

    template = Template(get_resource('ply.template'))
    export = template.substitute({'vertex_count': len(mesh.vertices),
                                  'face_count': len(mesh.faces)}).encode('utf-8')
    export += vertex.tostring()
    export += faces.tostring()
    return export


def read_ply_header(file_obj):
    '''
    Read the ASCII header of a PLY file, and leave the file object
    at the position of the start of data but past the data.
    '''
    # from ply specification, and additional dtypes found in the wild
    dtypes = {'char': 'i1',
              'uchar': 'u1',
              'short': 'i2',
              'ushort': 'u2',
              'int': 'i4',
              'int16': 'i2',
              'int32': 'i4',
              'uint': 'u4',
              'uint16': 'u2',
              'uint32': 'u4',
              'float': 'f4',
              'float16': 'f2',
              'float32': 'f4',
              'double': 'f8'}

    if 'ply' not in str(file_obj.readline()):
        raise ValueError('This aint a ply file')

    encoding = file_obj.readline().decode('utf-8').strip().lower()
    encoding_ascii = 'ascii' in encoding

    endian = ['<', '>'][int('big' in encoding)]
    elements = OrderedDict()

    while True:
        line = file_obj.readline()
        if line is None:
            raise ValueError('Header wasn\'t terminated properly!')
        line = line.decode('utf-8').strip().split()

        if 'end_header' in line:
            break

        if 'element' in line[0]:
            name, length = line[1:]
            elements[name] = {'length': int(length),
                              'properties': OrderedDict()}
        elif 'property' in line[0]:
            if len(line) == 3:
                dtype, field = line[1:]
                elements[name]['properties'][
                    str(field)] = endian + dtypes[dtype]
            elif 'list' in line[1]:
                dtype_count, dtype, field = line[2:]
                elements[name]['properties'][str(field)] = (endian +
                                                            dtypes[dtype_count] +
                                                            ', ($LIST,)' +
                                                            endian +
                                                            dtypes[dtype])
    return elements, encoding_ascii


def elements_to_kwargs(elements):
    '''
    Given an elements data structure, extract the keyword
    arguments that a Trimesh object constructor will expect.
    '''
    vertices = np.column_stack([elements['vertex']['data'][i] for i in 'xyz'])
    if not is_shape(vertices, (-1, 3)):
        raise ValueError('Vertices were not (n,3)!')

    if is_shape(elements['face']['data'], (-1, (3, 4))):
        faces = elements['face']['data']
    else:
        blob = elements['face']['data']
        # some exporters set this name to 'vertex_index'
        # and some others use 'vertex_indices', but we really
        # don't care about the name unless there are multiple properties
        # defined
        if len(blob.dtype.names) == 1:
            name = blob.dtype.names[0]
        elif len(blob.dtype.names) > 1:
            for i in blob.dtype.names:
                if i in ['vertex_index',
                         'vertex_indices']:
                    name = i
                    break
        faces = elements['face']['data'][name]['f1']

    if not is_shape(faces, (-1, (3, 4))):
        raise ValueError('Faces weren\'t (n,(3|4))!')

    result = {'vertices': vertices,
              'faces': faces,
              'ply_data': elements}

    # if both vertex and face color are defined, pick the one
    # with the most going on
    f_color, f_signal = element_colors(elements['face'])
    v_color, v_signal = element_colors(elements['vertex'])
    colors = [{'face_colors': f_color},
              {'vertex_colors': v_color}]
    colors_index = np.argmax([f_signal,
                              v_signal])
    result.update(colors[colors_index])

    return result


def element_colors(element):
    '''
    Given an element, try to extract RGBA color from its properties
    and return them as an (n,3|4) array.

    Parameters
    -------------
    element: dict, containing color keys

    Returns
    ------------
    colors: (n,(3|4) 
    signal: float, estimate of range
    '''
    keys = ['red', 'green', 'blue', 'alpha']
    candidate_colors = [element['data'][i]
                        for i in keys if i in element['properties']]

    if len(candidate_colors) >= 3:
        colors = np.column_stack(candidate_colors)
        signal = colors.ptp(axis=0).sum()
        return colors, signal

    return None, 0.0


def ply_ascii(elements, file_obj):
    '''
    Load data from an ASCII PLY file into the elements data structure.
    '''
    # list of strings, split by newlines and spaces
    blob = file_obj.read().decode('utf-8')
    # numpy array with string type
    raw = np.array(blob.split())
    position = 0

    for key, values in elements.items():
        dtype_str = list(values['properties'].values())[0]
        if '$LIST' in dtype_str:
            # the first row is the number of data points following
            rows = int(raw[position]) + 1
            count = values['length'] * rows
            # for index types the dtype_str contains the dtype of the count followed
            # by the dtype of the values that follow
            dtype = np.dtype(dtype_str.split('($LIST,)')[-1])
            data = raw[position:position +
                       count].reshape((-1, rows)).astype(dtype)[:, 1:]
            elements[key]['data'] = data
        else:
            rows = len(values['properties'])
            count = values['length'] * rows
            data = raw[position:position +
                       count].reshape((-1, rows)).astype(dtype_str)
            elements[key]['data'] = {p: c for p, c in zip(
                values['properties'].keys(), data.T)}
        position += count

    if position != len(raw):
        raise ValueError('File was unexpected length!')


def ply_binary(elements, file_obj):
    '''
    Load the data from a binary PLY file into the elements data structure.
    '''

    def populate_listsize(file_obj, elements):
        '''
        Given a set of elements populated from the header if there are any
        list properties seek in the file the length of the list.

        Note that if you have a list where each instance is different length
        (if for example you mixed triangles and quads) this won't work at all
        '''
        p_start = file_obj.tell()
        p_current = file_obj.tell()
        for element_key, element in elements.items():
            props = element['properties']
            prior_data = ''
            for k, dtype in props.items():
                if '$LIST' in dtype:
                    # every list field has two data types:
                    # the list length (single value), and the list data (multiple)
                    # here we are only reading the single value for list length
                    field_dtype = np.dtype(dtype.split(',')[0])
                    if len(prior_data) == 0:
                        offset = 0
                    else:
                        offset = np.dtype(prior_data).itemsize()
                    file_obj.seek(p_current + offset)
                    size = np.fromstring(file_obj.read(field_dtype.itemsize),
                                         dtype=field_dtype)[0]
                    props[k] = props[k].replace('$LIST', str(size))
                prior_data += props[k] + ','
            itemsize = np.dtype(', '.join(props.values())).itemsize
            p_current += element['length'] * itemsize
        file_obj.seek(p_start)

    def populate_data(file_obj, elements):
        '''
        Given the data type and field information from the header,
        read the data and add it to a 'data' field in the element.
        '''
        for key in elements.keys():
            items = list(elements[key]['properties'].items())
            dtype = np.dtype(items)
            data = file_obj.read(elements[key]['length'] * dtype.itemsize)
            elements[key]['data'] = np.fromstring(data, dtype=dtype)
        return elements

    def elements_size(elements):
        '''
        Given an elements data structure populated from the header,
        calculate how long the file should be if it is intact.
        '''
        size = 0
        for element in elements.values():
            dtype = np.dtype(','.join(element['properties'].values()))
            size += element['length'] * dtype.itemsize
        return size

    # some elements are passed where the list dimensions
    # are not included in the header, so this function goes
    # into the meat of the file and grabs the list dimensions
    # before we to the main data read as a single operation
    populate_listsize(file_obj, elements)

    # how many bytes are left in the file
    size_file = distance_to_end(file_obj)
    # how many bytes should the data structure described by
    # the header take up
    size_elements = elements_size(elements)

    # if the number of bytes is not the same the file is probably corrupt
    if size_file != size_elements:
        raise ValueError('File is unexpected length!')

    # with everything populated and a reasonable confidence the file
    # is intact, read the data fields described by the header
    populate_data(file_obj, elements)


def export_draco(mesh):
    '''
    Export a mesh using Google's Draco compressed format.

    Only works if draco_encoder is in your PATH:
    https://github.com/google/draco

    Parameters
    ----------
    mesh: Trimesh object

    Returns
    ----------
    data: str or bytes, data
    '''
    with tempfile.NamedTemporaryFile(suffix='.ply') as temp_ply:
        temp_ply.write(export_ply(mesh))
        temp_ply.flush()
        with tempfile.NamedTemporaryFile(suffix='.drc') as encoded:
            subprocess.check_output([draco_encoder,
                                     '-i',
                                     temp_ply.name,
                                     '-o',
                                     encoded.name])
            encoded.seek(0)
            data = encoded.read()
    return data


def load_draco(file_obj, file_type=None):
    '''
    Load a mesh from Google's Draco format.

    Parameters
    ----------
    file_obj: open file- like object
    file_type: unused

    Returns
    ----------
    kwargs: dict, kwargs to construct a Trimesh object
    '''

    with tempfile.NamedTemporaryFile(suffix='.drc') as temp_drc:
        temp_drc.write(file_obj.read())
        temp_drc.flush()

        with tempfile.NamedTemporaryFile(suffix='.ply') as temp_ply:
            subprocess.check_output([draco_decoder,
                                     '-i',
                                     temp_drc.name,
                                     '-o',
                                     temp_ply.name])
            temp_ply.seek(0)
            kwargs = load_ply(temp_ply)
    return kwargs


_ply_loaders = {'ply': load_ply}
_ply_exporters = {'ply': export_ply}

draco_encoder = find_executable('draco_encoder')
draco_decoder = find_executable('draco_decoder')

if draco_decoder is not None:
    _ply_loaders['drc'] = load_draco
if draco_encoder is not None:
    _ply_exporters['drc'] = export_draco
