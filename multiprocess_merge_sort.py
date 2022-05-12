import chunk
from functools import partial
from timeit import timeit
import numpy as np
from sys import getsizeof
from helper import loadTestFile
import os
import multiprocessing as mp
import multiprocessing.managers as mpm
import multiprocessing.shared_memory as shm
import ctypes as ct
import time

SHARED_STRING_NAME= 'shm_string'
SHARED_ARRAY_NAME = 'shm_array'

class SharedMemoryManager():
    def __init__(self, inputFile):
        self.inputFile = inputFile

    def construct(self):
        b = bytes(loadTestFile(self.inputFile), 'utf-8')
        self.inputSize = len(b)
        self.shmString = shm.SharedMemory(name=SHARED_STRING_NAME, create=True, size=len(b))
        for i in range(0, len(b)):
            self.shmString.buf[i] = b[i]
        self.shmArray = shm.SharedMemory(name=SHARED_ARRAY_NAME, create=True, size = len(b) * 8)

    def deconstruct(self):
        self.shmString.close()
        self.shmString.unlink()
        self.shmArray.close()
        self.shmArray.unlink()

def _multiprocessFill(start, end, size):
    shmArray = shm.SharedMemory(name=SHARED_ARRAY_NAME, create=False)
    b = np.ndarray((size, ), dtype=np.int64, buffer=shmArray.buf)
    for i in range(start, end):
       b[i] = i
    shmArray.close()

def multiprocessFill(size):
    numProcess = mp.cpu_count()
    processes = []
    chunkSize = size // numProcess
    for i in range(0, numProcess):
        processes.append(mp.Process(target=_multiprocessFill, args=(i * chunkSize, min((i + 1) * chunkSize, size), size)))
    for i in range(0, numProcess):
        processes[i].start()
    for i in range(0, numProcess):
        processes[i].join()

def merge(arr, string, start, mid, end):
    start2 = mid + 1
 
    # If the direct merge is already sorted
    if inplaceRotationsCompare(arr[start], arr[start2], string) < 0:
        return
 
    # Two pointers to maintain start
    # of both arrays to merge
    while (start <= mid and start2 <= end):
 
        # If element 1 is in right place
        if inplaceRotationsCompare(arr[start], arr[start2], string) < 0:
            start += 1
        else:
            value = arr[start2]
            index = start2
 
            # Shift all the elements between element 1
            # element 2, right by 1.
            while (index != start):
                arr[index] = arr[index - 1]
                index -= 1
 
            arr[start] = value
 
            # Update all the pointers
            start += 1
            mid += 1
            start2 += 1
 
 
'''
* l is for left index and r is right index of
the sub-array of arr to be sorted
'''
 
def mergeSort(arr, string, l, r):
    if (l < r):
 
        # Same as (l + r) / 2, but avoids overflow
        # for large l and r
        m = l + (r - l) // 2
 
        # Sort first and second halves
        mergeSort(arr, string, l, m)
        mergeSort(arr, string, m + 1, r)
 
        merge(arr, string, l, m, r)

def _multiprocessMergeSort(l, r, size):
    print('Process %d START: start=%d end=%d' % (os.getpid(), l, r))
    shmArray = shm.SharedMemory(name=SHARED_ARRAY_NAME, create=False)
    b = np.ndarray((size, ), dtype=np.int64, buffer=shmArray.buf)
    shmString = shm.SharedMemory(name=SHARED_STRING_NAME, create=False)
    mergeSort(b, shmString, l, r)
    shmArray.close()
    shmString.close()
    print('Process %d END' % (os.getpid(),))

def multiprocessMergeSort(sm):
    numProcess = mp.cpu_count()
    chunkSize = sm.inputSize // numProcess
    while numProcess > 1:
        processes = []
        for i in range(0, numProcess):
            processes.append(mp.Process(target=_multiprocessMergeSort, args=(i * chunkSize, min((i + 1) * chunkSize, sm.inputSize), sm.inputSize)))
        for i in range(0, numProcess):
            processes[i].start()
        for i in range(0, numProcess):
            processes[i].join()
        chunkSize = chunkSize * 2
        numProcess = numProcess // 2
    b = np.ndarray((sm.inputSize, ), dtype=np.int64, buffer=sm.shmArray.buf)
    merge(b, sm.shmString, 0, b.size // 2, b.size - 1)

def inplaceRotationsCompare(t1, t2, string):
    i = t1
    j = t2
    inputLen = string.size
    # Iterate until we find different characters, since these are rotations end index is start index - 1
    for k in range(0, inputLen):
        if string.buf[i] != string.buf[j]:
            ret = -1 if string.buf[i] < string.buf[j] else 1
            return ret
        i = (i + 1) % inputLen
        j = (j + 1) % inputLen
    # Since rotations all have the same length, we can just return 0 here because all characters were the same
    return 0

if __name__ == '__main__':
    print(time.strftime("%H:%M:%S", time.localtime()) + ' : Starting...')
    sm = SharedMemoryManager('./tests/min_tests/min_test4.fa')
    # sm = SharedMemoryManager('./tests/min_tests/min_test3.fa')
    sm.construct()
    print(time.strftime("%H:%M:%S", time.localtime()) + ' : Shared memory constructed...')
    multiprocessFill(sm.inputSize)
    print(time.strftime("%H:%M:%S", time.localtime()) + ' : Array filled...')
    multiprocessMergeSort(sm)
    print(time.strftime("%H:%M:%S", time.localtime()) + ' : Array sorted...')
    b = np.ndarray((sm.inputSize, ), dtype=np.int64, buffer=sm.shmArray.buf)
    print(b[sm.inputSize // 2: sm.inputSize // 2 + 10])
    sm.deconstruct()
    print(time.strftime("%H:%M:%S", time.localtime()) + ' : Ending...')