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


class HeadInReplyCountTest(unittest.TestCase):

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

        #获取原始评论数
        article = self.api.get_head_list()[0]['id']
        self.count = self.db.get_comment_count_by_id(article)
        str_comment = u'评论'
        #评论数为0显示测试
        self.db.change_comment_count_by_id(article,0)
        slide_down(self.driver,3)
        article_count = self.driver.find_element_by_id(HEAD_INPAGE_REPLY_COUNT).text
        assert article_count == str_comment+str(0)
        print u'Step %s:上头条详情页评论数为0时显示测试：OK' % (str(step))
        step+=1

        #评论数为0-99999显示测试
        self.db.change_comment_count_by_id(article,99999)
        slide_down(self.driver,3)
        article_count = self.driver.find_element_by_id(HEAD_INPAGE_REPLY_COUNT).text
        assert article_count == str_comment+str(99999)
        print u'Step %s:上头条详情页评论数为<=99999时显示测试：OK' % (str(step))
        step+=1

        #评论数大于等于10万显示测试
        self.db.change_comment_count_by_id(article,100000)
        slide_down(self.driver,3)
        article_count = self.driver.find_element_by_id(HEAD_INPAGE_REPLY_COUNT).text
        assert article_count == str_comment+u'99999 +'
        print u'Step %s:上头条详情页评论数大于等于10万时显示测试：OK' % (str(step))
        step+=1

        self.db.change_comment_count_by_id(article,self.count)

    #excute TestCase
    def testHeadCount(self):
        assert go_to_head(self.driver)
        sleep(WAIT_TIME)
        self.driver.find_element_by_id(HEAD_CONTENT).click()
        sleep(WAIT_TIME)
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
