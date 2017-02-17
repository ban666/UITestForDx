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
from config import TEST_PHONE,DEVICE_TID
from elements_id import *
from common import exception_handler

class AnonymousCommentTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.mode = 'mcp/dx'
        self.db = DbLib()
        self.api = ChnlRequest(self.mode)
        self.first_article = self.api.get_first_chnl_article_by_model(13)
        self.db.change_comment_state_by_db(self.first_article['id'],2)
        self.driver = webdriver.Remote('http://localhost:4732/wd/hub', self.desired_caps)
        start_to_index(self.driver,self.mode)
        if is_login(self.driver):
            logout_to_index(self.driver,self.mode)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.db.change_comment_state_by_db(self.first_article['id'],0)
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self):
        step = 1
        #发表评论
        type_title = self.driver.find_element_by_id(AMAZING_COMMENT_TIPS).text
        print type_title
        assert type_title == u'精彩评论'
        print u'Step %s:评论页存在精彩评论测试：OK' % (str(step))
        step+=1

    def non_exsit_check(self):
        step = 1
        #发表评论
        type_title = self.driver.find_element_by_id(AMAZING_COMMENT_TIPS).text
        print type_title
        assert type_title == u'最新评论'
        print u'Step %s:评论页不存在精彩评论测试：OK' % (str(step))
        step+=1

    #excute TestCase
    def testExsit(self):
        get_to_article_by_search(self.driver,WONDERFUL_COMMENT_ARTICLE,self.mode)
        sleep(WAIT_TIME)
        self.driver.find_element_by_id(COMMENT_ITEM).click()
        self.common_check()

    def testNonExsit(self):
        get_to_article_by_search(self.driver,NORMAL_ARTICLE,self.mode)
        sleep(WAIT_TIME)
        self.driver.find_element_by_id(COMMENT_ITEM).click()
        self.non_exsit_check()


if __name__ == '__main__':
    pass
    # a = TestLogin()
    # a.setUp()
    # a.testFunc1()
    # a.tearDown()
    #d =DbLib()
    __import__('AnonymousCommentTest')
    # import HTMLTestRunner
    # t = unittest.TestSuite()
    # t.addTest(unittest.makeSuite(TestComment))
    # #unittest.TextTestRunner.run(t)
    # filename = 'F:\\dx_comment.html'
    # fp = file(filename,'wb')
    # runner = HTMLTestRunner.HTMLTestRunner(
    #         stream = fp,
    #         title ='Dx_Test',
    #         description = 'Report_discription')
    #
    # runner.run(t)
    # fp.close()

