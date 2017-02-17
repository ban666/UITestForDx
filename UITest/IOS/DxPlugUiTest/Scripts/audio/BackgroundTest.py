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
from common import exception_handler,get_now,time_range_for_audio
from configrw import get_case
from TestlinkHandler import TestlinkHandler


class BackgroundTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.result = 'f'
        self.msg = ''
        self.tsl = TestlinkHandler()
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

        #退出到其他页面后播放器持续播放
        get_to_article_by_search(self.driver,article,self.mode)
        sleep(WAIT_TIME)
        play_time = self.driver.find_element_by_id(AUDIO_PLAY_TIME)
        while play_time.text == '00:00':
            sleep(WAIT_TIME)
        play_time_old = play_time.text
        #print play_time_old
        back(self.driver)
        sleep(WAIT_TIME)
        self.driver.find_element_by_class_name('android.widget.RelativeLayout')\
            .find_element_by_class_name('android.widget.TextView').click()
        sleep(WAIT_TIME)
        play_time_new = play_time.text
        #print play_time_new
        time_range = time_range_for_audio(play_time_old,play_time_new)
        assert time_range >= 7
        print u'Step %s:切换到客户端其他页面时音频继续播放测试：OK' % (str(step))

        return True

    def home_check(self,article):
        step = 1

        #退出到其他页面后播放器持续播放
        get_to_article_by_search(self.driver,article,self.mode)
        sleep(WAIT_TIME)
        play_time = self.driver.find_element_by_id(AUDIO_PLAY_TIME)
        while play_time.text == '00:00':
            sleep(WAIT_TIME)
        play_time_old = play_time.text
        #print play_time_old
        home(self.driver)
        sleep(5)
        open_notifications(self.driver)
        sleep(WAIT_TIME)
        self.driver.find_element_by_id(NOTIFICATION_AUDIO_TITLE).click()
        sleep(WAIT_TIME)
        play_time_new = get_played_time(self.driver)
        #print play_time_new
        time_range = time_range_for_audio(play_time_old,play_time_new)
        assert time_range >= 11
        print u'Step %s:将客户端压后台后音频继续播放测试：OK' % (str(step))

        return True

    def back_check(self,article):
        step = 1

        #退出到其他页面后播放器持续播放
        get_to_article_by_search(self.driver,article,self.mode)
        sleep(WAIT_TIME)
        play_time = self.driver.find_element_by_id(AUDIO_PLAY_TIME)
        while play_time.text == '00:00':
            sleep(WAIT_TIME)
        play_time_old = play_time.text
        #print play_time_old
        back(self.driver)
        sleep(WAIT_TIME)
        self.driver.find_element_by_class_name('android.widget.RelativeLayout')\
            .find_element_by_class_name('android.widget.TextView').click()
        sleep(WAIT_TIME)
        play_time_new = play_time.text
        #print play_time_new
        time_range = time_range_for_audio(play_time_old,play_time_new)
        assert time_range >= 7
        print u'Step %s:音频详情页播放时退出详情页，音频继续正常播放测试：OK' % (str(step))

        return True


    #excute TestCase
    def testSwitch(self):
        self.case_id = get_case(__file__)
        self.result = self.common_check(AUDIO_ARTICLE)

    def testAudioHome(self):
        self.case_id = get_case(__file__)
        self.result = self.home_check(AUDIO_ARTICLE)

    def testBack(self):
        self.case_id = get_case(__file__)
        self.result = self.back_check(AUDIO_ARTICLE)

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

