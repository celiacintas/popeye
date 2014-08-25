#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""In this example we can see how to call 
the s_search_single fuction of STASM from Python 
with a video and save the landmarks into txt"""

import cv2
import numpy as np
from popeye.dependencies import pystasm



FILENAME =  '/tmp/out.webm'

def video_config(FILENAME):
	"""Initialize video capture, pass filename by
	param jic that remove var and pass by argv"""

	cap = cv2.VideoCapture(FILENAME)
	while not cap.isOpened():
	    cap = cv2.VideoCapture(FILENAME)
	    cv2.waitKey(1000)
	    print "Wait for the header"
	pos_frame = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
	
	return cap, pos_frame

def main():
	mystasm = pystasm.STASM()
	cap, pos_frame = video_config(FILENAME)
	
	while True:
	    flag, frame = cap.read()
	    if flag:
	        # The frame is ready and already captured
	        # save a tmp file because pystasm receive by parameter a filename
	        filename = '/tmp/frame{}.jpg'.format(pos_frame)
	        cv2.imwrite(filename, frame)
	        # nasty fix .. pystasm should receive np array .. 
	        mylandmarks = mystasm.s_search_single(filename)
	        
	        # draw the landmarks
	        map(lambda p: cv2.circle(frame, (int(p[0]), int(p[1])), 5, (0,0,255), -1), mylandmarks)
	        cv2.imshow('video landmarks', frame)

	        #save to txt the landmarks of each frame 
	        np.savetxt('/tmp/frame{}.txt'.format(pos_frame), mylandmarks,  fmt='%4.4d', delimiter=" ")
	        pos_frame = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)

	    else:
	        # The next frame is not ready, so we try to read it again
	        cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, pos_frame-1)
	        print "frame is not ready"
	        cv2.waitKey(1000)

	    if cv2.waitKey(10) == 27:
	        break

	    if cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES) == cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT):
	        break
	
if __name__ == '__main__':
    main()
