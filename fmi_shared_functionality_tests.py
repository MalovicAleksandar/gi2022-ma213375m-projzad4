from fmi_optimised_sp import *
from fmi_unoptimised import *
from fmi_optimised import *
from bwt_unoptimised import calculateBurrowsWheelerMatrixUnoptimised
from bwt_unoptimised import calculateLIndexUnoptimized
from bwt_optimised_sp import spCalculateBurrowsWheelerMatrix
from bwt_optimised_sp import spCalculateLIndex
from helper import arraysEqual

def _testFIndexFunctionality(test):
    fIndex = test['class'](test['input'])
    for qTest in test['queryTests']:
        assert (fIndex.first(qTest['char']) == qTest['expectedFirst'] 
            and fIndex.last(qTest['char']) == qTest['expectedLast'])

def testFIndexFunctionality(constr):
    # Test case 1: Valid BWM for input string 'abcd'
    _testFIndexFunctionality(
        {
            'class': constr,
            'input': 'ACGT$',
            'queryTests': [
                {
                    'char': 'A',
                    'expectedFirst': 1,
                    'expectedLast': 1
                },
                {
                    'char': 'C',
                    'expectedFirst': 2,
                    'expectedLast': 2
                },
                {
                    'char': 'N',
                    'expectedFirst': -1,
                    'expectedLast': -1
                }
            ]
        }
    )
    
    # Test case 2: Valid BWM with repetition for input string 'aabbab'
    _testFIndexFunctionality(
        {
            'class': constr,
            'input': 'AACCAC$',
            'queryTests': [
                {
                    'char': 'A',
                    'expectedFirst': 1,
                    'expectedLast': 3
                },
                {
                    'char': 'C',
                    'expectedFirst': 4,
                    'expectedLast': 6
                },
                {
                    'char': 'N',
                    'expectedFirst': -1,
                    'expectedLast': -1
                }
            ]
        }
    )

def constructUnoptimisedFIndex(t):
    bwm = calculateBurrowsWheelerMatrixUnoptimised(t)
    return FIndex(bwm)

def constructSpOptimisedFIndex(t):
    bwm = spCalculateBurrowsWheelerMatrix(t)
    return SpOptimisedFIndex(bwm, t)

def _testTallyFunctionality(test):
    tally = test['class'](test['input'])
    for qTest in test['queryTests']:
        assert tally.query(qTest['char'], qTest['position']) == qTest['expectedRank']

def testTallyFunctionality(constr):
    # Test case 1: One character string
    _testTallyFunctionality(
        {
            'class': constr,
            'input': 'A',
            'queryTests': [
                {
                    'char': 'A',
                    'position': 0,
                    'expectedRank': 1
                },
                {
                    'char': 'A',
                    'position': 2,
                    'expectedRank': -1
                },
                {
                    'char': 'N',
                    'position': 0,
                    'expectedRank': -1
                }
            ]
        }
    )
    
    # Test case 2: Valid BWT string
    _testTallyFunctionality(
        {
            'class': constr,
            'input': 'ACGAAC$G',
            'queryTests': [
                {
                    'char': 'A',
                    'position': 0,
                    'expectedRank': 1
                },
                {
                    'char': 'C',
                    'position': 5,
                    'expectedRank': 2
                },
                {
                    'char': 'N',
                    'position': 0,
                    'expectedRank': -1
                },
                {
                    'char': '$',
                    'position': 6,
                    'expectedRank': 1
                }
            ]
        }
    )

def constructUnoptimisedTally(t):
    return Tally(t)

def constructSpOptimisedTally(t):
    return OptimisedTally(t)

def _testSuffixArrayFunctionality(test):
    suffixArray = test['class'](test['input'])
    for qTest in test['queryTests']:
        assert arraysEqual(suffixArray.query(qTest['start'], qTest['end']), qTest['expectedOffsets'])

def testSuffixArrayFunctionality(constr):
    # Test case 1: String with one character
    
    _testSuffixArrayFunctionality(
        {
            'class': constr,
            'input': 'A$',
            'queryTests': [
                {
                    'start': 1,
                    'end': 2,
                    'expectedOffsets': [0]
                }
            ]
        }
    )
    
    
    # Test case 2: Valid string
    _testSuffixArrayFunctionality(
        {
            'class': constr,
            'input': 'ACGAACG$',
            'queryTests': [
                {
                    'start': 0,
                    'end': 3,
                    'expectedOffsets': [7, 3, 4]
                }
            ]
        }
    )

def constructUnoptimisedSuffixArray(t):
    return SuffixArray(t)

def constructSpOptimisedSuffixArray(t):
    bwm = spCalculateBurrowsWheelerMatrix(t)
    fIndex = SpOptimisedFIndex(bwm, t)
    lIndex = spCalculateLIndex(bwm, t)
    tally = SpOptimisedTally(lIndex)
    return SpOptimisedSuffixArray(bwm, fIndex, lIndex, tally)

def _testFMIndex(test):
    try:
        fmIndex = test['class'](test['input'])
    except ValueError:
        assert test['expectedFailure']
        return
    for qTest in test['queryTests']:
        assert arraysEqual(fmIndex.query(qTest['substring']), qTest['expectedOutput'])

def testFMIndex(constr):
    # Test case 1: None
    _testFMIndex(
        {
            'class': constr,
            'input': None,
            'expectedFailure': True
        }
    )
    
    # Test case 2: Empty string
    _testFMIndex(
        {
            'class': constr,
            'input': '',
            'expectedFailure': True
        }
    )
    
    #Test case 3: Simple string without ending character
    _testFMIndex(
        {
            'class': constr,
            'input': 'GACNT',
            'expectedFailure': False,
            'queryTests': [
                {
                    'substring': 'T',
                    'expectedOutput': [4]
                }
            ]
        }
    )
    
    #Test case 4: Simple string without ending character
    _testFMIndex(
        {
            'class': constr,
            'input': 'GACTGACT',
            'expectedFailure': False,
            'queryTests': [
                {
                    'substring': 'GA',
                    'expectedOutput': [4, 0]
                }
            ]
        }
    )
    
    #Test case 5: Simple string with ending character
    _testFMIndex(
        {
            'class': constr,
            'input': 'GACTGACT$',
            'expectedFailure': False,
            'queryTests': [
                {
                    'substring': 'GA',
                    'expectedOutput': [4, 0]
                }
            ]
        }
    )

    #Test case 6: Simple string with ending character, no match
    _testFMIndex(
        {
            'class': constr,
            'input': 'GACTGACT$',
            'expectedFailure': True,
            'queryTests': [
                {
                    'substring': 'GT',
                    'expectedOutput': []
                }
            ]
        }
    )

def testUnoptimisedFMIndex():
    testFIndexFunctionality(constructUnoptimisedFIndex)
    testTallyFunctionality(constructUnoptimisedTally)
    testSuffixArrayFunctionality(constructUnoptimisedSuffixArray)
    testFMIndex(FMIndex)

def testSpOptimisedFMIndex():
    testFIndexFunctionality(constructSpOptimisedFIndex)
    testTallyFunctionality(constructSpOptimisedTally)
    testSuffixArrayFunctionality(constructSpOptimisedSuffixArray)
    testFMIndex(SpOptimisedFMIndex)

def testOptimisedFMIndex():
    testFMIndex(OptimisedFMIndex)