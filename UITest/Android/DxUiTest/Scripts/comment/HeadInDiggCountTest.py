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
from config import ACTIVITY
from elements_id import *
from common import exception_handler


class HeadInDiggCountTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.mode = 'mcp/dx'
        self.db = DbLib()
        self.api = ChnlRequest(self.mode)
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        start_to_index(self.driver,self.mode)
        if not is_login(self.driver):
            login_to_index(self.driver,self.mode,self.desired_caps['appPackage'],TEST_PHONE,DEVICE_TID)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self):
        step = 1

        #获取原始点赞数
        sleep(8)
        article = self.api.get_head_list()[0]['id']
        self.count = self.db.get_support_count_by_db(article)
        str_digg = u'赞'
        #点赞数为0显示测试
        self.db.set_support_count_by_db(article,0)
        slide_down(self.driver,3)
        article_count = self.driver.find_element_by_id(HEAD_INPAGE_DIGG_COUNT).text
        assert article_count == str_digg+str(0)
        print u'Step %s:上头条详情页点赞数为0时显示测试：OK' % (str(step))
        step+=1

        #点赞数为0-99999显示测试
        self.db.set_support_count_by_db(article,99999)
        slide_down(self.driver,3)
        article_count = self.driver.find_element_by_id(HEAD_INPAGE_DIGG_COUNT).text
        assert article_count == str_digg+str(99999)
        print u'Step %s:上头条详情页点赞数为<=99999时显示测试：OK' % (str(step))
        step+=1

        #点赞数大于等于10万显示测试
        self.db.set_support_count_by_db(article,100000)
        slide_down(self.driver,3)
        article_count = self.driver.find_element_by_id(HEAD_INPAGE_DIGG_COUNT).text
        assert article_count == str_digg+u'99999 +'
        print u'Step %s:上头条详情页点赞数大于等于10万时显示测试：OK' % (str(step))
        step+=1

        self.db.set_support_count_by_db(article,self.count)

    #excute TestCase
    def testHeadCount(self):
        assert go_to_head(self.driver)
        sleep(WAIT_TIME)
        self.driver.find_element_by_id(HEAD_CONTENT).click()
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

