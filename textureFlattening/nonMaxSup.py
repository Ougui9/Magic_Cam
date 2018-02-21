'''
  File name: nonMaxSup.py
  Author: Yilun Zhang
  Date created:
'''

'''
  File clarification:
    Find local maximum edge pixel using NMS along the line of the gradient
    - Input Mag: H x W matrix represents the magnitude of derivatives
    - Input Ori: H x W matrix represents the orientation of derivatives
    - Output M: H x W binary matrix represents the edge map after non-maximum suppression
'''
from math import  pi
import numpy as np
def nonMaxSup(Mag, Ori):
  # TODO: your code here
  M = np.zeros((len(Mag),len(Mag[0])))
  for i in range(len(Mag)):
      for j in range(len(Mag[0])):
          # orientaion in pi/4 to pi/2 and its symmetrical part about the [i,j]
          if (pi/2 > Ori[i,j] > pi/4) or (-pi/2 > Ori[i,j] > -3*pi/4):
              # calculate the absolut angle between ori and vertical axis
              yaw = np.tan(abs(pi/2-abs(Ori[i, j])))
              # interpolate point pt1 if existing
              pt1 = yaw*(Mag[i-1, j+1]-Mag[i-1, j])+Mag[i-1, j]if (i > 0 and j< (len(Mag[0])-1)) else 0
              # interpolate point pt2 if existing
              pt2 = yaw*(Mag[i+1, j-1]-Mag[i+1, j])+Mag[i+1, j]if ((i<len(Mag)-1) and j>0) else 0
              #check if Mag[i,j] is max among at most 3 points
              M[i, j] = 1 if Mag[i, j] >= pt1 and Mag[i, j] >= pt2 else 0


          # similarly below. the only difference is orientaion section
          elif (3*pi/4<Ori[i,j]<=pi/2)or(-pi/4>Ori[i, j]>=-pi/2):  #orientaion in pi/2 to 3*pi/4 and its symmetrical part about the [i,j]
              yaw = np.tan(abs(pi/2-abs(Ori[i, j])))  #calculate the absolut angle between ori and vertical axis
              pt1 = yaw*(Mag[i-1, j-1]-Mag[i-1, j])+Mag[i-1, j]if (i>0 and j>0) else 0   #interpolate point pt1 if existing
              pt2 = yaw*(Mag[i+1, j+1]-Mag[i+1, j])+Mag[i+1, j]if ((i<len(Mag)-1) and j<len(Mag[0])-1) else 0  #interpolate point pt2 if existing
              M[i, j] = 1 if Mag[i,j]>=pt1 and Mag[i,j]>=pt2 else 0  #check if Mag[i,j] is max among at most 3 points

          elif (pi > Ori[i, j] >= 3*pi/4) or (-pi/4 >= Ori[i, j] > 0.):  #orientaion in 3*pi/4 to pi and its symmetrical part about the [i,j]
              yaw = np.tan((pi-Ori[i, j]) if Ori[i, j] > 0 else abs(Ori[i, j]))  #calculate the absolut angle between ori and horizontal axis
              pt1 = yaw*(Mag[i-1, j-1]-Mag[i, j-1])+Mag[i, j-1]if (i>0 and j>0) else 0  #interpolate point pt1 if existing
              pt2 = yaw*(Mag[i+1, j+1]-Mag[i, j+1])+Mag[i, j+1]if ((i<len(Mag)-1) and j<(len(Mag[0])-1)) else 0  #interpolate point pt2 if existing
              M[i,j] = 1 if Mag[i,j]>=pt1 and Mag[i,j]>=pt2 else 0  #check if Mag[i,j] is max among at most 3 points

          elif (pi/4 >= Ori[i, j] >= 0) or (-3*pi/4 >= Ori[i, j] >= -pi):  #orientaion in 0 to pi/4 and its symmetrical part about the [i,j]
              yaw = np.tan((pi + Ori[i, j]) if Ori[i, j] < 0 else Ori[i, j])  #calculate the absolut angle between ori and horizontal axis
              pt1 = yaw * (Mag[i + 1, j + 1] - Mag[i, j + 1]) + Mag[i, j + 1]if (i < (len(Mag)-1) and j < (len(Mag[0])-1)) else 0  #interpolate point pt1 if existing
              pt2 = yaw * (Mag[i - 1, j - 1] - Mag[i, j - 1]) + Mag[i, j - 1]if (i > 0 and j >0) else 0  #interpolate point pt2 if existing
              M[i, j] = 1 if Mag[i, j] >= pt1 and Mag[i, j] >= pt2 else 0  #check if Mag[i,j] is max among at most 3 points
  return M