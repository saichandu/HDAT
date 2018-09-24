# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 00:37:06 2018

@author: saavvaru
"""

import os,configparser

class Reader(object):
    
    config = configparser.RawConfigParser()    
    config.read(os.getcwd() + '/config/ApplicationConfig.properties')
    print("Application Configuration Loaded...")
        
    def fetchProperty(self, section, propertyName):
        
        return self.config.get(section, propertyName)