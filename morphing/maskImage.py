'''
Function: maskImage
Author:
Date:
'''
#(INPUT) img: h*w*3 matrix representing the source image.
# (OUTPUT) mask: h*w matrix representing the logical mask
#

from helpers import draw_mask
def maskImage(img):
    '''
    :param img: h*w*3 matrix representing the source image.
    :return: mask: h*w matrix representing the logical mask
    '''
    mask, bbox = draw_mask(img) #use function in helper to select the region to be replaced
    return mask