from helper import *

def testInputValidation():
    # Test case 1: None, should return false
    assert not isInputValid(None)
    
    # Test case 2: Empty string, should return false
    assert not isInputValid('')
    
    # Test case 3: Valid input
    assert isInputValid('abc')

def testBWInputValidation():
    # Test case 1: None, should return false
    assert not isBWInputValid(None)
    
    # Test case 2: Empty string, should return false
    assert not isBWInputValid('')
    
    # Test case 3: String containing only the ending character, should return false
    assert not isBWInputValid('$')
    
    # Test case 4: String missing ending character, should return false
    assert not isBWInputValid('abc')
    
    # Test case 5: Valid string, should return true
    assert isBWInputValid('abc$')

def testArraysEqual():
    assert not arraysEqual(None, None)
    
    assert not arraysEqual(None, [])
    
    assert not arraysEqual(['0', '1', '2'], ['0', '1', '2', '3'])
    
    assert not arraysEqual(['0', '1'], ['2', '3'])
    
    assert arraysEqual(['0', '1', '2', '3'], ['0', '1', '2', '3'])

def testSetsEqual():
    assert not setsEqual(None, None)
    
    assert not setsEqual(None, [])
    
    assert not setsEqual(['0', '1', '2'], ['0', '1', '2', '3'])
    
    assert not setsEqual(['1', '0'], ['2', '3'])
    
    assert setsEqual(['0', '1', '3', '2'], ['2', '0', '1', '3'])

def testHelpers():
    testInputValidation()
    testBWInputValidation()
    testArraysEqual()
    testSetsEqual()

testHelpers()