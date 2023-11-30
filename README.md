# x86_isa_help

This project is a demo to show how to write a cpp code read cpuid to check x86 ISAs.

Current code is works use pytorch cpp_extension load build code, and use pybuild11 bind api. This solution can proof it works but still some issues:
> 1. cpp_extension load is depends on ninja.
> 2. cpp_extension is include all python and torch dependencies, so it is build very slow.
> 3. pybuild11 is also make build slow, use ctypes to replace it seems a better api binder.
