# -*- coding: utf-8 -*-
__author__ = 'liaoben'

import sys
from appium import webdriver
from time import sleep
import unittest
from random import randint
sys.path.append('../../Lib')
import time
import os
from appium_lib import *
from dx_action import *
from ui_comment import *
from ChnlRequest import ChnlRequest
from DbLib import DbLib
from config import *
from loglib import log

from elements_id import *
from common import exception_handler,get_now
from screenshot import Appium_Extend
from ui_video import Video
class PlayPauseTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.mode = MODE
        self.db = DbLib()
        #self.api = ChnlRequest(self.mode)
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        start_to_index(self.driver,self.mode)

    def tearDown(self):
        print 'Test End...................................'
        try:
             self.tsl.set_tc_status(self.case_id,self.result,self.msg)
             self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self,article):
        step = 1

        #音频详情页播放时验证通知栏
        get_to_article_by_search(self.driver,article,self.mode)
        sleep(WAIT_TIME)
        #print self.driver.contexts
        def get_video_time():
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
        def get_video_time():
            try:
                el = self.driver.find_element_by_id(VIDEO_TIME).text
                print el
                self.driver.find_element_by_id(VIDEO_ROTATE).click()
            except:
                print 'click'
                self.driver.find_element_by_id(VIDEO_ITEM).click()
            return False
        for i in range(10):
            get_video_time()
        # video = Video(self.driver)
        # video.get_video_time2()
        #
        # self.driver.find_element_by_id(VIDEO_START_PAUSE).click()
        # print video.get_video_time()
        # sleep(10)
        # print video.get_video_time()
        #
        # progress = self.driver.find_element_by_id(AUDIO_AUDIO_PROGRESS)
        # play_time = self.driver.find_element_by_id(AUDIO_PLAY_TIME)
        # all_time = self.driver.find_element_by_id(AUDIO_ALL_TIME).text
        # self.driver.find_element_by_id(AUDIO_PAUSE).click()
        # back(self.driver)
        # sleep(WAIT_TIME)
        # slide_down(self.driver)
        # assert self.driver.find_element_by_id(PAGEVIEW_COUNT).text+u'播放' == u'23播放'
        # print u'Step %s:播放数增加测试：OK' % (str(step))
        # step+=1


    #excute TestCase
    def testPlayCount(self):
        self.common_check(VIDEO_ARTICLE)


if __name__ == '__main__':
    pass
    # a = TestLogin()
    # a.setUp()
    # a.testFunc1()
    # a.tearDown()
    #d =DbLib()

    import HTMLTestRunner
    t = unittest.TestSuite()
    t.addTest(unittest.makeSuite(TestComment))
    #unittest.TextTestRunner.run(t)
    filename = 'F:\\dx_comment.html'
    fp = file(filename,'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
            stream = fp,
            title ='Dx_Test',
            description = 'Report_discription')

    runner.run(t)
    fp.close()

