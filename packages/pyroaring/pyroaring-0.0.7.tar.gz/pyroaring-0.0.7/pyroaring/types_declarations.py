import ctypes
import platform
import sys
is_python2 = sys.version_info < (3, 0)

libfilename = "libroaring.so"
if(platform.uname()[0] == "Darwin") :
    libfilename = "libroaring.dylib"
from .__main__ import syntax_msg

try:
    libroaring = ctypes.cdll.LoadLibrary(libfilename)
except OSError as e:
    if 'install' not in sys.argv and 'uninstall' not in sys.argv: # dirty, but there is no universal way to detect if pyroaring is ran as a script or is imported...
        sys.stderr.write('ERROR: cannot open shared library %s\n' % libfilename)
        sys.stderr.write('       Please make sure that the library can be found.\n')
        sys.stderr.write('       For instance, on GNU/Linux, it could be in /usr/lib and /usr/include directories,\n')
        sys.stderr.write('       or in some other directory with the environment variable LD_LIBRARY_PATH correctly set.\n')
        sys.stderr.write('       You can install it by runing %s\n' % syntax_msg)
        sys.exit(1)
    else:
        libroaring = None

bm_type = ctypes.c_void_p
val_type = ctypes.c_uint32

class BitMapStats(ctypes.Structure):
    _fields_ = [
        ('n_containers', val_type),
        ('n_array_containers', val_type),
        ('n_run_containers', val_type),
        ('n_bitset_containers', val_type),
        ('n_values_array_containers', val_type),
        ('n_values_run_containers', val_type),
        ('n_values_bitset_containers', val_type),
        ('n_bytes_array_containers', val_type),
        ('n_bytes_run_containers', val_type),
        ('n_bytes_bitset_containers', val_type),
        ('max_value', val_type),
        ('min_value', val_type),
        ('sum_value', ctypes.c_uint64),
        ('cardinality', ctypes.c_uint64)
    ]

    def to_dict(self):
        result = dict()
        for field in self._fields_:
            key = field[0]
            result[key] = self.__getattribute__(key)
        return result

    def __repr__(self):
        return repr(self.to_dict())

