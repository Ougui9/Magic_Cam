'''
  File name: reconstructImg.py
  Author: Yilun Zhang
  Date created:
'''


import numpy as np

def reconstructImg(indexes, red, green, blue, targetImg):
    '''
    :param indexes: h'*w' matrix representing the indices of each replacement pixel.
    :param red: 1*N vector representing the intensity of the red channel replacement pixel.
    :param green: 1*N vector representing the intensity of the green channel replacement pixel.
    :param blue: 1*N vector representing the intensity of the blue channel replacement pixel.
    :param targetImg: h'*w'*3 matrix representing the target image.
    :return: resultImg: h'*w'*3 matrix representing the resulting cloned image
    '''
    inten = np.array([np.stack([red,green,blue],axis=0).T])# combine pixel value of three channals
    inten = np.clip(inten, 0, 255)
    h = len(targetImg) # height of the target image
    w = len(targetImg[0]) # width of the target image
    N = np.amax(indexes)
    resultImg = targetImg.copy()
    for i in range(h):
        for j in range(w):
            k=indexes[i, j]
            if k>0: # if current indice>0, replace pixel of the target image
                resultImg[i, j, :] = inten[0, k-1,:]
            if k == N:
                return resultImg

