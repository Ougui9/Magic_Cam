'''
  File name: seamlessCloningPoisson.py
  Author: Yilun Zhang
  Date created:
'''

import numpy as np
from textureFlattening.getIndexes import getIndexes
from textureFlattening.getCoefficientMatrix import getCoefficientMatrix
from textureFlattening.getSolutionVect import getSolutionVect
from textureFlattening.reconstructImg import reconstructImg
from scipy.sparse import linalg

def seamlessCloningPoisson(sourceImg, targetImg, mask, offsetX, offsetY, edgeMask, fuzzyCoeff):
    '''

    :param sourceImg: h*w*3 matrix representing the source image.
    :param targetImg: h'*w'*3 matrix representing the target image.
    :param mask: The logical matrix hw representing the replacement region
    :param offsetX: The x-axis offset of the source image with respect to the target image.
    :param offsetY: The y-axis offset of the source image with respect to the target image.
    :return: resultImg: h'*w'*3 matrix representing the resulting cloned image.
    '''

    H = len(targetImg) #height of target image
    W = len(targetImg[0]) #width of target image
    ch = len(sourceImg[0,0]) # channel of source image
    indexes = getIndexes(mask, H, W, offsetX, offsetY)
    N = np.amax(indexes) #number of pixel to be replaced
    coeffA = getCoefficientMatrix(indexes) #get coeffA
    b = np.zeros((N,ch))# preallocate a matrix for b

    for i in range(ch):
        b[:, i] = getSolutionVect(indexes, sourceImg[:, :, i], targetImg[:, :, i], offsetX, offsetY, edgeMask, fuzzyCoeff)

    f = linalg.spsolve(coeffA,b) # solve the equation for blended pixel value
    resultImg = reconstructImg(indexes,f[:,0],f[:,1],f[:,2],targetImg)



    return resultImg
