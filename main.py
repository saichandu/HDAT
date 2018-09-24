# -*- coding: utf-8 -*-

from webcam.Webcam import Webcam
from facedetect.Detect import Detect
from compare.Compare import Compare
import cv2


def main():
    previous_frame = None
    while True:
     webcam = Webcam()
     frame_resized_grayscale = webcam.captureImage()
     
     if previous_frame != None:
         min_area=(3000/800)*frame_resized_grayscale.shape[1]
         temp=background_subtraction(previous_frame, frame_resized_grayscale, min_area)
         if temp==1:
             detect = Detect()
             detect.detect_faces()
         else:
             print("Frame is skipped")
         
         previous_frame = frame_resized_grayscale
     else:
         detect = Detect()
         detect.detect_faces()
     compare = Compare()
     compare.compareImages()
     
     key = cv2.waitKey(1) & 0xFF
     if key == ord("q"):
         break


if __name__ == "__main__":
    main()
    
def background_subtraction(previous_frame, frame_resized_grayscale, min_area):
	"""
	This function returns 1 for the frames in which the area 
	after subtraction with previous frame is greater than minimum area
	defined. 
	Thus expensive computation of human detection face detection 
	and face recognition is not done on all the frames.
	Only the frames undergoing significant amount of change (which is controlled min_area)
	are processed for detection and recognition.
	"""
	frameDelta = cv2.absdiff(previous_frame, frame_resized_grayscale)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
	thresh = cv2.dilate(thresh, None, iterations=2)
	im2, cnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	temp=0
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) > min_area:
			temp=1
	return temp