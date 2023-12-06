# from torch.utils.cpp_extension import load, CppExtension 
import platform
import sys
import os
import ctypes
sys.path.append('cxx_builder')
from cxx_builder import cxx_build_options, CxxBuilder

def x86_isa_checker():
    Arch = platform.machine()
    '''
    Arch value is x86_64 on Linux, and the value is AMD64 on Windows.
    '''
    if Arch !=  "x86_64" and Arch != "AMD64":
        return

    cur_dir = os.path.dirname(os.path.abspath(__file__))
    x86_isa_help_builder = CxxBuilder("x86_isa_help", [os.path.join(cur_dir, "csrc", "x86_isa_help.cpp")], cxx_build_options, cur_dir)
    status, target_file = x86_isa_help_builder.build()

    # 1. open the shared library
    isa_help_lib = ctypes.CDLL(target_file)

    # 2. tell Python the argument and result types of function
    isa_help_lib.check_avx2_feature.restype = ctypes.c_bool
    isa_help_lib.check_avx2_feature.argtypes = []

    isa_help_lib.check_avx512_feature.restype = ctypes.c_bool
    isa_help_lib.check_avx512_feature.argtypes = []

    avx2 = isa_help_lib.check_avx2_feature()
    avx512 = isa_help_lib.check_avx512_feature()

    print("!!! x86 isa --> avx2: {}, avx512: {}".format(avx2, avx512))

if __name__=='__main__':
    x86_isa_checker()