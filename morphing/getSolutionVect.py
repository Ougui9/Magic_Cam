'''
  File name: getSolutionVect.py
  Author:Yilun Zhang
  Date created:
'''

from scipy import signal
import numpy as np


def getSolutionVect(indexes, source, target, offsetX, offsetY):
    '''

    :param indexes: h'*w' matrix representing the indices of each replacement pixel.
    :param source:
    :param target:
    :param offsetX:
    :param offsetY:
    :return:
    '''
    N = np.amax(indexes)
    Solvectorb = np.zeros(N)
    ker = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
    im_s = signal.convolve2d(source, ker, mode='same')

    h = len(source)
    w = len(source[0])
    H = len(target)
    W = len(target[0])
    for i in range(h):
        for j in range(w):
            I = i + offsetY #position in the target image
            J = j + offsetX
            curVal = im_s[i, j] #current pixel val in source image
            curInd = indexes[I, J] #current indice in indexes map
            if curInd>0: # make sure it is the pixel to be replaced
                upperInd = indexes[I - 1, J] if I > 0 else 0
                rightInd = indexes[I, J + 1] if J < W - 1 else 0
                leftInd = indexes[I, J - 1] if J > 0 else 0
                lowerInd = indexes[I + 1, J] if I < H - 1 else 0


                curB = curVal
                # if the surrounding element is not the ones to be replaced, add the corresponding target pixel value to b
                curB += target[I - 1, J] if upperInd == 0 and I > 0 else 0
                curB += target[I, J+1] if rightInd == 0 and J < W - 1 else 0
                curB += target[I, J - 1] if leftInd == 0 and J > 0 else 0
                curB += target[I + 1, J] if lowerInd == 0 and I < H - 1 else 0
                Solvectorb[curInd-1] = curB
            if curInd == N:
                return Solvectorb
