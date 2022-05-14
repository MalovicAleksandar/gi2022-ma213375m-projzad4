from helper import isBWInputValid
from functools import cmp_to_key

"""
Inplace comparison of rotations for calculating BWT

Provided arguments are tuples containing
start - start index in string - position 0
inputString - string to be queried during comparison - position 1
We need to double the sstring reference due to limitations of the custom sorting mechanisms in python 
"""
def inplaceRotationsCompare(t1, t2):
    i = t1[0]
    j = t2[0]
    inputLen = len(t1[1])
    # Iterate until we find different characters, since these are rotations end index is start index - 1
    for k in range(0, inputLen):
        if (t1[1][i] != t1[1][j]):
            return -1 if t1[1][i] < t1[1][j] else 1
        i = (i + 1) % inputLen
        j = (j + 1) % inputLen
    # Since rotations all have the same length, we can just return 0 here because all characters were the same
    return 0

"""
Returns array of tuples containing start index of rotation in input string and reference to input string to facilitate later sorting
"""
def spRotations(t):
    if not isBWInputValid(t):
        return None
    inputLen = len(t)
    return [ (i, t) for i in range(0, inputLen) ]

"""
Returns array of integers containing start index of rotation in input string
"""
def spCalculateBurrowsWheelerMatrix(t):
    r = spRotations(t)
    if r == None:
        return None
    r.sort(key=cmp_to_key(inplaceRotationsCompare))
    return [x[0] for x in r] if r != None else None

"""
r - array of integers containing start indexes of rotations
t - reference to input string
"""
def spCalculateLIndex(r, t):
    return ''.join(map(lambda x: t[x - 1], r)) if r != None else None

def spCalculateBurrowsWheelerTransform(t):
    r = spCalculateBurrowsWheelerMatrix(t)
    return spCalculateLIndex(r, t) if r != None else None