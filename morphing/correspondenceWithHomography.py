

import numpy as np
import cv2 as cv

def correspondenceWithHomography(corners1, corners2, match, mask, M):
    #Scan over the corners list, keep the matches within the mask
    #For other keypoints, apply a homogeneous transporm
    matched = np.zeros([len(corners2)])
    length = np.sum(mask)
    finalMatch1 = np.zeros([length, 2])
    finalMatch2 = np.zeros_like(finalMatch1)
    q = 0
    for i in range(len(mask)):
        q1 = match[i][0].queryIdx
        q2 = match[i][0].trainIdx
        if mask[i] == 1 and matched[q2] == 0:
            finalMatch1[q, 0] = corners1[q1].pt[0]
            finalMatch1[q, 1] = corners1[q1].pt[1]
            finalMatch2[q, 0] = corners2[q2].pt[0]
            finalMatch2[q, 1] = corners2[q2].pt[1]
            matched[q2] = 1
            q += 1
        elif mask[i] == 1 :
            pt1 = corners1[q1].pt
            ptHomo = np.array([pt1[0], pt1[1], 1])
            ptNew = M.dot(ptHomo)
            ptNew = ptNew / ptNew[2]
            finalMatch1[q, 0] = corners1[q1].pt[0]
            finalMatch1[q, 1] = corners1[q1].pt[1]
            finalMatch2[q, 0] = ptNew[0]
            finalMatch2[q, 1] = ptNew[1]
            q += 1
            
    return finalMatch1, finalMatch2