
import numpy as np
import cv2 as cv

def auto_correspondences(im1, im2, face1, face2):
    #Good Features to Track detection + SIFT descriptor
    im1Gray = cv.cvtColor(im1, cv.COLOR_BGR2GRAY)
    im2Gray = cv.cvtColor(im2, cv.COLOR_BGR2GRAY)
#    im1Hue = cv.cvtColor(im1, cv.COLOR_BGR2HSV)
#    im2Hue = cv.cvtColor(im2, cv.COLOR_BGR2HSV)
#    im1Gray = im1Hue[..., 0]
#    im2Gray = im2Hue[..., 0]
    im1Gray = cv.GaussianBlur(im1Gray, (5, 5), 0.1)
    im2Gray = cv.GaussianBlur(im2Gray, (5, 5), 0.1)
    x1, y1 , w1, h1 = face1[0,1],face1[0,1],face1[0,2],face1[0,3]
    x2, y2, w2, h2 = face2[0,0], face2[0,1], face2[0,2], face2[0,3]

    corners1 = cv.goodFeaturesToTrack(im1Gray[y1:y1+h1, x1:x1+w1], maxCorners = 200, qualityLevel = 0.05, minDistance = 9)
#    corners1 = np.int0(corners1)
    kcorners1 = []
    corners2 = cv.goodFeaturesToTrack(im2Gray[y2:y2+h2, x2:x2+w2], maxCorners = 200, qualityLevel = 0.05, minDistance = 9)
#    corners2 = np.int0(corners2)
    kcorners2 = []

    for i in corners1:
        x, y = i.ravel()+face1[0,:2]
        kcorners1.append(cv.KeyPoint(x,y,32))
        
    for i in corners2:
        x, y = i.ravel()+face2[0,:2]
#        pt = cv.Point2f(x, y)
        kcorners2.append(cv.KeyPoint(x,y,32))
    
    for i in corners1:
        x,y = (i.ravel()+face1[0,:2]).astype(int)
#        cv.circle(im1,(x,y),3,255,-1)

#    cv.imshow('kp1', im1)
    
    for i in corners2:
        x,y = (i.ravel()+face2[0,:2]).astype(int)
#        cv.circle(im2,(x,y),3,255,-1)

#    cv.imshow('kp2', im2)
    
    sift = cv.xfeatures2d.SIFT_create(nfeatures = 4)
#    kcorners1, des1 = sift.detectAndCompute(im1Gray, None)
#    kcorners2, des2 = sift.detectAndCompute(im2Gray, None)
    
    kcorners1, des1 = sift.compute(im1Gray, kcorners1)
    kcorners2, des2 = sift.compute(im2Gray, kcorners2)

#    plt.imshow(im3,),plt.show()

#    im1c=cv.drawKeypoints(im1,kcorners1,outImage = None, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
#    im2c=cv.drawKeypoints(im2,kcorners2,outImage = None, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
#    cv.imshow('kp1', im1c)
#    cv.imshow('kp2', im2c)
    
    bf = cv.BFMatcher()
    matchesF = bf.knnMatch(des1, des2, k = 1)
    
#    good = []
#    for m,n in matches:
#        if m.distance < 0.99*n.distance:
#            good.append([m])

    #cv2.drawMatchesKnn expects list of lists as matches.
#    im3 = np.zeros_like(im1)
#    im3 = cv.drawMatchesKnn(im1,kcorners1,im2,kcorners2,matchesF,flags=2, outImg = None)
#    cv.imshow('match', im3)
#     print(len(matchesF))
    m_forward = np.zeros((len(matchesF), 2))
    
    for i in range(len(matchesF)):
        m_forward[i, 0] = matchesF[i][0].queryIdx
        m_forward[i, 1] = matchesF[i][0].trainIdx
#        print kcorners2[np.int32(m_forward[i, 1])].pt

    matchesB = bf.knnMatch(des2, des1, k = 1)
    
#    good = []
#    for m,n in matches:
#        if m.distance < 0.99*n.distance:
#            good.append([m])

    #cv2.drawMatchesKnn expects list of lists as matches.
#    im3 = np.zeros_like(im1)
#    im4 = cv.drawMatchesKnn(im2,kcorners2,im1,kcorners1,matchesB,flags=2, outImg = None)
#    cv.imshow('match2', im4)
#     print(len(matchesB))
    m_backward = np.zeros((len(matchesB), 2))
    for i in range(len(matchesB)):
        m_backward[i, 0] = matchesB[i][0].trainIdx
#        print kcorners2[np.int32(m_backward[i, 0])].pt
        m_backward[i, 1] = matchesB[i][0].queryIdx

    return kcorners1, kcorners2, m_forward, m_backward, matchesF, matchesB