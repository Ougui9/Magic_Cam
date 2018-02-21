'''
  File name: morph_tri.py
  Author: Yilun Zhang
  Date created: 10/13/2017
'''

'''
  File clarification:
    Image morphing via Triangulation
    - Input im1: target image
    - Input im2: source image
    - Input im1_pts: correspondences coordiantes in the target image
    - Input im2_pts: correspondences coordiantes in the source image
    - Input warp_frac: a vector contains warping parameters
    - Input dissolve_frac: a vector contains cross dissolve parameters

    - Output inteIm: a set of morphed images obtained from different warp and dissolve parameters.
                         The size should be [number of images, image height, image Width, color channel number]
'''

from scipy.spatial import Delaunay
import numpy as np
from morphing import helpers

def morph_tri(im1, im2, im1_pts, im2_pts, warp_frac, dissolve_frac):
  '''

  :param im1: target image [h*w*3]
  :param im2: source image [h*w*3]
  :param im1_pts: N*2 matrix representing correspondences in the first image.
  :param im2_pts: N *2 matrix representing correspondences in the second image.
  :param warp_frac:1* M vector representing each frames shape warping parameter
  :param dissolve_frac:1*M vector representing each frames cross-dissolve parameter.
  :return: morphed_im: [numIm*h*w*3] morphed image set
  '''

  (h, w, l) = np.shape(im1) # obtain height, width and layer(color channel) of 1st image(target)

  numIm = len(warp_frac) # number of frames we hope to generate
  morphed_im = np.zeros([numIm, h, w, l]) # preallocate a matrix for the result morphed image

  for m in range(numIm): #loop for every frame
      # print m
      inte_pts = (1 - warp_frac[m]) * im1_pts +  warp_frac[m] * im2_pts # calculate the position of corresponding points on intermediate image
      Tri = Delaunay(inte_pts) #generate the Delaunay Triangles
      numTri = len(Tri.simplices)   # number of triangles
      triCornerMat = np.ones([numTri,3,3])   # preallocate a matrix for triangle corner coordinates

      for k in range(numTri):  #loop for every triangles
        #generate the triangle corner coordinates in the intermediate image
        coor_pts0 = inte_pts[Tri.simplices[k, 0]]
        coor_pts1 = inte_pts[Tri.simplices[k, 1]]
        coor_pts2 = inte_pts[Tri.simplices[k, 2]]
        triCornerMat[k,:,:] = np.transpose([np.append(coor_pts0,1),np.append(coor_pts1,1),np.append(coor_pts2,1)]) #form a matrix for triangle corner coordinates in the intermediate image

      for i in range(h): ##loop for rows (y axis)
        for j in range(w):##loop for cols (x axis)

          NTri = int(Tri.find_simplex(np.array([j,i]))) ## make sure which triangle the current point is located in
          if NTri>=0:
              baryCoor= np.linalg.solve(triCornerMat[NTri,:,:],np.asarray([[j],[i],[1]])) # calculate the barycentric coordinate
    
              coor_Sorpts0, coor_Sorpts1, coor_Sorpts2 = im2_pts[Tri.simplices[NTri, 0]],im2_pts[Tri.simplices[NTri, 1]],im2_pts[Tri.simplices[NTri, 2]] #corresponding triangle corner coordinates in the source image
              sorTriCornerMat = np.transpose([np.append(coor_Sorpts0, 1), np.append(coor_Sorpts1, 1),np.append(coor_Sorpts2, 1)]) #triangle corner coordinates matrix in the source image
              posSor = np.dot(sorTriCornerMat,baryCoor) # calculate the corresponding pixel coordinate in source image
              posSor = helpers.switchAxis(np.transpose(posSor/posSor[2, 0])[0,0:2]) #switch(h,w) to (x,y) sequence
    
              coor_Tarpts0, coor_Tarpts1, coor_Tarpts2 = im1_pts[Tri.simplices[NTri, 0]], im1_pts[Tri.simplices[NTri, 1]], im1_pts[Tri.simplices[NTri, 2]]#corresponding triangle corner coordinates in the target image
              tarTriCornerMat = np.transpose([np.append(coor_Tarpts0, 1), np.append(coor_Tarpts1, 1),np.append(coor_Tarpts2, 1)])#triangle corner coordinates matrix in the target image
              posTar = np.dot(tarTriCornerMat, baryCoor)# calculate the corresponding pixel coordinate in target image
              posTar = helpers.switchAxis(np.transpose(posTar / posTar[2, 0])[0,0:2])#switch(h,w) to (x,y) sequence
              
              # make sure coordinates not out of the image of the image
              Tar_posfinal_i=int(round(posTar[0])) if int(round(posTar[0]))<h else h-1
              Tar_posfinal_j = int(round(posTar[1])) if int(round(posTar[1])) < w else w-1
              Sor_posfinal_i = int(round(posSor[0])) if int(round(posSor[0])) < h else h-1
              Sor_posfinal_j = int(round(posSor[1])) if int(round(posSor[1])) < w else w-1
          else: 
              Tar_posfinal_i=Sor_posfinal_i=i
              Tar_posfinal_j = Sor_posfinal_j=j


          
          morphed_im[m,i,j,:] = (1-dissolve_frac[m])*im1[Tar_posfinal_i,Tar_posfinal_j, :]+dissolve_frac[m]*im2[Sor_posfinal_i,Sor_posfinal_j, :] ##disslove process

  morphed_im = np.array(morphed_im, dtype = np.uint8)
  return morphed_im