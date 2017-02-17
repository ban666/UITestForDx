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

from config import *
from elements_id import *
from common import exception_handler

class MyCommentSlideTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.mode = 'mcp/dx'
        self.db = DbLib()
        self.api = ChnlRequest(self.mode)
        self.first_article = self.api.get_first_chnl_article_by_model(13)
        self.db.change_comment_state_by_db(self.first_article['id'],2)
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        start_to_index(self.driver,self.mode)
        if not is_login(self.driver):
            login_to_index(self.driver,self.mode,self.desired_caps['appPackage'],TEST_PHONE,DEVICE_TID)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.db.change_comment_state_by_db(self.first_article['id'],0)
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self):
        step = 1

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

    #excute TestCase
    def testMyComment(self):
        self.common_check()

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

