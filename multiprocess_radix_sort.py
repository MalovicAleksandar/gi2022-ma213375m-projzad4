import numpy as np
from helper import loadTestFile
import multiprocess_merge_sort as mpms
import time
import sys
import multiprocessing as mp
import multiprocessing.shared_memory as shm
import os
import queue as q

SHARED_STRING_NAME= 'shm_string'
SHARED_ARRAY_NAME = 'shm_array'

class SharedMemoryManager():
    def __init__(self, inputFile):
        self.inputFile = inputFile

    def construct(self):
        b = bytes(loadTestFile(self.inputFile), 'utf-8')
        self.inputSize = len(b)
        try:
            self.shmString = shm.SharedMemory(name=SHARED_STRING_NAME, create=True, size=len(b))
        except FileExistsError:
            self.shmString = shm.SharedMemory(name=SHARED_STRING_NAME, create=False, size=len(b))
        for i in range(0, len(b)):
            self.shmString.buf[i] = b[i]
        try:
            self.shmArray = shm.SharedMemory(name=SHARED_ARRAY_NAME, create=True, size = len(b) * 8)
        except FileExistsError:
            self.shmArray = shm.SharedMemory(name=SHARED_ARRAY_NAME, create=False, size = len(b) * 8)

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
        processes.append(mp.Process(target=_multiprocessFill, args=(i * chunkSize, (i + 1) * chunkSize if i != numProcess - 1 else size, size,)))
    for i in range(0, numProcess):
        processes[i].start()
    for i in range(0, numProcess):
        processes[i].join()

PIVOT_G = 71
C = 67
T = 84
EOS = 36

def swap(array, i, j):
    value = array[i]
    array[i] = array[j]
    array[j] = value

def sizeCheck(array, d, string, length, l, r):
    if r - l <= 2:
        if r - l == 2 and string.buf[(array[r - 1] + d) % length] < string.buf[(array[l] + d) % length]:
            swap(array, l, r - 1)
        return 0
    else:
        return 1

def partition_sort(array, d, string, length, l, r, high):
    if sizeCheck(array, d, string, length, l, r) == 0:
        return -1
    i = l
    j = r - 1
    while i < j:
        if string.buf[(array[i] + d) % length] == high:
            swap(array, i, j)
            j -= 1
        else:
            i+=1
    return i + 1

def three_way_partition(array, d, string, length, pivot, l, r):
    if sizeCheck(array, d, string, length, l, r) == 0:
        return -1, -1, -1
    i = l
    k = l
    j = r - 1
    eos = -1
    while k <= j:
        if string.buf[(array[k] + d) % length] < pivot:
            if string.buf[(array[k] + d) % length] == EOS:
                # remember position of EOS for later
                eos = i
            swap(array, i, k)
            i+=1
            k+=1
        elif string.buf[(array[k] + d) % length] == pivot:
            k+=1
        else: # greater than pivot
            swap(array, k, j)
            j-=1
    return i, k, eos

def quicksort(array, d, string, length, l, r):
    if sizeCheck(array, d, string, length, l, r) == 0:
        return -1, -1, -1, -1, -1, -1
    leftL = l
    midL, midR, eos = three_way_partition(array, d, string, length, PIVOT_G, l, r)
    if eos != -1: 
        # if EOS was in this partition, swap it to the start of the array
        swap(array, leftL, eos)
        leftL = leftL + 1
    leftM = partition_sort(array, d, string, length, leftL, midL, C)
    rightM = partition_sort(array, d, string, length, midR, r, T)
    return leftL, leftM, midL, midR if midR != midL else midR + 1, rightM, r

def _multikey_qsort(array, string, length, d, l, r):
    if sizeCheck(array, d, string, length, l, r) == 0:
        return
    l, leftM, midL, midR, rightM, r = quicksort(array, d, string, length, l, r)
    if leftM != -1:
        multikey_qsort(array, string, length, d + 1, l, leftM)
        multikey_qsort(array, string, length, d + 1, leftM, midL)
    elif midL - l > 1:
            multikey_qsort(array, string, length, d + 1, l, midL)
    if midR - midL > 1:
        multikey_qsort(array, string, length, d + 1, midL, midR)
    if rightM != -1:
        multikey_qsort(array, string, length, d + 1, midR, rightM)
        multikey_qsort(array, string, length, d + 1, rightM, r)
    elif r - midR > 1:
        multikey_qsort(array, string, length, d + 1, midR, r)

