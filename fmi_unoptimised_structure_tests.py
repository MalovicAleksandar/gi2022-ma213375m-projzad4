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
            'input': ['$GATC','ATC$G', 'C$GAT', 'GATC$', 'TC$GA'],
            'expectedFailure': False,
            'expectedOutput': '$ACGT',
        }
    )
    
    # Test case 2: Valid BWM with repetition for input string 'aabbab'
    _testUnoptimisedFIndexStructure(
        {
            'input': ['$AACCAC','AACCAC$','AC$AACC','ACCAC$A','C$AACCA','CAC$AAC','CCAC$AA'],
            'expectedFailure': False,
            'expectedOutput': '$AAACCC',
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
            'input': 'A',
            'expectedFailure': False,
            'expectedOutput': {
                'A': [1]
            }
        }
    )
    
    # Test case 4: Valid BWT string
    _testUnoptimisedTallyStructure(
        {
            'input': 'ACGAAC$G',
            'expectedFailure': False,
            'expectedOutput': {
                '$': [0, 0, 0, 0, 0, 0, 1, 1],
                'A': [1, 1, 1, 2, 3, 3, 3, 3],
                'C': [0, 1, 1, 1, 1, 2, 2, 2],
                'G': [0, 0, 1, 1, 1, 1, 1, 2]
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
            'input': 'A$',
            'expectedFailure': False,
            'expectedOutput': [1, 0]
        }
    )
    
    # Test case 4: Valid string
    _testUnoptimisedSuffixArrayStructure(
        {
            'input': 'ACGAACG$',
            'expectedFailure': False,
            'expectedOutput': [7, 3, 4, 0, 5, 1, 6, 2]
        }
    )

def testUnoptimisedFMIStructures():
    testUnoptimisedFIndexStructure()
    testUnoptimisedTallyStructure()
    testUnoptimisedSuffixArrayStructure()
