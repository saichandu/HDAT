# -*- coding: utf-8 -*-
"""
Created on Sat Aug 25 14:18:02 2018

@author: saavvaru, harikkrishna, prmodi
"""

from configreader.Reader import Reader
import cv2,os,imutils
from random import randint

class Webcam(object):
    reader = Reader()
    webcamTmpPath = reader.fetchProperty("FolderStructure", "webcam.tmp.path");
    
    def captureImage(self):   
        camera = cv2.VideoCapture(0)
       
        tmp,image = camera.read()
        
        frame_resized = imutils.resize(image, width=min(800, image.shape[1]))
        frame_resized_grayscale = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
                 
        cv2.imwrite(os.path.join(self.webcamTmpPath + "\\" , str("Img") + str(randint(0,10000)) + str(".jpg")), frame_resized)
            
        camera.release()
        return frame_resized_grayscale