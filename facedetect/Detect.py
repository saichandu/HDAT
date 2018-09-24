# -*- coding: utf-8 -*-
"""
Created on Sat Aug 25 13:33:05 2018

@author: saavvaru,harikkrishna,prmodi
"""

from configreader.Reader import Reader
import cv2,glob,os,time,random,shutil
from imutils.object_detection import non_max_suppression

class Detect(object):

    reader = Reader()
    webcamTmpPath = reader.fetchProperty("FolderStructure", "webcam.tmp.path");
    webcamFacesPath = reader.fetchProperty("FolderStructure", "webcam.faces.path");
    archivePath = reader.fetchProperty("FolderStructure", "faces.to.archive");
    imageWidth = reader.fetchProperty("ImageResolution", "image.width");
    imageHeight = reader.fetchProperty("ImageResolution", "image.height");
    
    #CASCADE="Face_cascade.xml"
    CASCADE = "haarcascade_profileface.xml"
    face_cascade = cv2.CascadeClassifier(os.getcwd() + "\\config\\" + CASCADE)
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    def detect_faces(self):
        for webcamDirectCapturedImg in glob.iglob(self.webcamTmpPath + "\\*.jpg"):
            
            image = cv2.imread(webcamDirectCapturedImg)
            
            frame_resized_grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)           
            
            faces = self.detect_face(frame_resized_grayscale)
            if len(faces) > 0:
                temp = 0
                #detected = False
                for xaxis,yaxis,width,height in faces:
                    #detected = True
                    sub_img=image[yaxis:yaxis+height,xaxis:xaxis+width]
                   
                    sub_img=cv2.resize(sub_img, (int(self.imageWidth), int(self.imageHeight)))
                    
                    os.chdir(self.webcamFacesPath)
                    timestamp = time.time()
                    timestamp = str(timestamp).replace(".","_")
                    if (temp == timestamp):
                        timestamp = timestamp + str(random.randint(1,10000))
                    temp = timestamp
                    #cv2.rectangle(image,(xaxis,yaxis),(xaxis+width,yaxis+height),(255, 255,0),2)
                    cv2.imwrite(timestamp+".jpg",sub_img)
            #if (detected == True):
                #shutil.move(webcamDirectCapturedImg,self.archivePath)
            shutil.move(webcamDirectCapturedImg,self.archivePath)
            
            
    def detect_face(self, frame):
    	"""
    	detect human faces in image using haar-cascade
    	Args:
    		frame:
    	Returns:
    	coordinates of detected faces
    	"""
    	faces = self.face_cascade.detectMultiScale(frame, 1.1, 2, 0, (20, 20))
    	return faces
    
    def detect_people(self, frame):
    	"""
    	detect humans using HOG descriptor
    	Args:
    		frame:
    	Returns:
    		processed frame
    	"""
    	(rects, weights) = self.hog.detectMultiScale(frame, winStride=(8, 8), padding=(16, 16), scale=1.06)
    	rects = non_max_suppression(rects, probs=None, overlapThresh=0.65)
    	return rects
    