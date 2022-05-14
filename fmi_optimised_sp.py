from functools import cmp_to_key
from fmi_unoptimised import FIndex
from fmi_unoptimised import Tally
from fmi_unoptimised import SuffixArray
from helper import isInputValid
from fmi_unoptimised import FMIndex
from bwt_optimised_sp import spCalculateBurrowsWheelerMatrix
from bwt_optimised_sp import spCalculateLIndex
from bwt_optimised_sp import spRotations

class SpOptimisedFIndex(FIndex):
    def __init__(self, bwm, t):
        if bwm == None:
            raise ValueError('Invalid BWM supplied')
        self.dict = {}
        self.inputLen = len(t)
        """
        We are using two helper dictionaries to maintain O(1) search for the last occurence of an char.
        ki - mapping of a key to its index
        ik - mapping of an index to its key
        
        When looking for the next entry in the dictionary, if we have k as the current key, we find next key as
        ik[ki[k] + 1]
        """
        self.ik = {}
        self.ki = {}
        self
        j = 0
        for i in range(0, self.inputLen):
            if t[bwm[i]] not in self.dict:
                self.dict[t[bwm[i]]] = i
                self.ik[j] = t[bwm[i]]
                self.ki[t[bwm[i]]] = j
                j += 1
            
    def first(self, char):
        return self.dict[char] if char in self.dict else -1
    
    def last(self, char):
        if char not in self.dict:
            return -1
        nextIndex = self.ki[char] + 1
        if nextIndex == len(self.dict):
            return self.inputLen - 1
        return self.dict[self.ik[nextIndex]] - 1 if char in self.dict else -1
    
    def dataStructure(self):
        return self.dict

CHECKPOINT_DISTANCE = 5

class SpOptimisedTally(Tally):
    def __init__(self, bwt):
        if bwt == None:
            raise ValueError("Invalid BWT supplied")
        self.tally = {}
        self.chars = set()
        self.bwtLen = len(bwt)
        self.bwt = bwt
        # Calculate optimized tally length
        # we have at least one checkpoint
        self.tallyLen = max(len(bwt) // CHECKPOINT_DISTANCE, 1)
        # Separate counter used to track the optimized tally columns
        tallyCounter = 0
        for i in range(0, self.bwtLen):
            """
            Copy previous column values to current one if is a factor of 5 and we haven't reached end of tally 
            Increment our tallyCounter
            """
            if i > 0 and i % CHECKPOINT_DISTANCE == 0 and tallyCounter < self.tallyLen:
                if tallyCounter + 1 < self.tallyLen:
                    for value in self.tally.values():
                        value[tallyCounter + 1] = value[tallyCounter]
                tallyCounter += 1
            """ 
            Take current character in input string.
            If a row for said character exists, increment rank. If not, insert a row populated with 0s, and then increment.
            If we have passed tally calculation, just update the chars set
            """
            currentChar = bwt[i]
            if tallyCounter < self.tallyLen:
                if currentChar not in self.tally:
                    self.tally[currentChar] = [0] * self.tallyLen
                self.tally[currentChar][tallyCounter] += 1
            self.chars.add(currentChar)
            
    def query(self, char, j):
        if char not in self.chars or j < 0 or j >= self.bwtLen:
            return -1
        else: # calculate position based on nearest checkpoint
            if j % CHECKPOINT_DISTANCE > CHECKPOINT_DISTANCE // 2:
                checkPoint = j // CHECKPOINT_DISTANCE
                # in this branch we must handle the case when we are past the final checkpoint
                if checkPoint != self.tallyLen:
                    target = (checkPoint + 1) * CHECKPOINT_DISTANCE
                    start = j + 1
                    step = 1
                    rankStep = -1
                else:
                    start = (checkPoint - 1) * CHECKPOINT_DISTANCE
                    target = j + 1
                    step = 1
                    rankStep = 1
                # starting rank is 0 if character isn't present in tally
                rank = self.tally[char][checkPoint] if char in self.tally else 0
            else:
                # in this branch we must handle the case when we are close to 0 and therefore don't have previous checkpoint
                checkPoint = j // CHECKPOINT_DISTANCE - 1
                target = j + 1
                step = 1
                rankStep = 1
                if checkPoint == -1:
                    # start at 0 and go up to j and calculate rank in place
                    start = 0
                    rank = 0
                else:
                    # start from existing previous checkpoint
                    start = (checkPoint + 1) * CHECKPOINT_DISTANCE
                    # starting rank is 0 if character isn't present in tally
                    rank = self.tally[char][checkPoint] if char in self.tally else 0
            """
            We are going through the BWT, starting with j and taking a step(+1 or -1) until we reach target
            In each step, if we find the char we are looking for, modify startingRank by value of step(+1 or -1)
            """
            while start != target:
                if self.bwt[start] == char:
                    rank += rankStep
                start += step
            return rank
        
    def dataStructure(self):
        return self.tally

def inplaceSuffixCompare(t1, t2):
    i = t1[0]
    j = t2[0]
    inputLen = len(t1[1])
    # Iterate until we find different characters or one of the arrays reaches end
    while i < inputLen and j < inputLen:
        if (t1[1][i] != t1[1][j]):
            return -1 if t1[1][i] < t1[1][j] else 1
        i = i + 1
        j = j + 1
    # If all characters were equal so far, we can just return difference of suffix lengths, or negative difference of suffix offsets
    return t2[0] - t1[0]

class SpOptimisedSuffixArray(SuffixArray):
    def __init__(self, t, fIndex, lIndex, tally):
        if t == None:
            raise ValueError("Invalid BWT supplied")
        suffixArray = spRotations(t)
        suffixArray.sort(key=cmp_to_key(inplaceSuffixCompare))
        self.value = self.value = [suffix[0] for suffix in suffixArray[::CHECKPOINT_DISTANCE]]
        self.fIndex = fIndex
        self.lIndex = lIndex
        self.tally = tally
            
    def query(self, start, end):
        result = []
        for i in range(start, end):
            # Use LF mapping until we reach a checkpoint, noting how many steps we took
            """
            In case we only have one checkpoint, the math does not work if we start with 0 steps
            In this case the only value in the suffix array is the offset of suffix '$' which is len(BWT)
            In order for the math to still work, therefore start step count must be -len(BWT)

            In case we have multiple checkpoints and are looking for an offset after the final one, we again need to modify the math
            In this case the desired offset is equal to number of steps taken - 1
            """
            steps = 0 if len(self.value) > 1 else -len(self.lIndex)
            afterLast = steps == 0 and i > (len(self.value) - 1) * CHECKPOINT_DISTANCE
            position = i
            while position % CHECKPOINT_DISTANCE != 0:
                # see character in L Index at position
                char = self.lIndex[position]
                # see rank of character at position
                rank = self.tally.query(char, position)
                # see which row in fIndex this rank corresponds to, which is the new position
                position = self.fIndex.first(char) + rank - 1
                # increment steps counter
                steps += 1
            # we have reached a checkpoint, the desire offset is checkpoint + steps taken
            result.append(steps - 1 if afterLast else self.value[position // CHECKPOINT_DISTANCE] + steps)
        return result
                
    def dataStructure(self):
        return self.value

class SpOptimisedFMIndex(FMIndex):
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
        bwm = spCalculateBurrowsWheelerMatrix(tt)
        self.lIndex = spCalculateLIndex(bwm, tt)
        self.fIndex = SpOptimisedFIndex(bwm, tt)
        self.tally = SpOptimisedTally(self.lIndex)
        self.suffixArray = SpOptimisedSuffixArray(tt, self.fIndex, self.lIndex, self.tally)