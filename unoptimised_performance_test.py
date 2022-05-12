import gc
from timeit import timeit
import psutil, os
from helper import loadTestFile
from fmi_unoptimised import FMIndex
from bwt_unoptimised import *

tests = [
    './min_tests/min_test0.fa',
    './min_tests/min_test1.fa',
    './min_tests/min_test2.fa',
    './min_tests/min_test3.fa',
    './min_tests/min_test4.fa'
]

process = psutil.Process(os.getpid())
a = [0,]

def constructUnoptimisedBWT(testInput):
    gc.collect()
    initMem = process.memory_info().rss / 1024
    r = rotationsUnoptimised(testInput)
    r.sort()
    bwt = calculateLIndexUnoptimized(r)
    mem = process.memory_info().rss / 1024
    a[0] += (mem - initMem)

def constructUnoptimisedFMIndex(testInput):
    gc.collect()
    initMem = process.memory_info().rss / 1024
    FMIndex(testInput)
    mem = process.memory_info().rss / 1024
    a[0] += (mem - initMem)

def unoptimisedPerformanceTest():
    for i in range(0, len(tests)):
        print('/////')
        print()

        print('TESTING: ' + tests[i])
        testInput = loadTestFile(tests[i])
        print("Input size: " + str(len(testInput)))

        a[0] = 0
        print("Average BWT construction time in seconds (3 runs): " + str(timeit(lambda: constructUnoptimisedBWT(testInput), number=3)))
        print("Average BWT memory usage in kB (3 runs): " + str(a[0]/3))

        a[0] = 0
        print("Average FMI construction time in seconds (3 runs): " + str(timeit(lambda: constructUnoptimisedFMIndex(testInput), number=3)))
        print("Average FMI memory usage in kB (3 runs): " + str(a[0]/3))

        print()
        print('/////')

unoptimisedPerformanceTest() 


