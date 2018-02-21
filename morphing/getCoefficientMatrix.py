'''
  File name: getCoefficientMatrix.py
  Author: Yilun Zhang
  Date created:
'''
import numpy as np
from scipy.sparse import lil_matrix


def getCoefficientMatrix(indexes):
    '''

    :param indexes:h'*w' matrix representing the indices of each replacement pixel.
    :return: coeffA: an N *N sparse matrix representing the Coefficient Matrix, where N is the
number of replacement pixels.
    '''
    N = np.amax(indexes) #number of pixel to be replaced

    coeffA = lil_matrix((N,N)) # preallocate a sparse list matrix for the coeffA
    H = len(indexes) #height of the target image
    W = len(indexes[0]) #width of the target image
    for i in range(H):
        for j in range(W):
            curVal = indexes[i, j] #current indice val in indexes map

            if curVal>0: # make sure it is the pixel to be replaced
                #obtain the surrounding indice values of the current indice
                upperVal = indexes[i-1, j] if i>0 else 0
                rightVal = indexes[i, j+1] if j<W-1 else 0
                leftVal = indexes[i, j-1] if j>0 else 0
                lowerVal = indexes[i+1, j] if i<H-1 else 0
                #set the coeffA
                coeffA[curVal-1,curVal-1]= 4
                if upperVal > 0: coeffA[curVal-1,upperVal-1] = -1
                if lowerVal > 0: coeffA[curVal-1,lowerVal-1] = -1
                if leftVal > 0: coeffA[curVal-1,leftVal-1] = -1
                if rightVal > 0: coeffA[curVal-1,rightVal-1] = -1
            if curVal == N: # to save time, if find it's the largest indice, return
                return coeffA.tocsc(copy=False)

