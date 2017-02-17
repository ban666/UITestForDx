# -*- coding: utf-8 -*-
__author__ = 'liaoben'

from elements_id import *
from appium_lib import element_exsist,exception_handler
from appium import webdriver
import threading
from time import sleep
from Queue import Queue

class Video:

    def __init__(self,driver):
        self.driver = driver
        self.video_time = ''

    #@exception_handler
    def get_video_time(self):
        try:
            if not element_exsist(self.driver,'id',VIDEO_TIME):
                print 'click'
                self.driver.find_element_by_id(VIDEO_ITEM).click()
            t = self.driver.find_element_by_id(VIDEO_TIME).text
            print t
            self.video_time = t
            return True
        except Exception,e:
            pass
        return False

    def get_video_time2(self):
        while self.get_video_time() == False:
            sleep(0.01)

    def get_video_time3(self):
        try:
            if not element_exsist(self.driver,'id',VIDEO_TIME):
                self.driver.find_element_by_id(VIDEO_ITEM).click()
            t = self.driver.find_elements_by_class_name('android.support.v7.widget.AppCompatTextView')
            for i in t:
                print i.text,i._id
            return False
        except Exception,e:
            print e.__repr__()
            pass
        return False

    @exception_handler
    def start_pause_video(self):
        if not element_exsist(self.driver,'id',VIDEO_TIME):
            self.driver.find_element_by_id(VIDEO_ITEM).click()
        self.driver.find_element_by_id(VIDEO_START_PAUSE).click()
        return True