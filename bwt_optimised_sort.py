import multiprocessing as mp
import multiprocessing.shared_memory as shm
import numpy as np
import os
import queue as q
from shared_memory_management import SHARED_STRING_NAME, SHARED_ARRAY_NAME

A = 65
C = 67
G = 71
N = 78
T = 84
EOS = 36

def swap(array, i, j):
    value = array[i]
    array[i] = array[j]
    array[j] = value

def partition_sort(array, d, string, length, l, r, high):
    i = l
    j = r
    swapped = False
    while i < j:
        if string.buf[(array[i] + d) % length] == high:
            j -= 1
            if string.buf[(array[j] + d) % length] != high:
                swap(array, i, j)
                swapped = True
        else:
            i+=1
    if swapped:
        return i
    else:
        return r if r > i + 1 else i

def three_way_partition(array, d, string, length, pivot, l, r):
    i = l
    k = l
    j = r - 1
    eos = -1
    while k <= j:
        char = string.buf[(array[k] + d) % length]
        if char < pivot:
            if char == EOS:
                # remember position of EOS for later
                eos = i
            swap(array, i, k)
            i+=1
            k+=1
        elif char == pivot:
            k+=1
        else: # greater than pivot
            swap(array, k, j)
            j-=1
    return i, k, eos

def quicksort(array, d, string, length, l, r):
    leftL = l
    midL, midR, eos = three_way_partition(array, d, string, length, G, l, r)
    if eos != -1: 
        # if EOS was in this partition, swap it to the start of the array
        swap(array, leftL, eos)
        leftL = leftL + 1
    leftM = partition_sort(array, d, string, length, leftL, midL, C)
    rightM = partition_sort(array, d, string, length, midR, r, T)
    return leftL, leftM, midL, midR, rightM, r

def _multikey_qsort(queue, size):
    #print('Process %d START, queue %d' % (os.getpid(), id(queue)))
    shmString = shm.SharedMemory(name=SHARED_STRING_NAME, create=False)
    shmArray = shm.SharedMemory(name=SHARED_ARRAY_NAME, create=False)
    array = np.ndarray((size, ), dtype=np.int64, buffer=shmArray.buf)
    try:
        while True:
            bucket = queue.get()
            lb = bucket[0]
            rb = bucket[1]
            db = bucket[2]
            #print('Process %d pulled bucket: l=%d ; r=%d ; d=%d' % (os.getpid(), lb, rb, db,))
            l, leftM, midL, midR, rightM, r = quicksort(array, db, shmString, size, lb, rb)
            if leftM < midL:
                if leftM - l > 1:
                    queue.put((l, leftM, db + 1))
                if midL - leftM > 1:
                    queue.put((leftM, midL, db + 1))
            elif midL - l > 1:
                queue.put((l, midL, db + 1))
            if midR - midL > 1:
                queue.put((midL, midR, db + 1))
            if rightM < r:
                if rightM - midR > 1:
                    queue.put((midR, rightM, db + 1))
                if r - rightM > 1:
                    queue.put((rightM, r, db + 1))
            elif r - midR > 1:
                queue.put((midR, r, db + 1))
            queue.task_done()
            #print('Process %d finished bucket: l=%d ; r=%d ; d=%d' % (os.getpid(), lb, rb, db,))
    except q.Full:
        print('Process %d FULL EXCEPTION' % (os.getpid(),))
    except ValueError:
        print('Process %d VALUE EXCEPTION' % (os.getpid(),))
    except:
        print('Process %d OTHER EXCEPTION' % (os.getpid(),))
    shmArray.close()
    shmString.close()
    #print('Process %d END' % (os.getpid(),))

def _sp_multikey_qsort(array, string, length, d, l, r):
    l, leftM, midL, midR, rightM, r = quicksort(array, d, string, length, l, r)
    if leftM < midL:
        if leftM - l > 1:
            _sp_multikey_qsort(array, string, length, d + 1, l, leftM)
        if midL - leftM > 1:
            _sp_multikey_qsort(array, string, length, d + 1, leftM, midL)
    elif midL - l > 1:
        _sp_multikey_qsort(array, string, length, d + 1, l, midL)
    if midR - midL > 1:
        _sp_multikey_qsort(array, string, length, d + 1, midL, midR)
    if rightM < r:
        if rightM - midR > 1:
            _sp_multikey_qsort(array, string, length, d + 1, midR, rightM)
        if r - rightM > 1:
            _sp_multikey_qsort(array, string, length, d + 1, rightM, r)
    elif r - midR > 1:
        _sp_multikey_qsort(array, string, length, d + 1, midR, r)

def multikey_qsort(size):
    if size > 500:
        numProcess = mp.cpu_count()
        queue = mp.JoinableQueue(size * numProcess * 5)
        queue.put((0, size, 0))
        numProcess = mp.cpu_count()
        processes = []
        for i in range(0, numProcess):
            processes.append(mp.Process(target=_multikey_qsort, args=(queue, size,)))
        for i in range(0, numProcess):
            processes[i].start()
        queue.join()
        queue.close()
        for i in range(0, numProcess):
            processes[i].terminate()
            processes[i].join()
    else:
        shmString = shm.SharedMemory(name=SHARED_STRING_NAME, create=False)
        shmArray = shm.SharedMemory(name=SHARED_ARRAY_NAME, create=False)
        array = np.ndarray((size, ), dtype=np.int64, buffer=shmArray.buf)
        _sp_multikey_qsort(array, shmString, size, 0, 0, size)
        shmArray.close()
        shmString.close()