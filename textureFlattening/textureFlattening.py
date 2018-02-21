import numpy as np
import matplotlib.pyplot as plt
import os
from scipy import signal as sg


# import functions

from textureFlattening.findDerivatives import findDerivatives
from textureFlattening.nonMaxSup import nonMaxSup
from textureFlattening.edgeLink import edgeLink

import textureFlattening.utils as utils
import textureFlattening.helpers as helpers
from PIL import Image
from textureFlattening.maskImage import maskImage
from textureFlattening.seamlessCloningPoisson import seamlessCloningPoisson
import scipy.io
from textureFlattening.helpers import takePic


def textureFlattening(mode):
    #  to obtain the edgemask
    if mode == '1':
        I =np.array(Image.open('farmer.jpg').convert('RGB'))
    elif mode == '2':
        takePic()
        I = np.array(Image.open('userIm.jpg').convert('RGB'))
    im_gray = utils.rgb2gray(I)
    Mag, Magx, Magy, Ori = findDerivatives(im_gray)
    M = nonMaxSup(Mag, Ori)
    edgeMask = edgeLink(M, Mag, Ori)
    # plt.imshow(edgeMask)
    # plt.show()

    # to calculate blended image
    fuzzyCoeff = 0.3
    offsetX = 0
    offsetY = 0
    print("\nselect the area you want to remove wrinkles\n\nright click for selection, left click to end the selection\n")
    selectedMask = maskImage(I)
    reIM = seamlessCloningPoisson(I, I, selectedMask, offsetX, offsetY, edgeMask, fuzzyCoeff)

    plt.figure(1)
    plt.subplot(121)

    plt.imshow(reIM)

    plt.figure(1)
    plt.subplot(122)

    plt.imshow(I)
    plt.show()


