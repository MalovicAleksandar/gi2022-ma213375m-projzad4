from bwt_optimised_sort import multikey_qsort
from shared_memory_management import SHARED_ARRAY_NAME, SHARED_STRING_NAME
import multiprocessing.shared_memory as shm
import numpy as np

def calculateBurrowsWheelerTransformOptimised(sm):
    multikey_qsort(sm.inputSize)
    shmString = shm.SharedMemory(name=SHARED_STRING_NAME, create=False)
    shmArray = shm.SharedMemory(name=SHARED_ARRAY_NAME, create=False)
    array = np.ndarray((sm.inputSize, ), dtype=np.int64, buffer=shmArray.buf)
    bwt = ''.join(map(lambda x: chr(shmString.buf[x - 1 if x > 0 else sm.inputSize - 1]), array))
    shmArray.close()
    shmString.close()
    return bwt
