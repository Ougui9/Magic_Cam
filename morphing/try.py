from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from maskImage import maskImage
from seamlessCloningPoisson import seamlessCloningPoisson
import scipy.io

sIm = np.array(Image.open('./full/image%04d.jpg' % (1)))
mask = maskImage(sIm)
for i in range(60):
    sIm = np.array(Image.open('./full/image%04d.jpg' % (i)))
    tIm = np.array(Image.open('target.jpg'))
    offsetX = 0
    offsetY = 0

    # mask = maskImage(sIm)
    # scipy.io.savemat('mask.mat', mdict={'mask': mask})
    reIM = seamlessCloningPoisson(sIm, tIm, mask, offsetX, offsetY)

    j = Image.fromarray(reIM[:, :, :], mode='RGB')
    j.save("image%04d.jpg" % (i))

    # plt.imshow(reIM)
    # plt.show()
