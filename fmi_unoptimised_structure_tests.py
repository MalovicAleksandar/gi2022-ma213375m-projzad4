from fmi_unoptimised import FIndex
from fmi_unoptimised import Tally
from fmi_unoptimised import SuffixArray
from helper import arraysEqual
from helper import setsEqual

def _testUnoptimisedFIndexStructure(test):
    
    try:
        fIndex = FIndex(test['input'])
    except ValueError:
        assert test['expectedFailure']
        return
    assert fIndex.dataStructure() == test['expectedOutput']
    
def testUnoptimisedFIndexStructure():
    # Test case 1: None
    _testUnoptimisedFIndexStructure(
        {
            'input': None,
            'expectedFailure': True
        }
    )
    
    # Test case 2: Valid BWM for input string 'abcd'
    _testUnoptimisedFIndexStructure(
        {
            'input': ['$abcd','abcd$', 'bcd$a', 'cd$ab', 'd$abc'],
            'expectedFailure': False,
            'expectedOutput': '$abcd',
        }
    )
    
    # Test case 2: Valid BWM with repetition for input string 'aabbab'
    _testUnoptimisedFIndexStructure(
        {
            'input': ['$aabbab','aabbab$','ab$aabb','abbab$a','b$aabba','bab$aab','bbab$aa'],
            'expectedFailure': False,
            'expectedOutput': '$aaabbb',
        }
    )


def _testUnoptimisedTallyStructure(test):
    try:
        tally = Tally(test['input'])
    except ValueError:
        assert test['expectedFailure']
        return
    expectedOutput = test['expectedOutput']
    assert setsEqual(tally.dataStructure().keys(), expectedOutput.keys())
    for key in tally.dataStructure().keys():
        assert arraysEqual(tally.dataStructure()[key], expectedOutput[key])
    
def testUnoptimisedTallyStructure():
    # Test case 1: None
    _testUnoptimisedTallyStructure(
        {
            'input': None,
            'expectedFailure': True
        }
    )
    
    
    # Test case 2: Empty string
    _testUnoptimisedTallyStructure(
        {
            'input': '',
            'expectedFailure': True
        }
    )
    
    # Test case 3: One character string
    _testUnoptimisedTallyStructure(
        {
            'input': 'a',
            'expectedFailure': False,
            'expectedOutput': {
                'a': [1]
            }
        }
    )
    
    # Test case 4: Valid BWT string
    _testUnoptimisedTallyStructure(
        {
            'input': 'abcaab$c',
            'expectedFailure': False,
            'expectedOutput': {
                '$': [0, 0, 0, 0, 0, 0, 1, 1],
                'a': [1, 1, 1, 2, 3, 3, 3, 3],
                'b': [0, 1, 1, 1, 1, 2, 2, 2],
                'c': [0, 0, 1, 1, 1, 1, 1, 2]
            }
        }
    )

def _testUnoptimisedSuffixArrayStructure(test):
    try:
        suffixArray = SuffixArray(test['input'])
    except ValueError:
        assert test['expectedFailure']
        return
    expectedOutput = test['expectedOutput']
    assert arraysEqual(suffixArray.dataStructure(), expectedOutput)
    
def testUnoptimisedSuffixArrayStructure():
    # Test case 1: None
    _testUnoptimisedSuffixArrayStructure(
        {
            'input': None,
            'expectedFailure': True
        }
    )
    
    
    # Test case 2: Empty string
    _testUnoptimisedSuffixArrayStructure(
        {
            'input': '',
            'expectedFailure': True
        }
    )
    
    # Test case 3: String with one character
    _testUnoptimisedSuffixArrayStructure(
        {
            'input': 'a$',
            'expectedFailure': False,
            'expectedOutput': [1, 0]
        }
    )
    
    # Test case 4: Valid string
    _testUnoptimisedSuffixArrayStructure(
        {
            'input': 'abcaabc$',
            'expectedFailure': False,
            'expectedOutput': [7, 3, 4, 0, 5, 1, 6, 2]
        }
    )

def testUnoptimisedFMIStructures():
    testUnoptimisedFIndexStructure()
    testUnoptimisedTallyStructure()
    testUnoptimisedSuffixArrayStructure()
