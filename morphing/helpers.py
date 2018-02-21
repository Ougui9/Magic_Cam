'''
function name:
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mplPath


class drawMask(object):

	def __init__(self, img):
		self.img = img
		self.fig = plt.gcf()
		self.ax = plt.gca()
		self.previous_point = None
		self.start_point = None
		self.end_point = None
		self.fig.canvas.mpl_connect('motion_notify_event', self.motion_notify_event)
		self.fig.canvas.mpl_connect('button_press_event', self.button_press_event)
		plt.show()

	def button_press_event(self, event):
		if event.inaxes:
			x, y = event.xdata, event.ydata
			if event.button == 1:
				if self.start_point == None:
					self.start_point = [x,y]
					self.previous_point =  self.start_point
					self.x_point=[x]
					self.y_point=[y]
					self.line = plt.Line2D([x, x],[y, y], marker = 'o')
					self.ax.add_line(self.line)
					self.fig.canvas.draw()
				else:
					self.previous_point = [x,y]
					self.x_point.append(x)
					self.y_point.append(y)
					self.line = plt.Line2D([self.previous_point[0], x],[self.previous_point[1], y],marker = 'o')
					event.inaxes.add_line(self.line)
					self.fig.canvas.draw()
			elif (event.button == 3):
				self.line.set_data([self.previous_point[0],self.start_point[0]],
								   [self.previous_point[1],self.start_point[1]])
				self.ax.add_line(self.line)
				self.fig.canvas.draw()
				self.line = None
				plt.close(self.fig)

	def motion_notify_event(self, event):
		if event.inaxes:
			x, y = event.xdata, event.ydata
			if (event.button == None) and self.start_point != None:
				self.line.set_data([self.previous_point[0], x],
									[self.previous_point[1], y])
				self.fig.canvas.draw()

	def draw_mask(self):
		img_h = self.img.shape[0]
		img_w = self.img.shape[1]
		mesh_x, mesh_y = np.meshgrid(np.arange(img_w),np.arange(img_h))
		point = np.zeros((mesh_x.size,2))
		point[:,0] = mesh_x.flatten()
		point[:,1] = mesh_y.flatten()

		poly_point = np.zeros((len(self.x_point),2))

		poly_point[:,0] = np.array(self.x_point)
		poly_point[:,1] = np.array(self.y_point)
		poly_path = mplPath.Path(poly_point)
		poly_mask = poly_path.contains_points(point).reshape(img_h,img_w)
		return poly_mask

	def get_bbox(self, mask):
		coor = np.argwhere(mask)
		h_min = np.min(coor[:,0])
		h_max = np.max(coor[:,0])
		w_min = np.min(coor[:,1])
		w_max = np.max(coor[:,1])

		return [w_min, h_min, w_max, h_max]



def draw_mask(img):
	plt.imshow(img)
	draw = drawMask(img)
	mask = draw.draw_mask()
	bbox = draw.get_bbox(mask)
	plt.imshow(mask)
	plt.show()

	return mask.astype(int) , bbox

'''
  File name: helpers.py
  Author:
  Date created:
'''

'''
  File clarification:
    Helpers file that contributes the project
    You can design any helper function in this file to improve algorithm
'''
import numpy as np
import scipy.misc
import matplotlib.pyplot as plt
import math
'''
function name: cpselect
 Author: Xiao Zhang
'''
class cpselect_recorder:
    def __init__(self, img1, img2):

        fig, (self.Ax0, self.Ax1) = plt.subplots(1, 2, figsize=(20, 20))

        self.Ax0.imshow(img1)
        self.Ax0.axis('off')

        self.Ax1.imshow(img2)
        self.Ax1.axis('off')

        fig.canvas.mpl_connect('button_press_event', self)
        self.left_x = []
        self.left_y = []
        self.right_x = []
        self.right_y = []

    def __call__(self, event):
        circle = plt.Circle((event.xdata, event.ydata), color='r')
        if event.inaxes == self.Ax0:
            self.left_x.append(event.xdata)
            self.left_y.append(event.ydata)
            self.Ax0.add_artist(circle)
            plt.show()
        elif event.inaxes == self.Ax1:
            self.right_x.append(event.xdata)
            self.right_y.append(event.ydata)
            self.Ax1.add_artist(circle)
            plt.show()


def cpselect(img1, img2):
    resize_img1 = scipy.misc.imresize(img1, [300, 300])
    resize_img2 = scipy.misc.imresize(img2, [300, 300])
    point = cpselect_recorder(resize_img1, resize_img2)
    plt.show()
    point_left = np.concatenate([(np.array(point.left_x) * img1.shape[1] * 1.0 / 300)[..., np.newaxis], \
                                 (np.array(point.left_y) * img1.shape[0] * 1.0 / 300)[..., np.newaxis]], axis=1)
    point_right = np.concatenate([(np.array(point.right_x) * img2.shape[1] * 1.0 / 300)[..., np.newaxis], \
                                  (np.array(point.right_y) * img2.shape[0] * 1.0 / 300)[..., np.newaxis]], axis=1)
    plt.scatter(point_left[:, 0], point_left[:, 1])
    plt.imshow(img1)
    plt.show()
    plt.scatter(point_right[:, 0], point_right[:, 1])
    plt.imshow(img2)
    plt.show()
    return point_left, point_right

'''
function name: switch the Axis value
Author: Yilun Zhang
'''


def switchAxis(xx):
    return np.asarray([xx[1],xx[0]])


'''
function name: set some boundary point for forming triangles
Author: Yilun Zhang
'''

def BPts(h,w):
    h_s = np.arange(0, h, h/10.0)
    w_s = np.arange(0, w, w/10.0)
    b_pts = np.zeros([40,2])
    b_pts[0:10,0] = w_s.copy()
    b_pts[10:20, 0] = w_s.copy()
    b_pts[10:20,1] = h-1
    b_pts[20:30,1] = np.append(h_s[1:10],h-1)
    b_pts[30:40, 1] = np.append(h_s[1:10],h-1)
    b_pts[30:40, 0] = w-1

    return b_pts

def Udistance(a_pos,b_pos):

    r_square =(a_pos[0] - b_pos[0])**2+(a_pos[1]-b_pos[1])**2
    return -r_square*math.log(r_square)

def tps(a1,ax,ay,w, pos, pts):
    u = 0
    # for i in range(len(pts)):
    #     u += w[i]*Udistance(pts[i],pos) if not np.array_equal(pts[i],pos) else 0
    # f = a1+ax*pos[0]+ay*pos[1] + u
    # return f
    numPixel=len(pos)
    Pt= np.zeros((len(pts), numPixel, 2))
    # re = np.zeros((len(pos),1))
    u = np.zeros((len(pos), 1))
    for i in range(numPixel):
        Pt[:,i,:] = pts.copy()
    for m in range(len(pts)):
        sqSum = np.square(Pt[m,:,:]-pos[:,:])
        r = sqSum[:,0]+sqSum[:,1]
        r0=np.where(r==0)[0]
        for k in r0:
            r[k]=1
        u[:,0]+= -w[m]*np.square(r)*(np.log(r))
    u[:,0] += a1+ax*pos[:,0]+ay*pos[:, 1]
    return u



def round2coor(x,y,h,w):
    x = np.around(x, decimals=1)
    y = np.around(y, decimals=1)

    # x = h-1 if x>h-1 else x
    # x = 0 if x<0 else x
    # y = w - 1 if y > w - 1 else y
    # y = 0 if y < 0 else y
    return np.array(x,dtype=int),np.array(y,dtype=int)
