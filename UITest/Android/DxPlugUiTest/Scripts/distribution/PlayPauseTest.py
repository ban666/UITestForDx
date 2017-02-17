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
from adb import is_login
from elements_id import *
from common import exception_handler,get_now
from screenshot import Appium_Extend

class PlayPauseTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.mode = MODE
        self.db = DbLib()
        #self.api = ChnlRequest(self.mode)
        remote_url = get_appium_url_from_config()
        self.driver = webdriver.Remote(remote_url, self.desired_caps)
        start_to_index(self.driver,self.mode)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self,article):
        step = 1

        #音频详情页播放时验证通知栏
        fname_pause =PIC_SAVE_PATH+'\\pause'+get_now()+'.png'
        fname_start =PIC_SAVE_PATH+'\\start'+get_now()+'.png'
        start_image = IMAGE_PATH + '\\'+IMAGES['notification_start']
        pause_image = IMAGE_PATH + '\\'+IMAGES['notification_pause']
        get_to_article_by_search(self.driver,article,self.mode)
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',AUDIO_PAUSE)
        open_notifications(self.driver)
        sleep(WAIT_TIME)
        scr = Appium_Extend(self.driver)
        el = self.driver.find_element_by_id(NOTIFICATION_AUDIO_PLAY)
        scr.get_screenshot_by_element(el,fname_pause)
        assert scr.same_as(fname_pause,pause_image)
        print u'Step %s:音频详情页播放时通知栏图标测试：OK' % (str(step))
        step+=1

        #音频详情页暂停时验证通知栏
        close_notification(self.driver)
        sleep(5)
        self.driver.find_element_by_id(AUDIO_PAUSE).click()
        assert element_exsist(self.driver,'id',AUDIO_START)
        open_notifications(self.driver)
        sleep(WAIT_TIME)
        el = self.driver.find_element_by_id(NOTIFICATION_AUDIO_PLAY)
        scr.get_screenshot_by_element(el,fname_start)
        assert scr.same_as(fname_start,start_image)
        #print self.driver.current_activity
        print u'Step %s:音频详情页暂停时通知栏图标测试：OK' % (str(step))
        step+=1

        #通知栏播放时验证详情页
        open_notifications(self.driver)
        sleep(WAIT_TIME)
        self.driver.find_element_by_id(NOTIFICATION_AUDIO_PLAY).click()
        scr.get_screenshot_by_element(el,fname_pause)
        assert scr.same_as(fname_pause,pause_image)
        close_notification(self.driver)
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',AUDIO_PAUSE)
        print u'Step %s:通知栏播放时详情页状态测试：OK' % (str(step))
        step+=1

        #通知栏暂停时验证详情页
        open_notifications(self.driver)
        sleep(WAIT_TIME)
        self.driver.find_element_by_id(NOTIFICATION_AUDIO_PLAY).click()
        scr.get_screenshot_by_element(el,fname_start)
        assert scr.same_as(fname_start,start_image)
        close_notification(self.driver)
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',AUDIO_START)
        print u'Step %s:通知栏暂停时详情页状态测试：OK' % (str(step))
        step+=1

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
        self.common_check(AUDIO_ARTICLE)


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

