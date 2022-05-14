import gc
from timeit import timeit
import psutil, os
from helper import loadTestFile
from fmi_optimised import OptimisedFMIndex
from bwt_optimised import *
from shared_memory_management import *

tests = [
    './min_tests/min_test0.fa',
    './min_tests/min_test1.fa',
    './min_tests/min_test2.fa',
    './min_tests/min_test3.fa',
    './min_tests/min_test4.fa'
]

testQueries = [
    'AAA',
    'GAGA',
    'TTCAAAA',
    'TTCCAAGATTAGTAATAA'
]

process = psutil.Process(os.getpid())
a = [0,]

def constructOptimisedBWT(testInput):
    initMem = process.memory_info().rss / 1024
    sm = SharedMemoryManager()
    sm.construct(testInput)
    calculateBurrowsWheelerTransformOptimised(sm)
    mem = process.memory_info().rss / 1024
    sm.deconstruct()
    a[0] += (mem - initMem)

def constructOptimisedFMIndex(testInput):
    initMem = process.memory_info().rss / 1024
    OptimisedFMIndex(testInput)
    mem = process.memory_info().rss / 1024
    a[0] += (mem - initMem)

def optimisedPerformanceTest():
    for i in range(0, len(tests)):
        print('/////')
        print()

        print('TESTING: ' + tests[i])
        testInput = loadTestFile(tests[i])
        print("Input size: " + str(len(testInput)))

        a[0] = 0
        time = timeit(lambda: constructOptimisedBWT(testInput), setup='gc.collect()', number=3)
        print("Average BWT construction time in seconds (3 runs): " + str(time/3))
        print("Average BWT memory usage in kB (3 runs): " + str(a[0]/3))

        a[0] = 0
        time = timeit(lambda: constructOptimisedFMIndex(testInput), setup='gc.collect()', number=3)
        print("Average FMI construction time in seconds (3 runs): " + str(time/3))
        print("Average FMI memory usage in kB (3 runs): " + str(a[0]/3))

        fmi = OptimisedFMIndex(testInput)
        for j in range(0, len(testQueries)):
            print('Testing query: ' + testQueries[j])
            print("Average FMI query time in seconds (3 runs): " + str(timeit(lambda: fmi.query(testQueries[j]), number=3)/3))
        del fmi

        print()
        print('/////')

if __name__ == '__main__':
    optimisedPerformanceTest() 


