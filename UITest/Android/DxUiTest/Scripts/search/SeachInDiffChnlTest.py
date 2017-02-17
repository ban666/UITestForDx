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

    def testSearchInDiffChnl(self):
        step = 1

        self.case_id = get_case(__file__)

        #搜索文章并检查样式
        chnl_group = self.driver.find_element_by_id(CHNL_GROUP).find_elements_by_class_name('android.widget.TextView')
        for chnl in chnl_group[:5]:
            chnl.click()
            sleep(WAIT_TIME)
            get_to_search(self.driver,self.mode)
            sleep(WAIT_TIME)
            assert self.driver.current_activity == ACTIVITY.get('search')
            back(self.driver)

        print u'Step %s:所有新闻列表都能下拉显示搜索框并点击进入搜索界面：OK' % (str(step))
        step+=1

        self.result = True


if __name__ == '__main__':
    print



