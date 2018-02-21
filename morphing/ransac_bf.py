

import cv2 as cv
import numpy as np

def RANSAC_BF(kC1, kC2, mnF, mnB, im1, im2):
    MIN_MATCH_COUNT = 10
    mF = []
    mB = []
    for m in mnF:
        mF.append(m[0])
    for m in mnB:
        mB.append(m[0])
    
    if len(mF)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kC1[m.queryIdx].pt for m in mF ]).reshape(-1,1,2)
        dst_pts = np.float32([ kC2[m.trainIdx].pt for m in mF ]).reshape(-1,1,2)
    
        MF, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC,10.0)
        matchesMaskF = mask.ravel().tolist()
    
        h,w,d = im1.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv.perspectiveTransform(pts,MF)
    
#        im2 = cv.polylines(im2,[np.int32(dst)],True,255,3, cv.LINE_AA)
    
    else:
        print ("Not enough matches are found - %d/%d" % (len(mF),MIN_MATCH_COUNT))
        matchesMaskF = None

#    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
#                   singlePointColor = None,
#                   matchesMask = matchesMaskF, # draw only inliers
#                   flags = 2)

#    im3 = cv.drawMatches(im1,kC1,im2,kC2,mF,None,**draw_params)    
#    cv.imshow('RANSAC_F', im3)
    
    if len(mB)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kC1[m.trainIdx].pt for m in mB ]).reshape(-1,1,2)
        dst_pts = np.float32([ kC2[m.queryIdx].pt for m in mB ]).reshape(-1,1,2)
    
        MB, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC,10.0)
#        print M
        matchesMaskB = mask.ravel().tolist()
    
        h,w,d = im1.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv.perspectiveTransform(pts,MB)
    
#        im2 = cv.polylines(im2,[np.int32(dst)],True,255,3, cv.LINE_AA)
    
    else:
        print ("Not enough matches are found - %d/%d" % (len(mB),MIN_MATCH_COUNT))
        matchesMaskB = None
    
#    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
#                   singlePointColor = None,
#                   matchesMask = matchesMaskB, # draw only inliers
#                   flags = 2)
        
#    im3 = cv.drawMatches(im2,kC2,im1,kC1,mB,None,**draw_params)    
#    cv.imshow('RANSAC_B', im3)
    
    return matchesMaskF, matchesMaskB, MF, MB