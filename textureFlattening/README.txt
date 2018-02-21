INTRODUCTION
===========================================
NAME: CANNY EDGE DECTECION
DATE: 9/24/2017
AUTHOR: YILUN ZHANG
HAOYUAN ZHANG(FOR START CODE)
===========================================

SYSTEM REQUIREMENT
===========================================
Python 3/2 (actually written in Python 3, but I have change all print expression into Python2 style)
Numpy
Scipy
matplotlib
PIL
math
===========================================

FILE LIST
===========================================
1. cannyEdge.py (main, run the proj from here)
2. edgeLink.py
3. findDerivatives.py
4. helpers.py
5. nonMaxSup.py
6. Test_script.py
7. utils.py
8. canny_dataset(folder for testing images)
9. result(folder for result images)
===========================================


Intro of functions
===========================================
All detailed info for the program is in code comments.

findDerivatives.py
1. generate 2d Gaussian filter (11*11).
2. calculate gradients of G
3. convolve image with gradients
4. calculate magtitude of Derivatives
5. calculate the Orientation

nonMaxSup.py
1. Divide 360 degrees around every pixel into 8 parts with each one of 45 degrees. 
2. In each part, interpolate to obtain the magnitude of virtual points which are at the orientation of the target point and the opposite direction. 
3. Compare the magnitude of them with that of the target point. If the later is not larger or equal to the former, set the later to zero.

edgeLink.py
1.  calculate strong edge point map and weak point map
2.  for every strong edgepoint, check whether there are nearby weak points (8 connectivity here)
P.S. In Step 2, I have set a updatable list for looping to make sure the case of "multiple nearby weak points" work well.

===========================================


Friendly booklet for Running the code
===========================================
First, for obtaining best effect for every test pictures, I reset different thresholds to process different pics.(BTW. For this problem, I have checked some info online and apply a adaptive threshold function to the original code. Its applicaiton is in another folder named CH1.) 

The thresholds (ration)for best results are as follows.(The angle threshold is set to 25 degrees for all images.)

118035.jpg: High: 0.1 Low:0.02
135069.jpg: High: 0.3 Low:0.28
16068.jpg: High: 0.27 Low:0.23
189080.jpg: High: 0.21 Low:0.12
201080.jpg: High: 0.25 Low:0.2
20177.jpg: High: 0.27 Low:0.23
22013.jpg: High: 0.27 Low:0.10
3096.jpg: High: 0.27 Low:0.17
48017.jpg: High: 0.27 Low:0.15
55067.jpg: High: 0.18 Low:0.07
86000.jpg: High: 0.2 Low:0.15
I1.jpg: High: 0.2 Low:0.05