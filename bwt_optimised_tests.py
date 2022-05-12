from bwt_optimised import *
from shared_memory_management import *

def _testBwtOptimised(testInput, expectedOutput):
    sm = SharedMemoryManager()
    sm.construct(testInput)
    bwt = calculateBurrowsWheelerTransformOptimised(sm)
    sm.deconstruct()
    assert bwt == expectedOutput

def testBwtOptimised():
    _testBwtOptimised('GATGAN$', 'NGGT$AA')

    _testBwtOptimised('TTTGGANNGATCAAAC$', 'CCAAGGATGNTNAATT$')

    _testBwtOptimised('TAAGAGAATTCAAAATAAAATGGTGGACTGGATTCAATCAAGAATTTGGAGATCAAACTAATGTGATCAG$', 'GCTCAAACTACATGGAGCGAAGAGAGAAAGATTTTTAAAAAGAGATGTTTTTGA$CTAATAGGTCAAAATA')

    _testBwtOptimised('CTCTTAGTTCTCCTACTATTCCCACTCACTCTAAAATAACCATTGTACTCAAAGTCTTTGTAGAAGTGGA$', 'AGTCATAGAATTCCTAATATCTCTCCATTTCAAATA$TTGATTTAAACACGGTCCCTCCTCGGTTCAGATC')

if __name__ == '__main__':
    testBwtOptimised()