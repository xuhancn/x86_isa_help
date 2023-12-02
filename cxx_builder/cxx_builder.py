import sys
from typing import Dict, List

# initialize variables for compilation
_IS_LINUX = sys.platform.startswith('linux')
_IS_MACOS = sys.platform.startswith('darwin')
_IS_WINDOWS = sys.platform == 'win32'

def _nonduplicate_append(dest_list: list, src_list: list):
    for i in src_list:
        if not i in dest_list:
            dest_list.append(i)

class BuildOptionsBase(object):
    _definations = []
    _include_dirs = []
    _cflags = []
    _ldlags = []
    _libraries_dirs = []
    _libraries = []
    _passthough_parameters = []

    def __init__(self) -> None:
        pass

    def get_definations(self) -> List[str]:
        return self._definations
    
    def get_include_dirs(self) -> List[str]:
        return self._include_dirs

    def get_cflags(self) -> List[str]:
        return self._cflags
    
    def get_ldlags(self) -> List[str]:
        return self._ldlags
    
    def get_libraries_dirs(self) -> List[str]:
        return self.get_libraries_dirs
    
    def get_libraries(self) -> List[str]:
        return self.get_libraries
    
    def get_passthough_parameters(self) -> List[str]:
        return self.get_passthough_parameters

class CxxOptions(BuildOptionsBase):
    def __init__(self) -> None:
        super().__init__()
        _nonduplicate_append(self._cflags, ["O3", "NDEBUG"])
    
class CxxTorchOptions(CxxOptions):
    def __init__(self) -> None:
        super().__init__()
        _nonduplicate_append(self._cflags, ["DTORCH"])
    
class CxxCudaOptions(CxxTorchOptions):
    def __init__(self) -> None:
        super().__init__()
        _nonduplicate_append(self._cflags, ["DCUDA"])

cxx_cfg = CxxOptions()
print(cxx_cfg.get_cflags())

cpu_cfg = CxxTorchOptions()
print(cpu_cfg.get_cflags())

cuda_cfg = CxxCudaOptions()
print(cuda_cfg.get_cflags())