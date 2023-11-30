from torch.utils.cpp_extension import load, CppExtension 
import platform

def build_helper():
    if platform.machine() !=  "x86_64":
        return

    module = load(
        name="x86_isa_help",
        sources=["csrc/x86_isa_help.cpp"],
        extra_cflags=["-O2"],
        verbose=True,
    )

    import x86_isa_help
    avx2 = x86_isa_help.check_avx2_feature()
    avx512 = x86_isa_help.check_avx512_feature()

    print("!!! x86 isa --> avx2: {}, avx512: {}".format(avx2, avx512))

if __name__=='__main__':
    build_helper()