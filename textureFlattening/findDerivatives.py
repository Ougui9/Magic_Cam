'''
  File name: findDerivatives.py
  Author: Yilun Zhang
  Date created: 9.24.2017
'''

'''
  File clarification:
    Compute gradient information of the input grayscale image
    - Input I_gray: H x W matrix as image
    - Output Mag: H x W matrix represents the magnitude of derivatives
    - Output Magx: H x W matrix represents the magnitude of derivatives along x-axis
    - Output Magy: H x W matrix represents the magnitude of derivatives along y-axis
    - Output Ori: H x W matrix represents the orientation of derivatives
'''

import numpy as np
import textureFlattening.helpers as helpers
from scipy import signal as sg
def findDerivatives(I_gray):
    # TODO: your code here
    G = helpers.generateGaus2d(11, 11, 1.4) #generate 2d Gaussian filter
    dx, dy = np.gradient(G) #calculate gradients of G

    # convolve image with gradients
    Magx = sg.convolve2d(I_gray, dx, "same")
    Magy = sg.convolve2d(I_gray, dy, "same")

    Mag = np.sqrt(np.square(Magx) + np.square(Magy)) #calculate magtitude of Derivatives
    Ori = np.arctan2(Magx, Magy)#calculate the Orientation
    return Mag, Magx, Magy, Ori
