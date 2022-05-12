from bwt_unoptimised import *
from helper import arraysEqual


def testRotationsUnoptimised():
    # Test case 1: None, should return None
    assert rotationsUnoptimised(None) == None
    
    # Test case 2: Empty string, should return false
    assert rotationsUnoptimised('') == None
    
    # Test case 3: String containing only the ending character, should return false
    assert rotationsUnoptimised('$') == None
    
    # Test case 4: String missing ending character, should return false
    assert rotationsUnoptimised('abc') == None
    
    # Test case 5: Input string of just one character 
    inputValue = 'G$'
    expectedOutput = ['G$', '$G']
    output = rotationsUnoptimised(inputValue)
    assert arraysEqual(output, expectedOutput)
    
    # Test case 6: Valid input string
    inputValue = 'GATC$'
    expectedOutput = ['GATC$', 'ATC$G', 'TC$GA', 'C$GAT', '$GATC']
    output = rotationsUnoptimised(inputValue)
    assert arraysEqual(output, expectedOutput)

def testCalculateBurrowsWheelerMatrixUnoptimised():
    # Test case 1: None, should return None
    assert calculateBurrowsWheelerMatrixUnoptimised(None) == None
    
    # Test case 2: Empty string, should return None
    assert calculateBurrowsWheelerMatrixUnoptimised('') == None
    
    # Test case 3: String containing only the ending character, should return None
    assert calculateBurrowsWheelerMatrixUnoptimised('$') == None
    
    # Test case 4: String missing ending character, should return None
    assert calculateBurrowsWheelerMatrixUnoptimised('GAT') == None
    
    # Test case 5
    inputValue = 'GATC$'
    expectedOutput = ['$GATC','ATC$G', 'C$GAT', 'GATC$', 'TC$GA']
    output = calculateBurrowsWheelerMatrixUnoptimised(inputValue)
    arraysEqual(output, expectedOutput)

def testCalculateLIndexUnoptimised():
    # Test case 1: None, should return None
    assert calculateLIndexUnoptimized(None) == None
    
    # Test case 2:
    assert calculateLIndexUnoptimized(['$GATC','ATC$G', 'C$GAT', 'GATC$', 'TC$GA']) == 'CGT$A'

def testBurrowsWheelerTransformUnoptimised():
    # Test case 1: None, should return None
    assert calculateBurrowsWheelerTransformUnoptimised(None) == None
    
    # Test case 2: Empty string, should return None
    assert calculateBurrowsWheelerTransformUnoptimised('') == None
    
    # Test case 3: String containing only the ending character, should return None
    assert calculateBurrowsWheelerTransformUnoptimised('$') == None
    
    # Test case 4: String missing ending character, should return None
    assert calculateBurrowsWheelerTransformUnoptimised('GAT') == None
    
    # Test case 5
    inputValue = 'GATC$'
    expectedOutput = 'CGT$A'
    output = calculateBurrowsWheelerTransformUnoptimised(inputValue)
    assert output != None
    assert output == expectedOutput
    
    # Test case 6
    inputValue = 'GAATCA$'
    expectedOutput = 'ACGAT$A'
    output = calculateBurrowsWheelerTransformUnoptimised(inputValue)
    assert output != None
    assert output == expectedOutput


def testBWTUnoptimised():
    testRotationsUnoptimised()
    testCalculateBurrowsWheelerMatrixUnoptimised()
    testCalculateLIndexUnoptimised()
    testBurrowsWheelerTransformUnoptimised()

testBWTUnoptimised()