# from torch.utils.cpp_extension import load, CppExtension 
import platform
import sys
import os
import ctypes
sys.path.append('cxx_builder')
from cxx_builder import cxx_build_options, CxxBuilder

def x86_isa_checker() -> list:
    supported_isa = []
    def _check_and_append_supported_isa(dest: list, isa: bool, isa_name: str):
        if isa is True:
            dest.append(isa_name)

    Arch = platform.machine()
    '''
    Arch value is x86_64 on Linux, and the value is AMD64 on Windows.
    '''
    if Arch !=  "x86_64" and Arch != "AMD64":
        return supported_isa

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

    # 3. call cpp backend and get result
    avx2 = isa_help_lib.check_avx2_feature()
    avx512 = isa_help_lib.check_avx512_feature()

    _check_and_append_supported_isa(supported_isa, avx2, "avx2")
    _check_and_append_supported_isa(supported_isa, avx512, "avx512")

    print("!!! x86 isa --> avx2: {}, avx512: {}".format(avx2, avx512))

    return supported_isa

if __name__=='__main__':
    x86_isa = x86_isa_checker()
    # print(x86_isa)