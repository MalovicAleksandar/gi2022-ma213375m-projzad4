from helper import isBWInputValid

def rotationsUnoptimised(t):
    if not isBWInputValid(t):
        return None
    tt = t * 2
    return [ tt[i:i+len(t)] for i in range(0, len(t)) ]

def calculateBurrowsWheelerMatrixUnoptimised(t):
    r = rotationsUnoptimised(t)
    return sorted(r) if r != None else None

def calculateLIndexUnoptimized(t):
    return ''.join(map(lambda x: x[-1], t)) if t != None else None

def calculateBurrowsWheelerTransformUnoptimised(t):
    r = calculateBurrowsWheelerMatrixUnoptimised(t)
    return calculateLIndexUnoptimized(r) if r != None else None