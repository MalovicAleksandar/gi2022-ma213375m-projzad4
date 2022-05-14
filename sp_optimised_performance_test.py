import gc
from timeit import timeit
import psutil, os
from helper import loadTestFile
from fmi_optimised_sp import  SpOptimisedFMIndex
from bwt_optimised_sp import *

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

def constructSpOptimisedBWT(testInput):
    initMem = process.memory_info().rss / 1024
    r = spRotations(testInput)
    r.sort(key=cmp_to_key(inplaceRotationsCompare))
    bwt = spCalculateLIndex([x[0] for x in r], testInput)
    mem = process.memory_info().rss / 1024
    a[0] += (mem - initMem)

def constructSpOptimisedFMIndex(testInput):
    initMem = process.memory_info().rss / 1024
    SpOptimisedFMIndex(testInput)
    mem = process.memory_info().rss / 1024
    a[0] += (mem - initMem)

def spOptimisedPerformanceTest():
    for i in range(0, len(tests)):
        print('/////')
        print()

        print('TESTING: ' + tests[i])
        testInput = loadTestFile(tests[i])
        print("Input size: " + str(len(testInput)))

        a[0] = 0
        time = timeit(lambda: constructSpOptimisedBWT(testInput), setup='gc.collect()', number=3)
        print("Average BWT construction time in seconds (3 runs): " + str(time/3))
        print("Average BWT memory usage in kB (3 runs): " + str(a[0]/3))

        a[0] = 0
        time = timeit(lambda: constructSpOptimisedFMIndex(testInput), setup='gc.collect()', number=3)
        print("Average FMI construction time in seconds (3 runs): " + str(time/3))
        print("Average FMI memory usage in kB (3 runs): " + str(a[0]/3))

        fmi = SpOptimisedFMIndex(testInput)
        for j in range(0, len(testQueries)):
            print('Testing query: ' + testQueries[j])
            print("Average FMI query time in seconds (3 runs): " + str(timeit(lambda: fmi.query(testQueries[j]), number=3)/3))
        del fmi

        print()
        print('/////')

spOptimisedPerformanceTest() 


