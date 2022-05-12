from numpy import int64
import numpy
import time
import sys

PIVOT_G = 'G'
C = 'C'
T = 'T'
EOS = '$'

def swap(array, i, j):
    value = array[i]
    array[i] = array[j]
    array[j] = value

def sizeCheck(array, d, string, length, l, r):
    if r - l <= 2:
        if r - l == 2 and string[(array[r - 1] + d) % length] < string[(array[l] + d) % length]:
            swap(array, l, r - 1)
        return 0
    else:
        return 1

def partition_sort(array, d, string, length, l, r, high):
    printSortedString(array, l, r, d)
    i = l
    j = r
    swapped = False
    while i < j:
        if string[(array[i] + d) % length] == high:
            j -= 1
            if string[(array[j] + d) % length] != high:
                swap(array, i, j)
                swapped = True
        else:
            i+=1
    printSortedString(array, l, r, d)
    if swapped:
        return i
    else:
        return r if r > i + 1 else i

def three_way_partition(array, d, string, length, pivot, l, r):
    i = l
    k = l
    j = r - 1
    eos = -1
    while k <= j:
        if string[(array[k] + d) % length] < pivot:
            if string[(array[k] + d) % length] == EOS:
                # remember position of EOS for later
                eos = i
            swap(array, i, k)
            i+=1
            k+=1
        elif string[(array[k] + d) % length] == pivot:
            k+=1
        else: # greater than pivot
            swap(array, k, j)
            j-=1
    return i, k, eos

def quicksort(array, d, string, length, l, r):
    leftL = l
    printSortedString(array, l, r, d)
    midL, midR, eos = three_way_partition(array, d, string, length, PIVOT_G, l, r)
    printSortedString(array, l, r, d)
    if eos != -1: 
        # if EOS was in this partition, swap it to the start of the array
        swap(array, leftL, eos)
        leftL = leftL + 1
    leftM = partition_sort(array, d, string, length, leftL, midL, C)
    printSortedString(array, l, r, d)
    rightM = partition_sort(array, d, string, length, midR, r, T)
    printSortedString(array, l, r, d)
    return leftL, leftM, midL, midR, rightM, r

def multikey_qsort(array, string, length, d, l, r):
    printSortedString(array, l, r, d)
    l, leftM, midL, midR, rightM, r = quicksort(array, d, string, length, l, r)
    if leftM < midL:
        if leftM - l > 1:
            multikey_qsort(array, string, length, d + 1, l, leftM)
        if midL - leftM > 1:
            multikey_qsort(array, string, length, d + 1, leftM, midL)
    elif midL - l > 1:
        multikey_qsort(array, string, length, d + 1, l, midL)
    if midR - midL > 1:
        multikey_qsort(array, string, length, d + 1, midL, midR)
    if rightM < r:
        if rightM - midR > 1:
            multikey_qsort(array, string, length, d + 1, midR, rightM)
        if r - rightM > 1:
            multikey_qsort(array, string, length, d + 1, rightM, r)
    elif r - midR > 1:
        multikey_qsort(array, string, length, d + 1, midR, r)

def printSortedString(array, l, r, d):
    print('//// ' + str(d))
    for i in range(l, r):
        print(longstring[array[i]: array[i] + len(b)])  
    print('//// ' + str(d))

longstring = None

if __name__ == '__main__':
    print(sys.getrecursionlimit())
    sys.setrecursionlimit(1500)
    print(time.strftime("%H:%M:%S", time.localtime()) + ' : Starting...')
    #b = 'TTTGGANNGATCAAAC$'
    #b = 'TAAGAGAATTCAAAATAAAATGGTGGACTGGATTCAATCAAGAATTTGGAGATCAAACTAATGTGATCAG$'
    b = 'GATGAN$'
    #b = 'CTCTTAGTTCTCCTACTATTCCCACTCACTCTAAAATAACCATTGTACTCAAAGTCTTTGTAGAAGTGGA$'
    longstring = b * 2
    a = numpy.empty(len(b), dtype=int64)
    for i in range(0, len(b)):
        a[i] = i
    print(time.strftime("%H:%M:%S", time.localtime()) + ' : Array filled... ' + str(len(b)))
    multikey_qsort(a, b, len(b), 0, 0, len(b))
    for i in range(0, len(b)):
        print(longstring[a[i]: a[i] + len(b)])
    print(a)
    print(time.strftime("%H:%M:%S", time.localtime()) + ' : Array sorted...')

