from fmi_optimised_sp import SpOptimisedFMIndex
from fmi_unoptimised import FIndex, FMIndex
from fmi_unoptimised import Tally
from fmi_unoptimised import SuffixArray
from fmi_optimised import OptimisedFIndex, OptimisedFMIndex
from fmi_optimised import OptimisedTally
from fmi_optimised import OptimisedSuffixArray
from bwt_unoptimised import calculateBurrowsWheelerMatrixUnoptimised
from bwt_unoptimised import calculateLIndexUnoptimized
from helper import arraysEqual

def _testFIndexFunctionality(test):
    fIndex = test['class'](test['input'][0], test['input'][1])
    for qTest in test['queryTests']:
        assert (fIndex.first(qTest['char']) == qTest['expectedFirst'] 
            and fIndex.last(qTest['char']) == qTest['expectedLast'])

def testFIndexFunctionality(constr):
    # Test case 1: Valid BWM for input string 'abcd'
    _testFIndexFunctionality(
        {
            'class': constr,
            'input': ([4, 0, 1, 2, 3], 'abcd$'),
            'queryTests': [
                {
                    'char': 'a',
                    'expectedFirst': 1,
                    'expectedLast': 1
                },
                {
                    'char': 'b',
                    'expectedFirst': 2,
                    'expectedLast': 2
                },
                {
                    'char': 'n',
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
            'input': ([6, 0, 4, 1, 5, 3, 2], 'aabbab$'),
            'queryTests': [
                {
                    'char': 'a',
                    'expectedFirst': 1,
                    'expectedLast': 3
                },
                {
                    'char': 'b',
                    'expectedFirst': 4,
                    'expectedLast': 6
                },
                {
                    'char': 'n',
                    'expectedFirst': -1,
                    'expectedLast': -1
                }
            ]
        }
    )

def constructUnoptimisedFIndex(t):
    return FIndex(t)

def constructOptimisedFIndex(t):
    return OptimisedFIndex(t)

def _testTallyFunctionality(test):
    tally = test['class'](test['input'])
    for qTest in test['queryTests']:
        assert tally.query(qTest['char'], qTest['position']) == qTest['expectedRank']

def testTallyFunctionality(constr):
    # Test case 1: One character string
    _testTallyFunctionality(
        {
            'class': constr,
            'input': 'a',
            'queryTests': [
                {
                    'char': 'a',
                    'position': 0,
                    'expectedRank': 1
                },
                {
                    'char': 'a',
                    'position': 2,
                    'expectedRank': -1
                },
                {
                    'char': 'n',
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
            'input': 'abcaab$c',
            'queryTests': [
                {
                    'char': 'a',
                    'position': 0,
                    'expectedRank': 1
                },
                {
                    'char': 'b',
                    'position': 5,
                    'expectedRank': 2
                },
                {
                    'char': 'n',
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

def constructOptimisedTally(t):
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
            'input': 'a$',
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
            'input': 'abcaabc$',
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

def constructOptimisedSuffixArray(t):
    bwm = calculateBurrowsWheelerMatrixUnoptimised(t)
    fIndex = OptimisedFIndex(bwm)
    lIndex = calculateLIndexUnoptimized(bwm)
    tally = OptimisedTally(lIndex)
    return OptimisedSuffixArray(t, fIndex, lIndex, tally)

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
    testFMIndex(FMIndex)

def testOptimisedFMIndex():
    testFMIndex(OptimisedFMIndex)

def testSpOptimisedFMIndex():
    testFMIndex(SpOptimisedFMIndex)