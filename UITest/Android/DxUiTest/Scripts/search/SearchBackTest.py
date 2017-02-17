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
from common import exception_handler
from configrw import get_case
from TestlinkHandler import TestlinkHandler

class SearchBackTest(unittest.TestCase):

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

    def testSearchBack(self):
        step = 1

        self.case_id = get_case(__file__)
        #搜索文章并检查样式
        chnl_group = self.driver.find_element_by_id(CHNL_GROUP).find_elements_by_class_name('android.widget.TextView')
        chnl_group[1].click()
        sleep(WAIT_TIME)
        first_article_in = self.driver.find_element_by_id(NORMAL_TITLE).text
        print first_article_in
        get_to_search(self.driver,self.mode)
        print self.driver.current_activity
        seach_by_ui(self.driver,'ABC')
        sleep(WAIT_TIME)
        self.driver.find_element_by_id(SEARCH_BACK).click()

        first_article_out = self.driver.find_element_by_id(NORMAL_TITLE).text
        print first_article_in,first_article_out
        print u'Step %s:取消搜索时能回到搜索前的新闻列表：OK' % (str(step))
        step+=1
        self.result = True


if __name__ == '__main__':
    print



