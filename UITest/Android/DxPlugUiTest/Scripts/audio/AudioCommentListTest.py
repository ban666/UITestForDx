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
from configrw import get_case
from TestlinkHandler import TestlinkHandler

class AudioCommentTest(unittest.TestCase):

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

        #音频详情页左划进入评论列表页
        get_to_article_by_search(self.driver,article,self.mode)
        sleep(WAIT_TIME)
        slide_left(self.driver)
        sleep(WAIT_TIME)
        assert self.driver.current_activity == ACTIVITY.get('comment')
        print u'Step %s:音频详情页左划进入评论列表页测试：OK' % (str(step))
        step+=1


        #音频详情页点击评论按钮入评论列表页
        back(self.driver)
        sleep(WAIT_TIME)
        self.driver.find_element_by_id(COMMENT_AUDIO_ENTRANCE).click()
        sleep(WAIT_TIME)
        assert self.driver.current_activity == ACTIVITY.get('comment')
        print u'Step %s:音频详情页点击评论按钮进入评论列表页测试：OK' % (str(step))
        step+=1

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

