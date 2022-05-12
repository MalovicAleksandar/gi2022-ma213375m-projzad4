from helper import isInputValid
from bwt_unoptimised import calculateLIndexUnoptimized
from bwt_unoptimised import calculateBurrowsWheelerMatrixUnoptimised

class FIndex(object):
    def __init__(self, bwm):
        if bwm == None:
            raise ValueError('Invalid BWM supplied')
        self.value = ''.join(map(lambda x: x[0], bwm))
        
    """
    Returns first occurence of a character in the F Index, or -1 if character doesn't exist
    """
    def first(self, char):
        try:
            return self.value.index(char)
        except ValueError:
            return -1
    
    """
    Returns last occurence of a character in the F Index, or -1 if character doesn't exist
    """
    def last(self, char):
        try:
            return self.value.rindex(char)
        except ValueError:
            return -1
        
    # Helper function for Structure testing    
    def dataStructure(self):
        return self.value

class Tally(object):
    def __init__(self, bwt):
        if not isInputValid(bwt):
            raise ValueError("Invalid BWT supplied")
        self.value = {}
        for i in range(0, len(bwt)):
            # Copy previous column values to current one
            for row in self.value.values():
                row[i] = row[i-1]
            """ 
            Take current character in input string.
            If a row for said character exists, increment rank. If not, insert a row populated with 0s, and then increment.
            """
            currentChar = bwt[i]
            if currentChar not in self.value:
                self.value[currentChar] = [0] * len(bwt)
            self.value[currentChar][i] += 1
     
    """
    Returns character rank at that position, or -1 if position is below 0 or greater than len, or if character isn't in tally
    """
    def query(self, char, j):
        if (char not in self.value) or (j < 0 or j >= len(self.value[char])):
            return -1
        return self.value[char][j]
    
    # Helper function for Structure testing    
    def dataStructure(self):
        return self.value

class SuffixArray(object):
    def __init__(self, t):
        if not isInputValid(t):
            raise ValueError('Invalid value provided for Suffix Array calculation')
        suffixArray = []
        for i in range(0, len(t)):
            suffixArray.append((i, t[i:]))
        self.value = [suffix[0] for suffix in sorted(suffixArray, key=lambda x: x[1])]
        
    """
    Returns offsets on indexes between start and end
    """
    def query(self, start, end):
        return self.value[start:end]
    
    # Helper function for structure testing
    def dataStructure(self):
        return self.value

class FMIndex(object):
    def __init__(self, t):
        """
        Check if input is a valid string.
        If input doesn't already have the ending character, append the ending character.
        """
        if not isInputValid(t):
            raise ValueError("Invalid input string for calculating FM index")
        tt = t
        if not tt.endswith('$'):
            tt += '$'
        bwm = calculateBurrowsWheelerMatrixUnoptimised(tt)
        
        self.fIndex = FIndex(bwm)
        self.lIndex = calculateLIndexUnoptimized(bwm)
        self.tally = Tally(self.lIndex)
        self.suffixArray = SuffixArray(tt)
    
    """
    Queries the initial string t for substring p. Returns array of indexes within t where p is located.
    """
    def query(self, p):
        start = 0
        end = 0
        length = len(p)
        for i in range(0, length):
            currentChar = p[length - i - 1]
            if start == 0 and end == 0: # first character, look just in F index
                start = self.fIndex.first(currentChar)
                end = self.fIndex.last(currentChar) + 1
            else:
                firstOcc = self.fIndex.first(currentChar)
                start = firstOcc + self.tally.query(currentChar, start - 1)
                end = firstOcc + self.tally.query(currentChar, end)
        return self.suffixArray.query(start, end)

