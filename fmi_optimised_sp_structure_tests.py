import traceback
from bwt_optimised_sp import spCalculateBurrowsWheelerMatrix, spCalculateBurrowsWheelerTransform, spCalculateLIndex
from fmi_optimised_sp import SpOptimisedFIndex
from fmi_optimised_sp import SpOptimisedTally
from fmi_optimised_sp import SpOptimisedSuffixArray
from helper import arraysEqual
from helper import setsEqual


def _testSpOptimisedFIndexStructure(test):
    try:
        fIndex = SpOptimisedFIndex(test['inputBwm'], test['inputString'])
    except ValueError:
        assert test['expectedFailure']
        return
    expectedOutput = test['expectedOutput']
    assert setsEqual(fIndex.dataStructure().keys(), expectedOutput.keys())
    for key in fIndex.dataStructure().keys():
        assert fIndex.dataStructure()[key] == expectedOutput[key]

    
def testSpOptimisedFIndexStructure():
    # Test case 1: None
    _testSpOptimisedFIndexStructure(
        {
            'inputBwm': None,
            'inputString': None,
            'expectedFailure': True
        }
    )
    
    # Test case 2: Valid BWM for input string 'abcd'
    _testSpOptimisedFIndexStructure(
        {
            'inputBwm': [4, 1, 3, 0, 2],
            'inputString': 'GATC$',
            'expectedFailure': False,
            'expectedOutput': {
                '$': 0,
                'A': 1,
                'C': 2,
                'G': 3,
                'T': 4
            },
        }
    )
    
    # Test case 2: Valid BWM with repetition for input string 'aabbab'
    _testSpOptimisedFIndexStructure(
        {
            'inputBwm': [7, 2, 3, 4, 5, 1, 0, 6],
            'inputString': 'GGAAACT$',
            'expectedFailure': False,
            'expectedOutput': {
                '$': 0,
                'A': 1,
                'C': 4,
                'G': 5,
                'T': 7
            },
        }
    )

def _testSpOptimisedTallyStructure(test):
    try:
        tally = SpOptimisedTally(test['input'])
    except ValueError:
        assert test['expectedFailure']
        return
    expectedOutput = test['expectedOutput']
    assert setsEqual(tally.dataStructure().keys(), expectedOutput.keys())
    for key in tally.dataStructure().keys():
        assert arraysEqual(tally.dataStructure()[key], expectedOutput[key])
    
def testSpOptimisedTallyStructure():
    # Test case 1: None
    _testSpOptimisedTallyStructure(
        {
            'input': None,
            'expectedFailure': True
        }
    )
    
    # Test case 2: String with less than 5 characters
    _testSpOptimisedTallyStructure(
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
    _testSpOptimisedTallyStructure(
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

def _testSpOptimisedSuffixArrayStructure(test):
    try:
        bwm = spCalculateBurrowsWheelerMatrix(test['input'])
        lIndex = spCalculateLIndex(bwm, test['input'])
        fIndex = SpOptimisedFIndex(bwm, test['input'])
        tally = SpOptimisedTally(lIndex)
        suffixArray = SpOptimisedSuffixArray(bwm, fIndex, lIndex, tally)
    except ValueError:
        assert test['expectedFailure']
        return
    expectedOutput = test['expectedOutput']
    assert arraysEqual(suffixArray.dataStructure(), expectedOutput)

    
def testSpOptimisedSuffixArrayStructure():
    # Test case 1: None
    _testSpOptimisedSuffixArrayStructure(
        {
            'input': None,
            'expectedFailure': True
        }
    )
    
    # Test case 2: String with one character
    _testSpOptimisedSuffixArrayStructure(
        {
            'input': 'A$',
            'expectedFailure': False,
            'expectedOutput': [1]
        }
    )
    
    # Test case 3: Valid string
    _testSpOptimisedSuffixArrayStructure(
        {
            'input': 'ACGAACG$',
            'expectedFailure': False,
            'expectedOutput': [7, 1]
        }
    )

def testSpOptimisedFMIStructures():
    testSpOptimisedFIndexStructure()
    testSpOptimisedTallyStructure()
    testSpOptimisedSuffixArrayStructure()

if __name__ == '__main__':
    testSpOptimisedFMIStructures()