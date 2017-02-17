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
from ui_settings import *
from configrw import get_case
from TestlinkHandler import TestlinkHandler

class SubTypeTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.result = 'f'
        self.msg = ''
        self.tsl = TestlinkHandler()
        self.mode = MODE
        self.db = DbLib()
        #self.api = ChnlRequest(MODE)
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        start_to_index(self.driver,self.mode)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.tsl.set_tc_status(self.case_id,self.result,self.msg)
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self):
        step = 1

        go_to_settings(self.driver)
        content = u'一'*256
        go_to_suggestion(self.driver)
        self.driver.find_element_by_id(SUGGESTION_INPUT).send_keys(content)
        assert self.driver.find_element_by_id(SUGGESTION_INPUT).text == content[:255]
        sleep(WAIT_TIME)
        print u'Step %s:意见反馈输入内容超过255测试：OK' % (str(step))
        step+=1

        self.driver.find_element_by_id(SUGGESTION_CONFIRM).click()
        sleep(WAIT_TIME)
        assert self.driver.current_activity == ACTIVITY.get('index')
        print u'Step %s:意见反馈在255字数以内时能够正常提交：OK' % (str(step))
        step+=1
        return True

    def db_check(self):
        step = 1

        go_to_settings(self.driver)
        content = u'建议测试'+str(randint(0,10000))
        go_to_suggestion(self.driver)
        self.driver.find_element_by_id(SUGGESTION_INPUT).send_keys(content)
        sleep(WAIT_TIME)
        self.driver.find_element_by_id(SUGGESTION_CONFIRM).click()
        sleep(WAIT_TIME)
        info = self.db.get_latest_suggestion_info()
        mid = self.db.get_mid_by_phone(TEST_PHONE)
        assert info.get('content').decode('utf-8') == content
        assert str(info.get('mid')) == str(mid)
        assert str(info.get('z')) == '420500'
        assert str(info.get('version')) == VERSION
        print u'Step %s:提交的意见反馈在数据库中能正确记录用户mid和客户端id及版本号：OK' % (str(step))
        step+=1
        return True

    #excute TestCase
    def test(self):
        self.case_id = get_case(__file__)
        self.result = self.common_check()

    def testDb(self):
        self.case_id = get_case(__file__)
        self.result = self.db_check()

if __name__ == '__main__':
    pass
    # a = TestLogin()
    # a.setUp()
    # a.testFunc1()
    # a.tearDown()
    #d =DbLib()

