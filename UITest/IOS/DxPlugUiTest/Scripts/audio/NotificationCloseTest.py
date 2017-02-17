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
from configrw import get_case
from TestlinkHandler import TestlinkHandler


class NotificationCloseTest(unittest.TestCase):

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

        #进入音频页并等待音频开始播放
        get_to_article_by_search(self.driver,article,self.mode)
        sleep(WAIT_TIME)

        while get_played_time(self.driver) == '00:00':
            sleep(WAIT_TIME)

        #通知栏关闭音频
        open_notifications(self.driver)
        sleep(WAIT_TIME)
        self.driver.find_element_by_id(NOTIFICATION_AUDIO_CLOSE).click()
        sleep(WAIT_TIME)
        try:
            close_notification(self.driver)
        except:
            pass
        played_time_now = get_played_time(self.driver)
        assert played_time_now  == '00:00'
        assert element_exsist(self.driver,'id',AUDIO_START)
        print u'Step %s:通知栏关闭音频播放器测试：OK' % (str(step))
        step+=1

        open_notifications(self.driver)
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',NOTIFICATION_AUDIO_CLOSE) == False
        print u'Step %s:通知栏关闭通知栏销毁测试：OK' % (str(step))
        step+=1

        close_notification(self.driver)

        return True

    #excute TestCase
    def test(self):
        self.case_id = get_case(__file__)
        self.result = self.common_check(AUDIO_ARTICLE)


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

