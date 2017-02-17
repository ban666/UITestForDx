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

class ErrArticleSearchTest(unittest.TestCase):

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
            self.db.publish_del_article_by_db(self.infoid)
            self.tsl.set_tc_status(self.case_id,self.result,self.msg)
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def testErrSearch(self):
        step = 1

        self.case_id = get_case(__file__)

        #搜索文章
        self.infoid = self.db.get_infoid_by_article_name(STATUS_ARTICLE)


        get_to_search(self.driver,self.mode)
        #文章为发布状态时搜索
        seach_by_ui(self.driver,STATUS_ARTICLE)
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',SEARCH_EMPTY_TIPS) == False and \
               element_exsist(self.driver,'id',SEARCH_ITEM)
        self.driver.find_element_by_id(SEARCH_CANCEL).click()

        #文章为被删除状态时搜索
        self.db.del_article_by_db(self.infoid)
        seach_by_ui(self.driver,STATUS_ARTICLE)
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',SEARCH_EMPTY_TIPS)
        self.driver.find_element_by_id(SEARCH_CANCEL).click()
        print u'Step %s:被删除新闻无法被搜索到测试：OK' % (str(step))
        step+=1

        #文章为未审核状态时搜索
        self.db.set_article_unpublished_by_db(self.infoid)
        seach_by_ui(self.driver,STATUS_ARTICLE)
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',SEARCH_EMPTY_TIPS)
        self.driver.find_element_by_id(SEARCH_CANCEL).click()
        print u'Step %s:未审核新闻无法被搜索到测试：OK' % (str(step))
        step+=1

        #文章为审核不通过时搜索
        self.db.set_article_faield_by_db(self.infoid)
        seach_by_ui(self.driver,STATUS_ARTICLE)
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',SEARCH_EMPTY_TIPS)
        self.driver.find_element_by_id(SEARCH_CANCEL).click()
        print u'Step %s:审核不通过新闻无法被搜索到测试：OK' % (str(step))
        step+=1

        self.result = True


if __name__ == '__main__':
    print



