import multiprocessing.shared_memory as shm
import numpy as np
import multiprocessing as mp

SHARED_STRING_NAME= 'shm_string'
SHARED_ARRAY_NAME = 'shm_suffix_array'

def _multiprocessIndexFill(arrayName, start, end, size):
    shmArray = shm.SharedMemory(name=arrayName, create=False)
    b = np.ndarray((size, ), dtype=np.int64, buffer=shmArray.buf)
    for i in range(start, end):
       b[i] = i
    shmArray.close()

def multiprocessIndexFill(size, arrayName):
    numProcess = mp.cpu_count()
    processes = []
    chunkSize = size // numProcess
    if (chunkSize > 0):
        for i in range(0, numProcess):
            processes.append(mp.Process(target=_multiprocessIndexFill, args=(arrayName, i * chunkSize, (i + 1) * chunkSize if i != numProcess - 1 else size, size,)))
        for i in range(0, numProcess):
            processes[i].start()
        for i in range(0, numProcess):
            processes[i].join()
    else:
        _multiprocessIndexFill(arrayName, 0, size, size)

class SharedMemoryManager():

    def construct(self, b):
        self.inputSize = -1
        if b == None:
            raise ValueError("Invalid input value")
        self.inputSize = len(b)
        try:
            self.shmString = shm.SharedMemory(name=SHARED_STRING_NAME, create=True, size=len(b))
        except FileExistsError:
            self.shmString = shm.SharedMemory(name=SHARED_STRING_NAME, create=False, size=len(b))
        for i in range(0, len(b)):
            self.shmString.buf[i] = ord(b[i])
        try:
            self.shmArray = shm.SharedMemory(name=SHARED_ARRAY_NAME, create=True, size = len(b) * 8)
        except FileExistsError:
            self.shmArray = shm.SharedMemory(name=SHARED_ARRAY_NAME, create=False, size = len(b) * 8)
        multiprocessIndexFill(self.inputSize, SHARED_ARRAY_NAME)

    def deconstruct(self):
        if self.inputSize != -1:
            self.shmString.close()
            self.shmString.unlink()
            self.shmArray.close()
            self.shmArray.unlink()