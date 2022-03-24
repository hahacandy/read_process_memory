import ctypes
from ctypes import *
from ctypes.wintypes import *

import psutil

from mem_edit import Process

def getpid(nameprocess):

    for proc in psutil.process_iter():
        if nameprocess in str(proc.name):

            return proc.pid

def read_process_memory(_address, _pid):
    with Process.open_process(pid) as p:
        num_ulong = p.read_memory(_address, ctypes.c_ulong())
        return num_ulong
    return None

def write_memory(_address, _value, _pid):
    with Process.open_process(pid) as p:
        p.write_memory(_address, ctypes.c_ulong(_value))

def search_memory(pid):
    with Process.open_process(pid) as p:
        addrs = None
        while True:
            value = input('검색 값 입력:')
            
            if value == '':
                print('검색 종료')
                break
                
            value = int(value)
                
            if addrs == None:
                addrs = p.search_all_memory(ctypes.c_int(value))
            else:
                addrs = p.search_addresses(addrs, ctypes.c_int(value))
                
            print('검색 된 개수:' + str(len(addrs)))
            
            if len(addrs) <= 100:
                for idx, addr in enumerate(addrs):
                    print(idx, hex(addr))
                    
                if len(addrs) == 1 or len(addrs) == 0:
                    print('검색 종료')
                    break


pid = getpid('피카츄배구.exe')

search_memory(pid)

# 메모리 주소에 해당하는 값이 무엇인지
print(read_process_memory(0x2313c94, pid))

# 메모리 주소에 값을 적용
write_memory(0x2313c94, 1, pid)