if libroaring is not None:
    libroaring.roaring_bitmap_create.restype = bm_type
    libroaring.roaring_bitmap_create.argtypes = []
    libroaring.roaring_bitmap_copy.restype = bm_type
    libroaring.roaring_bitmap_copy.argtypes = [bm_type]
    libroaring.roaring_bitmap_from_range.restype = bm_type
    libroaring.roaring_bitmap_from_range.argtypes = [val_type, val_type, val_type]
    libroaring.roaring_bitmap_add_many.restype = None
    libroaring.roaring_bitmap_add_many.argtypes = [bm_type, ctypes.c_size_t, ctypes.POINTER(val_type)]
    libroaring.roaring_bitmap_of_ptr.restype = bm_type
    libroaring.roaring_bitmap_of_ptr.argtypes = [ctypes.c_size_t, ctypes.POINTER(val_type)]
    libroaring.roaring_bitmap_run_optimize.restype = ctypes.c_bool
    libroaring.roaring_bitmap_run_optimize.argtypes = [bm_type]
    libroaring.roaring_bitmap_free.restype = None
    libroaring.roaring_bitmap_free.argtypes = [bm_type]
    libroaring.roaring_bitmap_add.restype = None
    libroaring.roaring_bitmap_add.argtypes = [bm_type, val_type]
    libroaring.roaring_bitmap_remove.restype = None
    libroaring.roaring_bitmap_remove.argtypes = [bm_type, val_type]
    libroaring.roaring_bitmap_contains.restype = ctypes.c_bool
    libroaring.roaring_bitmap_contains.argtypes = [bm_type, val_type]
    libroaring.roaring_bitmap_get_cardinality.restype = ctypes.c_size_t
    libroaring.roaring_bitmap_get_cardinality.argtypes = [bm_type]
    libroaring.roaring_bitmap_equals.restype = ctypes.c_bool
    libroaring.roaring_bitmap_equals.argtypes = [bm_type, bm_type]
    libroaring.roaring_bitmap_is_subset.restype = ctypes.c_bool
    libroaring.roaring_bitmap_is_subset.argtypes = [bm_type, bm_type]
    libroaring.roaring_bitmap_is_strict_subset.restype = ctypes.c_bool
    libroaring.roaring_bitmap_is_strict_subset.argtypes = [bm_type, bm_type]
    libroaring.roaring_bitmap_to_uint32_array.restype = ctypes.POINTER(val_type)
    libroaring.roaring_bitmap_to_uint32_array.argtypes = [bm_type]
    libroaring.roaring_bitmap_or.restype = bm_type
    libroaring.roaring_bitmap_or.argtypes = [bm_type, bm_type]
    libroaring.roaring_bitmap_and.restype = bm_type
    libroaring.roaring_bitmap_and.argtypes = [bm_type, bm_type]
    libroaring.roaring_bitmap_xor.restype = bm_type
    libroaring.roaring_bitmap_xor.argtypes = [bm_type, bm_type]
    libroaring.roaring_bitmap_andnot.restype = bm_type
    libroaring.roaring_bitmap_andnot.argtypes = [bm_type, bm_type]
    libroaring.roaring_bitmap_or_inplace.restype = None
    libroaring.roaring_bitmap_or_inplace.argtypes = [bm_type, bm_type]
    libroaring.roaring_bitmap_and_inplace.restype = None
    libroaring.roaring_bitmap_and_inplace.argtypes = [bm_type, bm_type]
    libroaring.roaring_bitmap_xor_inplace.restype = None
    libroaring.roaring_bitmap_xor_inplace.argtypes = [bm_type, bm_type]
    libroaring.roaring_bitmap_andnot_inplace.restype = None
    libroaring.roaring_bitmap_andnot_inplace.argtypes = [bm_type, bm_type]
    libroaring.roaring_bitmap_select.restype = ctypes.c_bool
    libroaring.roaring_bitmap_select.argtypes = [bm_type, val_type, ctypes.POINTER(val_type)]
    libroaring.roaring_bitmap_or_many.restype = bm_type
    libroaring.roaring_bitmap_or_many.argtypes = [ctypes.c_size_t, ctypes.POINTER(bm_type)]
    libroaring.roaring_bitmap_portable_serialize.restype = ctypes.c_size_t
    libroaring.roaring_bitmap_portable_serialize.argtypes = [bm_type, ctypes.POINTER(ctypes.c_char)]
    libroaring.roaring_bitmap_portable_deserialize.restype = bm_type
    libroaring.roaring_bitmap_portable_deserialize.argtypes = [ctypes.c_char_p]
    libroaring.roaring_bitmap_portable_size_in_bytes.restype = ctypes.c_size_t
    libroaring.roaring_bitmap_portable_size_in_bytes.argtypes = [bm_type]
    libroaring.roaring_bitmap_statistics.restype = None
    libroaring.roaring_bitmap_statistics.argtypes = [bm_type, ctypes.POINTER(BitMapStats)]
    libroaring.roaring_bitmap_flip.restype = bm_type
    libroaring.roaring_bitmap_flip.argtypes = [bm_type, ctypes.c_uint64, ctypes.c_uint64]
    libroaring.roaring_bitmap_flip_inplace.restype = None
    libroaring.roaring_bitmap_flip_inplace.argtypes = [bm_type, ctypes.c_uint64, ctypes.c_uint64]
    libroaring.roaring_bitmap_minimum.restype = val_type
    libroaring.roaring_bitmap_minimum.argtypes = [bm_type]
    libroaring.roaring_bitmap_maximum.restype = val_type
    libroaring.roaring_bitmap_maximum.argtypes = [bm_type]
    libroaring.roaring_bitmap_rank.restype = val_type
    libroaring.roaring_bitmap_rank.argtypes = [bm_type, val_type]
    libroaring.roaring_bitmap_intersect.restype = ctypes.c_bool
    libroaring.roaring_bitmap_intersect.argtypes = [bm_type, bm_type]
    libroaring.roaring_bitmap_or_cardinality.restype = ctypes.c_uint64
    libroaring.roaring_bitmap_or_cardinality.argtypes = [bm_type, bm_type]
    libroaring.roaring_bitmap_and_cardinality.restype = ctypes.c_uint64
    libroaring.roaring_bitmap_and_cardinality.argtypes = [bm_type, bm_type]
    libroaring.roaring_bitmap_andnot_cardinality.restype = ctypes.c_uint64
    libroaring.roaring_bitmap_andnot_cardinality.argtypes = [bm_type, bm_type]
    libroaring.roaring_bitmap_xor_cardinality.restype = ctypes.c_uint64
    libroaring.roaring_bitmap_xor_cardinality.argtypes = [bm_type, bm_type]
    libroaring.roaring_bitmap_jaccard_index.restype = ctypes.c_double
    libroaring.roaring_bitmap_jaccard_index.argtypes = [bm_type, bm_type]
