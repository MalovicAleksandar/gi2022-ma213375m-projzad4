def isInputValid(t):
    return t != None and len(t) > 0

def isBWInputValid(t):
    return t != None and len(t) > 0 and t != "$" and t.endswith('$')

def arraysEqual(output, expectedOutput):
    # Both inputs being None is considered an error as well
    if output is None or expectedOutput is None:
        return False
    if  len(output) != len(expectedOutput):
        return False
    for i in range(0, len(expectedOutput)):
         if output[i] != expectedOutput[i]:
            return False
    return True

def setsEqual(output, expectedOutput):
    # Both input being None is considered an error as well
    if output == None or expectedOutput == None:
        return False
    if  len(output) != len(expectedOutput):
        return False
    for e in output:
         if e not in expectedOutput:
            return False
    return True

def loadTestFile(fileName):
    try:
        file = open(fileName, 'r')
    except FileNotFoundError:
        return None
    lines = []
    line = file.readline()
    if not line:
        return None 
    # skip first line
    line = file.readline()
    while line:
        lines.append(line.strip())
        line = file.readline()
    file.close()
    lines.append('$')
    return ''.join(lines)