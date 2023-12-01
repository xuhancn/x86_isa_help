

class CxxOptionsBase(object):
    def __init__(self) -> None:
        pass

    def get_cflags(self):
        return ["O2", "NDEBUG"]
    
class CxxTorchOptions(CxxOptionsBase):
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

cxx_cfg = CxxOptionsBase()
print(cxx_cfg.get_cflags())

cpu_cfg = CxxTorchOptions()
print(cpu_cfg.get_cflags())

cuda_cfg = CxxCudaOptions()
print(cuda_cfg.get_cflags())