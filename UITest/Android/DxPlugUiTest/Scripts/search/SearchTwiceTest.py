# -*- coding: utf-8 -*-
__author__ = 'liaoben'

import sys
sys.path.append('../../Lib')
from appium import webdriver
from time import sleep
import unittest
from appium_lib import *
from dx_action import *
from ui_comment import *
from ChnlRequest import ChnlRequest
from DbLib import DbLib
from config import *
from loglib import log
from adb import is_login
from elements_id import *
from common import exception_handler

class SearchTwiceTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.mode = MODE
        self.db = DbLib()
        #self.api = ChnlRequest(self.mode)
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        start_to_index(self.driver,self.mode)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self,words):
        step = 1


        get_to_search(self.driver)
        #无结果搜索
        seach_by_ui(self.driver,words)
        sleep(WAIT_TIME)
        empty_tips = self.driver.find_element_by_id(SEARCH_EMPTY_TIPS).text
        expect_tips = u'找不到与“'+ words+u'”相符的结果'
        assert expect_tips==empty_tips

        #搜索正常文章
        seach_by_ui(self.driver,NORMAL_ARTICLE)
        sleep(WAIT_TIME)
        title = self.driver.find_element_by_id(NORMAL_TITLE).text
        assert title==NORMAL_ARTICLE

        #无结果搜索
        seach_by_ui(self.driver,words)
        sleep(WAIT_TIME)
        empty_tips = self.driver.find_element_by_id(SEARCH_EMPTY_TIPS).text
        expect_tips = u'找不到与“'+ words+u'”相符的结果'
        assert expect_tips==empty_tips
        print u'Step %s:连续搜索内容相互独立测试：OK' % (str(step))
        step+=1

    #excute TestCase
    def testSearch(self):
        words = '123321aaaaaaaa'
        self.common_check(words)


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