def multikey_qsort(queue, size):
    print('Process %d START, queue %d' % (os.getpid(), id(queue)))
    shmString = shm.SharedMemory(name=SHARED_STRING_NAME, create=False)
    shmArray = shm.SharedMemory(name=SHARED_ARRAY_NAME, create=False)
    array = np.ndarray((size, ), dtype=np.int64, buffer=shmArray.buf)
    try:
        while True:
            bucket = queue.get()
            lb = bucket[0]
            rb = bucket[1]
            db = bucket[2]
            print('Process %d pulled bucket: l=%d ; r=%d ; d=%d' % (os.getpid(), lb, rb, db,))
            l, leftM, midL, midR, rightM, r = quicksort(array, db, shmString, size, lb, rb)
            if leftM != -1:
                queue.put((l, leftM, db + 1))
                queue.put((leftM, midL, db + 1))
            elif midL - l > 1:
                queue.put((l, midL, db + 1))
            if midR - midL > 1:
                queue.put((midL, midR, db + 1))
            if rightM != -1:
                queue.put((midR, rightM, db + 1))
                queue.put((rightM, r, db + 1))
            elif r - midR > 1:
                queue.put((midR, r, db + 1))
            queue.task_done()
            print('Process %d finished bucket: l=%d ; r=%d ; d=%d' % (os.getpid(), lb, rb, db,))
    except q.Full:
        print('Process %d FULL EXCEPTION' % (os.getpid(),))
    except ValueError:
        print('Process %d VALUE EXCEPTION' % (os.getpid(),))
    except:
        print('Process %d OTHER EXCEPTION' % (os.getpid(),))
    print('Process %d END' % (os.getpid(),))

def printSortedString(array, l, r, d):
    print('////')
    dd = d if d == 0 else d - 1
    for i in range(l, r + 1):
        print(longstring[array[i - dd]: array[i - dd] + len(b)])  
    print('////')

longstring = None

if __name__ == '__main__':
    print(time.strftime("%H:%M:%S", time.localtime()) + ' : Starting...')
    print('Num processes: ' + str(mp.cpu_count()))
    #b = loadTestFile('./tests/min_tests/min_test4.fa')
    #b = 'TTTGGANNGATCAAAC$'
    b = 'GATGAN$'
    #sm = SharedMemoryManager('./min_tests/min_test0.fa')
    sm = SharedMemoryManager('./min_tests/min_test1.fa')
    sm.construct()
    print(time.strftime("%H:%M:%S", time.localtime()) + ' : Shared memory constructed...')
    multiprocessFill(sm.inputSize)
    #longstring = b * 2
    #a = np.empty(len(b), dtype=np.int64)
    #for i in range(0, len(b)):
    #    a[i] = i
    print(time.strftime("%H:%M:%S", time.localtime()) + ' : Array filled... ' + str(sm.inputSize))
    queue = mp.JoinableQueue(sm.inputSize)
    queue.put((0, sm.inputSize, 0))
    numProcess = mp.cpu_count()
    processes = []
    for i in range(0, numProcess):
        processes.append(mp.Process(target=multikey_qsort, args=(queue, sm.inputSize,)))
    for i in range(0, numProcess):
        processes[i].start()
    queue.join()
    queue.close()
    for i in range(0, numProcess):
        processes[i].terminate()
        processes[i].join()
    #multikey_qsort(a, b, 0, 0, len(b) - 1)
    #for i in range(0, len(b)):
    #    print(longstring[a[i]: a[i] + len(b)])
    print(time.strftime("%H:%M:%S", time.localtime()) + ' : Array sorted...')
    c = np.ndarray((sm.inputSize, ), dtype=np.int64, buffer=sm.shmArray.buf)
    print(c)
    sm.deconstruct()
    print(time.strftime("%H:%M:%S", time.localtime()) + ' : Ending...')

