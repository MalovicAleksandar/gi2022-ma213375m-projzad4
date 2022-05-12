import traceback
from bwt_optimised import calculateBurrowsWheelerTransformOptimised
from fmi_optimised import OptimisedFIndex
from fmi_optimised import OptimisedTally
from fmi_optimised import OptimisedSuffixArray
from bwt_unoptimised import calculateBurrowsWheelerMatrixUnoptimised, calculateLIndexUnoptimized
from bwt_unoptimised import calculateLIndexUnoptimized
from helper import arraysEqual
from helper import setsEqual
from shared_memory_management import SharedMemoryManager
from bwt_optimised_sort import A, C, G, N, T, EOS 

def _testOptimisedFIndexStructure(test):
    try:
        sm = SharedMemoryManager()
        try:
            sm.construct(test['input'])
        except ValueError:
            sm.deconstruct()
            assert test['expectedFailure']
            return
        calculateBurrowsWheelerTransformOptimised(sm)
        try:
            fIndex = OptimisedFIndex(sm)
        except ValueError:
            sm.deconstruct()
            assert test['expectedFailure']
            return
        expectedOutput = test['expectedOutput']
        assert setsEqual(fIndex.dataStructure().keys(), expectedOutput.keys())
        for key in fIndex.dataStructure().keys():
            assert fIndex.dataStructure()[key] == expectedOutput[key]
        sm.deconstruct()
    except:
        sm.deconstruct()
        print(traceback.format_exc())
        exit(-1)
    
    
def testOptimisedFIndexStructure():
    # Test case 1: None
    _testOptimisedFIndexStructure(
        {
            'input': None,
            'expectedFailure': True
        }
    )
    
    # Test case 2: Valid BWM for input string 'abcd'
    _testOptimisedFIndexStructure(
        {
            'input': 'GATC$',
            'expectedFailure': False,
            'expectedOutput': {
                EOS: 0,
                A: 1,
                C: 2,
                G: 3,
                T: 4
            },
        }
    )
    
    # Test case 2: Valid BWM with repetition for input string 'aabbab'
    _testOptimisedFIndexStructure(
        {
            'input': 'GGAAACT$',
            'expectedFailure': False,
            'expectedOutput': {
                EOS: 0,
                A: 1,
                C: 4,
                G: 5,
                T: 7
            },
        }
    )

def _testOptimisedTallyStructure(test):
    try:
        tally = OptimisedTally(test['input'])
    except ValueError:
        assert test['expectedFailure']
        return
    expectedOutput = test['expectedOutput']
    assert setsEqual(tally.dataStructure().keys(), expectedOutput.keys())
    for key in tally.dataStructure().keys():
        assert arraysEqual(tally.dataStructure()[key], expectedOutput[key])
    
def testOptimisedTallyStructure():
    # Test case 1: None
    _testOptimisedTallyStructure(
        {
            'input': None,
            'expectedFailure': True
        }
    )
    
    # Test case 2: String with less than 5 characters
    _testOptimisedTallyStructure(
        {
            'input': 'AGG',
            'expectedFailure': False,
            'expectedOutput': {
                'A': [1],
                'G': [2]
            }
        }
    )
    
    # Test case 3: Valid BWT string with more than 5 characters
    _testOptimisedTallyStructure(
        {
            'input': 'ACG$CCCCATCAAA',
            'expectedFailure': False,
            'expectedOutput': {
                '$': [1, 1],
                'A': [1, 2],
                'C': [2, 5],
                'G': [1, 1],
                'T': [0, 1]
            }
        }
    )

def _testOptimisedSuffixArrayStructure(test):
    try:
        sm = SharedMemoryManager()
        try:
            sm.construct(test['input'])
        except ValueError:
            sm.deconstruct()
            assert test['expectedFailure']
            return
        try:
            lIndex = calculateBurrowsWheelerTransformOptimised(sm)
            fIndex = OptimisedFIndex(sm)
            tally = OptimisedTally(lIndex)
            suffixArray = OptimisedSuffixArray(sm, fIndex, lIndex, tally)
        except ValueError:
            sm.deconstruct()
            assert test['expectedFailure']
            return
        expectedOutput = test['expectedOutput']
        assert arraysEqual(suffixArray.dataStructure(), expectedOutput)
        sm.deconstruct()
    except:
        sm.deconstruct()
        print(traceback.format_exc())
        exit(-1)
    
def testOptimisedSuffixArrayStructure():
    # Test case 1: None
    _testOptimisedSuffixArrayStructure(
        {
            'input': None,
            'expectedFailure': True
        }
    )
    
    # Test case 2: String with one character
    _testOptimisedSuffixArrayStructure(
        {
            'input': 'A$',
            'expectedFailure': False,
            'expectedOutput': [1]
        }
    )
    
    # Test case 3: Valid string
    _testOptimisedSuffixArrayStructure(
        {
            'input': 'ACGAACG$',
            'expectedFailure': False,
            'expectedOutput': [7, 1]
        }
    )

def testOptimisedFMIStructures():
    testOptimisedFIndexStructure()
    testOptimisedTallyStructure()
    testOptimisedSuffixArrayStructure()

if __name__ == '__main__':
    testOptimisedFMIStructures()