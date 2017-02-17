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
from loglib import log
from config import *
from elements_id import *
from common import exception_handler
from ui_settings import *
from adb import *


class MyCommentBlankTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.mode = MODE
        self.db = DbLib()
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        start_to_index(self.driver,self.mode)
        if not is_login(self.driver):
            login_to_index(self.driver,TEST_PHONE)
        logout_to_index(self.driver,self.mode)
        #print dc

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down'

    def common_check(self):
        step = 1

        go_to_mycomm(self.driver,self.mode)
        sleep(WAIT_TIME)
        #查看当前页面是否有提示
        assert element_exsist(self.driver,*ARTICLE_EMPTY_TIPS)
        assert self.driver.find_element(*ARTICLE_EMPTY_TIPS).text == u'暂无数据'
        print u'Step %s:我的评论-发布评论 列表无数据有提示测试结果：OK' % (str(step))
        step+=1

        self.driver.find_element(*MY_COMM_REPLY).click()
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,*ARTICLE_EMPTY_TIPS)
        assert self.driver.find_element(*ARTICLE_EMPTY_TIPS).text == u'暂无数据'
        print u'Step %s:我的评论-回复评论 列表无数据有提示测试结果：OK' % (str(step))
        step+=1



    #excute TestCase
    def testBlank(self):
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
    t.addTest(unittest.makeSuite(MyCommentBlankTest))
    #unittest.TextTestRunner.run(t)
    filename = 'F:\\dx_comment.html'
    fp = file(filename,'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
            stream = fp,
            title ='Dx_Test',
            description = 'Report_discription')

    runner.run(t)
    fp.close()

