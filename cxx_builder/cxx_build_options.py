import sys

# initialize variables for compilation
_IS_LINUX = sys.platform.startswith('linux')
_IS_MACOS = sys.platform.startswith('darwin')
_IS_WINDOWS = sys.platform == 'win32'

class BuildOptionsBase(object):
    def __init__(self) -> None:
        pass

    def get_definations(self):
        raise NotImplementedError()
    
    def get_include_dirs(self):
        raise NotImplementedError()    

    def get_cflags(self):
        raise NotImplementedError()
    
    def get_ldlags(self):
        raise NotImplementedError()
    
    def get_libraries_dirs(self):
        raise NotImplementedError()
    
    def get_libraries(self):
        raise NotImplementedError()
    
    def get_passthough_parameters(self):
        raise NotImplementedError()

class CxxOptions(BuildOptionsBase):
    def __init__(self) -> None:
        super().__init__()

    def get_cflags(self):
        return ["O2", "NDEBUG"]
    
class CxxTorchOptions(CxxOptions):
    def __init__(self) -> None:
        super().__init__()

    def get_cflags(self):
        cflags = super().get_cflags()
        cflags.append("DTORCH")
        return cflags
    
class CxxCudaOptions(CxxTorchOptions):
    def __init__(self) -> None:
        super().__init__()

    def get_cflags(self):
        cflags = super().get_cflags()
        cflags.append("DCUDA")
        return cflags

cxx_cfg = CxxOptions()
print(cxx_cfg.get_cflags())

cpu_cfg = CxxTorchOptions()
print(cpu_cfg.get_cflags())

cuda_cfg = CxxCudaOptions()
print(cuda_cfg.get_cflags())