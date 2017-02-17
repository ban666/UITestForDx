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
from common import exception_handler,get_day
from configrw import get_case
from TestlinkHandler import TestlinkHandler

class SearchSlideTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.result = 'f'
        self.msg = ''
        self.mode = MODE
        self.db = DbLib()
        self.tsl = TestlinkHandler()
        self.api = ChnlRequest(self.mode)
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        start_to_index(self.driver,self.mode)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.tsl.set_tc_status(self.case_id,self.result,self.msg)
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def testSearchSlide(self):
        step = 1

        self.case_id = get_case(__file__)

        get_to_search(self.driver,self.mode)

        #搜索文章并检查样式
        get_to_search(self.driver,self.mode)
        sleep(WAIT_TIME)

        seach_by_ui(self.driver,HEAD_ARTICLE)
        assert element_exsist(self.driver,'id',SEARCH_EMPTY_TIPS)
        slide_left(self.driver)
        assert self.driver.find_element_by_id(SEARCH_ARTICLE).get_attribute('checked') == 'false'
        assert self.driver.find_element_by_id(SEARCH_HEAD).get_attribute('checked') == 'true'
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',HEAD_PIC)
        print u'Step %s:划屏切换到报料搜索测试：OK' % (str(step))
        step+=1

        slide_right(self.driver)
        assert element_exsist(self.driver,'id',SEARCH_EMPTY_TIPS)
        assert self.driver.find_element_by_id(SEARCH_ARTICLE).get_attribute('checked') == 'true'
        assert self.driver.find_element_by_id(SEARCH_HEAD).get_attribute('checked') == 'false'
        print u'Step %s:划屏切换到文章搜索测试：OK' % (str(step))
        step+=1
        self.result = True


if __name__ == '__main__':
    db = DbLib()
    now_day = get_day()
    db.set_article_time_by_db(now_day,'title=\''+NORMAL_ARTICLE+'\'')



