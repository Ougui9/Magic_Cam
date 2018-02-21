'''
  File name: getIndexes.py
  Author: Yilun ZHang
  Date created:
'''

import numpy as np


def getIndexes(mask, targetH, targetW, offsetX, offsetY):
    '''

    :param mask: The logical matrix h*w representing the replacement region.
    :param targetH: The height of the target image, h'
    :param targetW: The width of the target image, w'
    :param offsetX: The x-axis offset of the source image with respect to the target image.
    :param offsetY: The y-axis offset of the source image with respect to the target image.
    :return: indexes: h'*w' matrix representing the indices of each replacement pixel. The value
0 means that is not a replacement pixel.
    '''
    Mask = np.zeros((targetH, targetW),dtype= int) # preallocate a matrix for mask with target image size
    h = len(mask) #height of small mask (source image)
    w = len(mask[0]) #width of small mask (source image)
    Mask[offsetY:offsetY+h, offsetX:offsetX+w] = mask.copy()  #copy small mask to the position(offset) in the big Mask
    indexes = Mask.copy() #copy Mask to indexes

    preEl = 0
    # from the first element continuously add the former one to the current one , then multiply the result map with Mask
    for i in range(targetH):
        for j in range(targetW):
            indexes[i, j] += preEl
            preEl = indexes[i, j]
    indexes *= Mask

    return indexes
