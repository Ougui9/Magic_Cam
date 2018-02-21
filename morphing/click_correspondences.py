'''
  File name: click_correspondences.py
  Author: 
  Date created: 
'''

'''
  File clarification:
    Click correspondences between two images
    - Input im1: target image
    - Input im2: source image
    - Output im1_pts: correspondences coordiantes in the target image
    - Output im2_pts: correspondences coordiantes in the source image
'''


from morphing.helpers import cpselect, BPts
import numpy as np
def click_correspondences(im1, im2):
  '''
  :param input im1: source image h*w*3
  :param input im2: target image h*w*3
  :param return im1_pts: N *2 matrix representing correspondences coordinates in first image.
  :param return im2_pts: N *2 matrix representing correspondences coordinates in second image.
  '''

  im1_pts, im2_pts = cpselect(im1, im2) ##click and select the correspondences position
  h = len(im1) #height of the target image
  w = len(im1[0])#width of the target image

  # add some preset boundary point to the set
  # Bounary_pts = BPts(h,w)
  # im1_pts = np.append(im1_pts,Bounary_pts, axis=0)
  # im2_pts = np.append(im2_pts, Bounary_pts, axis =0)
  
  return im1_pts, im2_pts
