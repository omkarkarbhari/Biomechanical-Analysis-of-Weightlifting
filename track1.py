import cv2
import numpy as np

ix, iy, k = 200,200,1
def onMouse(event, x, y, flag, param):
	global ix,iy,k
	if event == cv2.EVENT_LBUTTONDOWN:
		ix,iy = x,y 
		k = -1


def run(filename):
	cv2.namedWindow("window")
	cv2.setMouseCallback("window", onMouse)
	cap = cv2.VideoCapture(filename)
	cnt=0
	while True:
		_, frm = cap.read()
		cv2.imshow("window", frm)
		if cv2.waitKey(1) == 27 or k == -1:
			old_gray = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)
			cv2.destroyAllWindows()
			break

	old_pts = np.array([[ix,iy]], dtype="float32").reshape(-1,1,2)
	mask = np.zeros_like(frm)

	while True:
		_, frame2 = cap.read()

		new_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

		new_pts,status,err = cv2.calcOpticalFlowPyrLK(old_gray, 
							new_gray, 
							old_pts, 
							None, maxLevel=1,
							criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
															15, 0.08))

		cv2.circle(mask, (int(new_pts.ravel()[0]) ,int(new_pts.ravel()[1])), 2, (0,0,255), 2)
		combined = cv2.addWeighted(frame2, 0.7, mask, 0.3, 0.1)

		cv2.imshow("new win", mask)
		cv2.imshow("wind", combined)

		old_gray = new_gray.copy()
		old_pts = new_pts.copy()

		if cv2.waitKey(1) == 27:
			cv2.imwrite('barbell.jpg',combined)
			cv2.imshow('track',combined)
			cv2.waitKey(0)
			cap.release()
			cv2.destroyAllWindows()
			break

'''import numpy as np
import cv2 as cv
import argparse

#parser = argparse.ArgumentParser(description='This sample demonstrates Lucas-Kanade Optical Flow calculation. \
                                              #The example file can be downloaded from: \
                                              #https://www.bogotobogo.com/python/OpenCV_Python/images/mean_shift_tracking/slow_traffic_small.mp4')
#parser.add_argument('image', type=str, help='path to image file')
#args = parser.parse_args()

cap = cv.VideoCapture('C:\\Users\\sohil\Downloads\\check123.mp4')

# params for ShiTomasi corner detection
feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )

# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (15, 15),
                  maxLevel = 2,
                  criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

# Create some random colors
color = np.random.randint(0, 255, (100, 3))

# Take first frame and find corners in it
ret, old_frame = cap.read()
old_gray = cv.cvtColor(old_frame, cv.COLOR_BGR2GRAY)
p0 = cv.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

# Create a mask image for drawing purposes
mask = np.zeros_like(old_frame)

while(1):
	ret, frame = cap.read()
	if not ret:
		print('No frames grabbed!')
		break
	frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # calculate optical flow
	p1, st, err = cv.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

    # Select good points
	if p1 is not None:
		good_new = p1[st==1]
		good_old = p0[st==1]

    # draw the tracks
	for i, (new, old) in enumerate(zip(good_new, good_old)):
		a, b = new.ravel()
		c, d = old.ravel()
		mask = cv.line(mask, (int(a), int(b)), (int(c), int(d)), color[i].tolist(), 2)
		frame = cv.circle(frame, (int(a), int(b)), 5, color[i].tolist(), -1)
		img = cv.add(frame, mask)

	cv.imshow('frame', img)
	k = cv.waitKey(30) & 0xff
	if k == 27:
		break

    # Now update the previous frame and previous points
	old_gray = frame_gray.copy()
	p0 = good_new.reshape(-1, 1, 2)

cv.destroyAllWindows()'''