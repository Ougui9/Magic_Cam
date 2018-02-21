import numpy as np
import cv2
from morphing.auto_correspondences import auto_correspondences
from morphing.ransac_bf import RANSAC_BF
from morphing.correspondenceWithHomography import correspondenceWithHomography
from morphing.helpers import BPts

#Only keep correspondences that appears in both matching direction
#Too strong. Alternate: do a distance check
def backwardForward(mF, mB):
    nF, dF = mF.shape
    q = []
    for i in range(nF):
        p1 = mF[i, 0]
        p2 = mF[i, 1]
        if mB[np.int32(p2), 0] == p1:
            q.append([cv2.DMatch(np.int32(p1), np.int32(p2), 0)])
    
    return q



def faceBBox(source, target):
    face_cascade = cv2.CascadeClassifier('./morphing/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('./morphing/haarcascade_eye.xml')
    
    faces_s = face_cascade.detectMultiScale(source, 1.3, 5)
    faces_t = face_cascade.detectMultiScale(target, 1.3, 5)
    
    for (x,y,w,h) in faces_s:
        roi_gray = source[y:y+h, x:x+w]
        eye_s = eye_cascade.detectMultiScale(roi_gray)
    
    for (x,y,w,h) in faces_t:
        roi_gray = source[y:y+h, x:x+w]
        eye_t = eye_cascade.detectMultiScale(roi_gray)
#    print 'face detection finished'
    return faces_s, faces_t, eye_s, eye_t

def featureMatch(img1, img2, faces_s, faces_t):
    kcorners1, kcorners2, mF, mB, mcF, mcB = auto_correspondences(img1, img2, faces_s, faces_t)
    # print len(kcorners1)
#    q = backwardForward(mF, mB)
    
#    im4 = cv2.drawMatchesKnn(img1,kcorners1,img2,kcorners2,q,flags=2, outImg = None)
#    cv2.imshow('match12', im4)
    
    mMF, mMB, MF, MB = RANSAC_BF(kcorners1, kcorners2, mcF, mcB, img1, img2)
    featureMatch1, featureMatch2 = correspondenceWithHomography(kcorners1, kcorners2, mcF, mMF, MF)
    
    H, W, d = img1.shape
    h_s = faces_s[0,3]
    w_s = faces_s[0,2]
    h_t = faces_t[0,3]
    w_t = faces_t[0,2]
    finalMatch1 = np.r_['0, 2', featureMatch1, BPts(H, W), BPts(h_s, w_s) + np.array([faces_s[0,1], faces_s[0,0]])]
    finalMatch2 = np.r_['0, 2', featureMatch2, BPts(H, W), BPts(h_t, w_t) + np.array([faces_t[0,1], faces_t[0,0]])]
#    finalMatch1 = np.r_['0, 2', BPts(H, W), BPts(h_s, w_s) + np.array([faces_s[0,1], faces_s[0,0]])]
#    finalMatch2 = np.r_['0, 2', BPts(H, W), BPts(h_t, w_t) + np.array([faces_t[0,1], faces_t[0,0]])]
    
    return finalMatch1, finalMatch2

#if cv2.waitKey():
#    cv2.destroyAllWindows()
    