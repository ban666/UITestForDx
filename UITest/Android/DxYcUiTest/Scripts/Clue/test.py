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
from ui_clue imoport *
from configrw import get_case
from TestlinkHandler import TestlinkHandler

class AppQuitTest(unittest.TestCase):

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

        go_to_clue(self.driver)

        sub_1 = self.driver.find_element_by_id(SUB_TYPE_1)
        sub_2 = self.driver.find_element_by_id(SUB_TYPE_2)
        sub_3 = self.driver.find_element_by_id(SUB_TYPE_3)
        sub_4 = self.driver.find_element_by_id(SUB_TYPE_4)

        assert sub_1.text == u'投诉'
        assert sub_2.text == u'咨询'
        assert sub_3.text == u'求助'
        assert sub_4.text == u'建议'

        go_to_mycomm(self.driver,self.mode)
        assert self.driver.find_element_by_id(MY_COMM_REPLY).get_attribute('checked') == 'false'
        assert self.driver.find_element_by_id(MY_COMM_SEND).get_attribute('checked') == 'true'

        #点击切换
        self.driver.find_element_by_id(MY_COMM_REPLY).click()
        assert self.driver.find_element_by_id(MY_COMM_REPLY).get_attribute('checked') == 'true'
        assert self.driver.find_element_by_id(MY_COMM_SEND).get_attribute('checked') == 'false'
        print u'Step %s:点击切换我的评论-回复评论测试：OK' % (str(step))
        step+=1

        #右划切换
        slide_right(self.driver)
        sleep(3)
        assert self.driver.find_element_by_id(MY_COMM_REPLY).get_attribute('checked') == 'false'
        assert self.driver.find_element_by_id(MY_COMM_SEND).get_attribute('checked') == 'true'
        print u'Step %s:右划切换我的评论-回复评论测试：OK' % (str(step))
        step+=1

        #左划切换
        slide_left(self.driver)
        assert self.driver.find_element_by_id(MY_COMM_REPLY).get_attribute('checked') == 'true'
        assert self.driver.find_element_by_id(MY_COMM_SEND).get_attribute('checked') == 'false'
        print u'Step %s:左划切换我的评论-回复评论测试：OK' % (str(step))
        step+=1

        return True

    #excute TestCase
    def testQuit(self):
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

