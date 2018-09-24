# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 00:17:02 2018

@author: saavvaru
"""
import os, fnmatch

class FileUtil():
    
    @staticmethod
    def searchNCreateFolder(directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
            else:
                print("Directory: " + directory + " already exists")
        except OSError:
            print ('Error: Creating directory. ' +  directory)
            
            
    def find_files(directory, pattern):
        for root, dirs, files in os.walk(directory):
            for basename in files:
                if fnmatch.fnmatch(basename, pattern):
                    filename = os.path.join(root, basename)
                    yield filename