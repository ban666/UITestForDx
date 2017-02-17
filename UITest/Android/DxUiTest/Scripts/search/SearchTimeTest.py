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

class SearchTimeTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.result = 'f'
        self.msg = ''
        self.mode = MODE
        self.db = DbLib()
        self.tsl = TestlinkHandler()
        #self.api = ChnlRequest(self.mode)
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        start_to_index(self.driver,self.mode)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.tsl.set_tc_status(self.case_id,self.result,self.msg)
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def testSearchTime(self):
        step = 1

        self.case_id = get_case(__file__)

        get_to_search(self.driver,self.mode)


        now_day = get_day(0,'%Y-%m-%d %H:%M:%S')
        yesterday = get_day(1,'%Y-%m-%d %H:%M:%S')
        other_day = get_day(2,'%Y-%m-%d %H:%M:%S')
        other_day_expect =  get_day(2,'%m-%d')
        #修改文章时间为今天
        self.db.set_article_time_by_db(now_day,'title=\''+NORMAL_ARTICLE+'\'')
        seach_by_ui(self.driver,NORMAL_ARTICLE)
        sleep(WAIT_TIME)
        search_time = self.driver.find_element_by_id(SEARCH_ITEM_DATA).text
        print search_time
        assert search_time == u'今日'
        self.driver.find_element_by_id(SEARCH_CANCEL).click()

        #修改文章时间为昨天
        self.db.set_article_time_by_db(yesterday,'title=\''+NORMAL_ARTICLE+'\'')
        seach_by_ui(self.driver,NORMAL_ARTICLE)
        sleep(WAIT_TIME)
        search_time = self.driver.find_element_by_id(SEARCH_ITEM_DATA).text
        print search_time
        assert search_time == u'昨日'
        self.driver.find_element_by_id(SEARCH_CANCEL).click()

        #修改文章时间为2天前
        self.db.set_article_time_by_db(other_day,'title=\''+NORMAL_ARTICLE+'\'')
        seach_by_ui(self.driver,NORMAL_ARTICLE)
        sleep(WAIT_TIME)
        search_time = self.driver.find_element_by_id(SEARCH_ITEM_DATA).text
        print search_time
        assert search_time == other_day_expect
        self.driver.find_element_by_id(SEARCH_CANCEL).click()

        print u'Step %s:搜索结果中时间显示正确：OK' % (str(step))
        step+=1
        self.result = True


if __name__ == '__main__':
    db = DbLib()
    now_day = get_day()
    db.set_article_time_by_db(now_day,'title=\''+NORMAL_ARTICLE+'\'')



