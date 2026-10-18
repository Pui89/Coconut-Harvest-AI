"""Check whether this Windows/Python environment can run the free rule-based agent.

This check does not install packages, download models, or contact a paid service.
"""
from __future__ import print_function

import os
import platform
import shutil
import sys


def available_ram_gb():
    if os.name != "nt":
        return None
    try:
        import ctypes

        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        status = MEMORYSTATUSEX()
        status.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
            return status.ullAvailPhys / (1024.0 ** 3)
    except Exception:
        pass
    return None


def main():
    print("=" * 60)
    print("Coconut Harvest AI — free local agent readiness check")
    print("=" * 60)
    print("Operating system : {0}".format(platform.platform()))
    print("Python version   : {0}".format(platform.python_version()))
    print("Python executable: {0}".format(sys.executable))

    ram = available_ram_gb()
    if ram is not None:
        print("Available RAM    : {0:.1f} GB".format(ram))
    else:
        print("Available RAM    : unable to read automatically")

    try:
        disk = shutil.disk_usage(os.getcwd())
        print("Free disk space  : {0:.1f} GB".format(disk.free / (1024.0 ** 3)))
    except Exception:
        print("Free disk space  : unable to read automatically")

    print("\nOptional packages (not required for the rule-based agent):")
    for package in ("torch", "transformers", "ultralytics", "smolagents"):
        try:
            module = __import__(package)
            version = getattr(module, "__version__", "installed; version unknown")
            print("  {0}: {1}".format(package, version))
        except Exception:
            print("  {0}: not installed".format(package))

    print("\nRecommendation:")
    if sys.version_info < (3, 10):
        print("  Install Python 3.10 or newer to run the agent in this repository.")
        print("  Python downloads are free: https://www.python.org/downloads/windows/")
        return 1

    print("  Your Python version is suitable for the lightweight rule-based agent.")
    print("  Run: python agents\\harvest_planning_agent.py")
    print("  No model download or extra package installation is needed.")
    print("\nThis check does not benchmark GPU performance or guarantee that large models fit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
