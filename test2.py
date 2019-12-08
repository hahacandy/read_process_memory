import ctypes
from ctypes import *
from ctypes.wintypes import *

import psutil


def getpid():
    #  ex) nameprocess = "notepad.exe"
    nameprocess = ""
    for proc in psutil.process_iter():
        if nameprocess in str(proc.name):

            return proc.pid


def read_process_memory(_PROCESS_HEADER_ADDR, _PROCESS_ID):
    PROCESS_VM_READ = 0x0010
    k32 = WinDLL('kernel32')
    k32.OpenProcess.argtypes = DWORD, BOOL, DWORD
    k32.OpenProcess.restype = HANDLE
    k32.ReadProcessMemory.argtypes = HANDLE, LPVOID, LPVOID, c_size_t, POINTER(c_size_t)
    k32.ReadProcessMemory.restype = BOOL
    process = k32.OpenProcess(PROCESS_VM_READ, 0, _PROCESS_ID)
    result = create_string_buffer(4)
    bytes_read = c_size_t()
    if k32.ReadProcessMemory(process, _PROCESS_HEADER_ADDR, result, 4, ctypes.byref(bytes_read)):
        result2 = 0
        result2 += result.raw[0] << 8 * 0
        result2 += result.raw[1] << 8 * 1
        result2 += result.raw[2] << 8 * 2
        result2 += result.raw[3] << 8 * 3
        return result2
    else:
        return -1


# ex) print(read_process_memory(0x00000000, getpid()))