# from torch.utils.cpp_extension import load, CppExtension 
import platform
import sys
import os
import glob
import ctypes
sys.path.append('cxx_builder')
from cxx_builder import cxx_build_options, CxxBuilder

def build_helper():
    if platform.machine() !=  "x86_64":
        return

    cur_dir = os.path.dirname(os.path.abspath(__file__))
    x86_isa_help_builder = CxxBuilder("x86_isa_help", [os.path.join(cur_dir, "csrc", "x86_isa_help.cpp")], cxx_build_options, cur_dir)
    x86_isa_help_builder.build()

    file_ext = x86_isa_help_builder.get_shared_lib_ext()
    libfile = os.path.join(cur_dir, f'x86_isa_help{file_ext}')

    # 1. open the shared library
    isa_help_lib = ctypes.CDLL(libfile)

    # 2. tell Python the argument and result types of function
    isa_help_lib.check_avx2_feature.restype = ctypes.c_bool
    isa_help_lib.check_avx2_feature.argtypes = []

    isa_help_lib.check_avx512_feature.restype = ctypes.c_bool
    isa_help_lib.check_avx512_feature.argtypes = []

    avx2 = isa_help_lib.check_avx2_feature()
    avx512 = isa_help_lib.check_avx512_feature()

    print("!!! x86 isa --> avx2: {}, avx512: {}".format(avx2, avx512))

if __name__=='__main__':
    build_helper()