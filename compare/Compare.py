# -*- coding: utf-8 -*-
"""
Created on Sat Aug 25 13:33:05 2018

@author: saavvaru,harikkrishna,prmodi
"""

from configreader.Reader import Reader
import glob,cv2,shutil
from skimage.measure import compare_ssim 

class Compare(object):
    
    reader = Reader()
    
    #read webcam path
    webcamPath = reader.fetchProperty("FolderStructure", "webcam.faces.path");
    saveImagePath = reader.fetchProperty("FolderStructure", "saved.images.path");
    archivePath = reader.fetchProperty("FolderStructure", "faces.to.archive");
    reportPath = reader.fetchProperty("FolderStructure", "faces.to.report");
    frequency = reader.fetchProperty("OtherConfig", "appear.frequency");
    scoreDefined = reader.fetchProperty("OtherConfig", "match.score");
    
    def compareImages(self):
    
        for incomingImage in glob.iglob(self.webcamPath + "\\*.jpg"):
            saveToDB = True
            reported = False
            imageA = cv2.imread(incomingImage)
            for savedImage in glob.iglob(self.saveImagePath + "\\*.jpg"):
                
                imageB = cv2.imread(savedImage)
                
                # convert the images to grayscale
                grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
                grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
                
                # compute the Structural Similarity Index (SSIM) between the two
                # images, ensuring that the difference image is returned
                (score, diff) = compare_ssim(grayA, grayB, full=True)
                diff = (diff * 255).astype("uint8")
                
                print ("Incomeing Image: " + incomingImage)
                print ("Saved Image: " + savedImage)
                print("SSIM: {}".format(score))
                
                #To do :: we need to write code to compare timestamp also
                if score > float(self.scoreDefined):
                    print ("\n\nImage Matched")
                    saveToDB = False
                    
                    timestamp1 = float(incomingImage.split(".jpg")[0].split("\\")[-1].replace("_","."))
                    timestamp2 = float(savedImage.split(".jpg")[0].split("\\")[-1].replace("_","."))
                    
                    #print "Timestamp of incoming image " + str(timestamp1)
                    #print "Timestamp of saved image " + str(timestamp2)
                    
                    print (timestamp1 - timestamp2)
                    print (self.frequency)
                    
                    if (timestamp1 - timestamp2) > float(self.frequency):
                        reported = True
                        print ("Report")
                        shutil.move(incomingImage, self.reportPath)
                        #To do :: we need to integrate with notification services
                        break
            if saveToDB == True:
                print ("New Image")
                image=incomingImage.split("\\")
               
                cv2.imwrite(self.saveImagePath + "\\" + image[-1], imageA)
            if (reported == False):
                shutil.move(incomingImage, self.archivePath)
        