import sys
from typing import Dict, List
import os

# initialize variables for compilation
_IS_LINUX = sys.platform.startswith('linux')
_IS_MACOS = sys.platform.startswith('darwin')
_IS_WINDOWS = sys.platform == 'win32'

def _get_cxx_compiler():
    if _IS_WINDOWS:
        compiler = os.environ.get('CXX', 'cl')
    else:
        compiler = os.environ.get('CXX', 'c++')
    return compiler

def _nonduplicate_append(dest_list: list, src_list: list):
    for i in src_list:
        if not i in dest_list:
            dest_list.append(i)

class BuildOptionsBase(object):
    _compiler = ""
    _definations = []
    _include_dirs = []
    _cflags = []
    _ldlags = []
    _libraries_dirs = []
    _libraries = []
    _passthough_args = []

    def __init__(self) -> None:
        pass

    def get_compiler(self) -> str:
        return self._compiler

    def get_definations(self) -> List[str]:
        return self._definations
    
    def get_include_dirs(self) -> List[str]:
        return self._include_dirs

    def get_cflags(self) -> List[str]:
        return self._cflags
    
    def get_ldlags(self) -> List[str]:
        return self._ldlags
    
    def get_libraries_dirs(self) -> List[str]:
        return self._libraries_dirs
    
    def get_libraries(self) -> List[str]:
        return self._libraries
    
    def get_passthough_args(self) -> List[str]:
        return self._passthough_args

class CxxOptions(BuildOptionsBase):
    def __init__(self) -> None:
        super().__init__()
        self._compiler = _get_cxx_compiler()
        _nonduplicate_append(self._cflags, ["O3", "NDEBUG"])
    
class CxxTorchOptions(CxxOptions):
    def __init__(self) -> None:
        super().__init__()
        _nonduplicate_append(self._cflags, ["DTORCH"])
    
class CxxCudaOptions(CxxTorchOptions):
    def __init__(self) -> None:
        super().__init__()
        _nonduplicate_append(self._cflags, ["DCUDA"])

class CxxBuilder():
    _compiler = ""
    _cflags_args = ""
    _definations_args = ""
    _include_dirs_args = ""
    _ldlags_args = ""
    _libraries_dirs_args = ""
    _libraries_args = ""
    _passthough_parameters_args = ""

    _name = ""
    _sources_args = ""

    def __init__(self, name, sources, BuildOption: BuildOptionsBase) -> None:
        self._name = name
        self._sources_args = " ".join(sources)

        self._compiler = BuildOption.get_compiler()

        for cflag in BuildOption.get_cflags():
            if _IS_WINDOWS:
                self._cflags_args += (f"/{cflag} ")
            else:
                self._cflags_args += (f"-{cflag} ")

        for defination in BuildOption.get_definations():
            if _IS_WINDOWS:
                self._definations_args +=  (f"/D {defination} ")
            else:
                self._definations_args +=  (f"-D{defination} ")

        for inc_dir in BuildOption.get_include_dirs():
            if _IS_WINDOWS:
                self._include_dirs_args += (f"/I {inc_dir} ")
            else:
                self._include_dirs_args += (f"-I{inc_dir} ")
        
        for ldflag in BuildOption.get_ldlags():
            if _IS_WINDOWS:
                self._ldlags_args += (f"/{ldflag} ")
            else:    
                self._ldlags_args += (f"-{ldflag} ")
        
        for lib_dir in BuildOption.get_libraries_dirs():
            if _IS_WINDOWS:
                self._libraries_dirs_args += (f"/LIBPATH:{lib_dir} ")
            else:
                self._libraries_dirs_args += (f"-L{lib_dir} ")

        for lib in BuildOption.get_libraries():
            if _IS_WINDOWS:
                self._libraries_args += (f"{lib}.lib ")
            else:
                self._libraries_args += (f"-l{lib} ")

        for passthough_arg in BuildOption.get_passthough_args():
            self._passthough_parameters_args += (f"{passthough_arg}")

    def get_command_line(self) -> str:
        return ""
    
    def build(self):
        build_cmd = self.get_command_line()
        return


cxx_cfg = CxxOptions()
cpu_cfg = CxxTorchOptions()
cuda_cfg = CxxCudaOptions()

builder = CxxBuilder("x86_isa_help", ["../csrc/x86_isa_help.cpp"], cxx_cfg)
builder.build()