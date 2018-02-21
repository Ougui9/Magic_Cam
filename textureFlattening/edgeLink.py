'''
  File name: edgeLink.py
  Author: Yilun Zhang
  Date created: 9.24.2017
'''

'''
  File clarification:
    Use hysteresis to link edges based on high and low magnitude thresholds
    - Input M: H x W logical map after non-max suppression
    - Input Mag: H x W matrix represents the magnitude of gradient
    - Input Ori: H x W matrix represents the orientation of gradient
    - Output E: H x W binary matrix represents the final canny edge detection map
'''

from math import pi
import numpy as np
from textureFlattening.helpers import smallAng
def edgeLink(M, Mag, Ori):
  # TODO: your code here
  thresh_l = 0.2   #low threshold ratio for Mag
  thresh_h = 0.35  #high threshold ratio for Mag
  angle_thre = pi / 180 * 25  # set threshold for angle similarity detection
  MagEdge =Mag*M   #obtain Edge magnitude
  H = len(M)
  W = len(M[0])

  StrongEdge = np.zeros([H, W])  # binary map for pixel whose magnitude larger than high threshold
  WeakEdge = np.zeros([H, W])



  low = thresh_l * np.amax(MagEdge)#low threshold for Mag
  high = thresh_h * np.amax(MagEdge)#high threshold for Mag

# calculate strong edge point map and weak point map
  for i in range(H):
    for j in range(W):
      StrongEdge[i, j] =1 if Mag[i, j] >= high else 0
      WeakEdge[i,j] = 1 if high>Mag[i, j] >=low else 0

  E = StrongEdge #strong points must be in the result map

  for i in range(H):
    for j in range(W):
      if StrongEdge[i, j]==1:
        list1 = [[i,j],] #define updatable loop list for multiple-end case

        for [m, n] in list1: #check nearby weak points

          if ((WeakEdge[m-1, n] == 1 and (smallAng(Ori[m,n],Ori[m-1,n])<=angle_thre))if m>0 else 0)and ([m-1,n] not in list1):
            E[m - 1, n] = 1
            WeakEdge[m-1, n] = 0  # sign checked weak point as 0 in weak point map
            list1.append([m-1,n])  # add a branch point to the list

          # Below is similar
          if ((WeakEdge[m + 1, n] == 1 and smallAng(Ori[m,n],Ori[m+1,n])<=angle_thre)if m<H-1 else 0)and ([m+1,n] not in list1):
            E[m + 1, n] = 1
            WeakEdge[m + 1, n] = 0
            list1.append([m + 1, n])
          if ((WeakEdge[m-1,n-1] == 1 and smallAng(Ori[m,n],Ori[m-1,n-1])<=angle_thre) if m>0 and n>0 else 0)and ([m-1,n-1] not in list1):
            E[m-1, n-1] = 1
            WeakEdge[m-1, n-1] =0
            list1.append([m - 1, n-1])
          if ((WeakEdge[m, n+1]==1 and smallAng(Ori[m,n],Ori[m,n+1])<=angle_thre)if n<(W-1) else 0)and ([m,n+1] not in list1):
            E[m, n + 1] = 1
            WeakEdge[m, n + 1] = 0
            list1.append([m, n+1])
          if ((WeakEdge[m-1, n+1] == 1 and smallAng(Ori[m,n],Ori[m-1,n+1])<=angle_thre) if m>0 and n<W-1 else 0)and ([m-1,n+1] not in list1):
            E[m - 1, n+1] = 1
            WeakEdge[m - 1, n + 1] = 0
            list1.append([m - 1, n+1])
          if ((WeakEdge[m+1, n+1] == 1 and smallAng(Ori[m,n],Ori[m+1,n+1])<=angle_thre) if m<H-1 and n<W-1 else 0)and ([m+1,n+1] not in list1):
            E[m+1, n+1] = 1
            WeakEdge[m +1, n + 1] = 0
            list1.append([m + 1, n+1])
          if ((WeakEdge[m+1, n-1] == 1 and smallAng(Ori[m,n],Ori[m+1,n-1])<=angle_thre) if m<H-1 and n>0 else 0)and ([m+1,n-1] not in list1):
            E[m + 1, n - 1] = 1
            WeakEdge[m+1, n-1] = 0
            list1.append([m + 1, n-1])
          if ((WeakEdge[m,n-1] == 1 and smallAng(Ori[m,n],Ori[m,n-1])<=angle_thre) if n>0 else 0)and ([m,n-1] not in list1):
            E[m, n - 1] = 1
            WeakEdge[m, n - 1] = 0
            list1.append([m, n-1])
  return E










