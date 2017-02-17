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
from common import exception_handler,caclulate_for_audio,time_range_for_audio

class ProgressTest(unittest.TestCase):

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
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self):
        step = 1
        #发表评论
        type_title = self.driver.find_element_by_id('com.cnhubei.dxxwhw:id/tv_typetitle').text
        print type_title
        assert type_title == u'精彩评论'
        print u'Step %s:评论页存在精彩评论测试：OK' % (str(step))
        step+=1

    def non_exsist_check(self):
        step = 1
        #发表评论
        type_title = self.driver.find_element_by_id('com.cnhubei.dxxwhw:id/tv_typetitle').text
        print type_title
        assert type_title == u'最新评论'
        print u'Step %s:评论页不存在精彩评论测试：OK' % (str(step))
        step+=1

    #excute TestCase
    def testExsit(self):
        step = 1

        get_to_article_by_search(self.driver,AUDIO_ARTICLE,self.mode)
        all_time = get_alltime(self.driver)
        #print caclulate_for_audio('3:20',0.3)
        seekbar_sendkey(self.driver,0.7)
        sleep(WAIT_TIME)
        played_time = get_played_time(self.driver)
        real_time = caclulate_for_audio(all_time,0.7)
        assert abs(time_range_for_audio(played_time,real_time)) < 8
        print u'Step %s:进度条右划测试：OK' % (str(step))
        step+=1

        seekbar_sendkey(self.driver,0.3)
        sleep(WAIT_TIME)
        played_time = get_played_time(self.driver)
        real_time = caclulate_for_audio(all_time,0.3)
        assert abs(time_range_for_audio(played_time,real_time)) < 8
        print u'Step %s:进度条左划测试：OK' % (str(step))
        step+=1

        #self.non_exsist_check()

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

