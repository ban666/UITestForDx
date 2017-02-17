# -*- coding: utf-8 -*-
__author__ = 'liaoben'

import sys
from appium import webdriver
from time import sleep
import unittest
from random import randint
sys.path.append('../../Lib')
import time
from appium_lib import *
from dx_action import *
from ui_comment import *
from ChnlRequest import ChnlRequest
from DbLib import DbLib
from config import *
from loglib import log

from elements_id import *
from common import exception_handler

class NetworkChangeTest(unittest.TestCase):

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
            change_network(self.driver,'wifi')
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self,article):
        step = 1


        #发表评论
        get_to_article_by_search(self.driver,AUDIO_ARTICLE,self.mode)
        sleep(WAIT_TIME)
        play_time_a = self.driver.find_element_by_id(AUDIO_PLAY_TIME).text
        print play_time_a
        back(self.driver)
        change_network(self.driver,'none')
        sleep(WAIT_TIME)
        self.driver.find_element_by_class_name('android.widget.RelativeLayout')\
            .find_element_by_class_name('android.widget.TextView').click()
        #assert element_exsist(self.driver,'id',AUDIO_START)
        play_time_b = self.driver.find_element_by_id(AUDIO_PLAY_TIME).text
        print play_time_b
        # self.driver.find_element_by_id(AUDIO_PAUSE).click()
        # back(self.driver)
        # sleep(WAIT_TIME)
        # slide_down(self.driver)
        # assert self.driver.find_element_by_id(PAGEVIEW_COUNT).text+u'播放' == u'23播放'
        # print u'Step %s:播放数增加测试：OK' % (str(step))
        # step+=1


    #excute TestCase
    def testPlayCount(self):
        self.common_check(AUDIO_ARTICLE)

    def test(self):
        open_notifications(self.driver)
        self.driver.find_element_by_id(NOTIFICATION_AUDIO_CLOSE).click()

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

