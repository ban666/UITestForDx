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

class SearchStyleTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.mode = MODE
        self.db = DbLib()
        #self.api = ChnlRequest(self.mode)
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        start_to_index(self.driver,self.mode)

    def tearDown(self):
        print 'Test End...................................'
        try:
             self.tsl.set_tc_status(self.case_id,self.result,self.msg)
             self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def testNormalArticle(self):
        step = 1

        #搜索文章并检查样式
        get_to_search(self.driver)
        seach_by_ui(self.driver,NORMAL_ARTICLE)
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',NORMAL_TITLE) and element_exsist(self.driver,'id',NORMAL_IMAGE) == False
        print u'Step %s:搜索结果中纯文字新闻显示测试：OK' % (str(step))
        step+=1

    def testSinglePicArticle(self):
        step = 1

        #搜索文章并检查样式
        get_to_search(self.driver)
        seach_by_ui(self.driver,SINGLE_PIC_ARTICLE)
        sleep(WAIT_TIME)
        el_list = [NORMAL_TITLE,NORMAL_IMAGE]
        for el in el_list:
            assert element_exsist(self.driver,'id',el)
        print u'Step %s:搜索结果中单小图新闻显示测试：OK' % (str(step))
        step+=1

    def testBigPicArticle(self):
        step = 1

        #搜索文章并检查样式
        get_to_search(self.driver)
        seach_by_ui(self.driver,BIG_PIC_ARTICLE)
        sleep(WAIT_TIME)
        el_list = [BIG_TITLE,BIG_IMAGE]
        for el in el_list:
            assert element_exsist(self.driver,'id',el)
        print u'Step %s:搜索结果中单大图新闻显示测试：OK' % (str(step))
        step+=1

    def testThreePicArticle(self):
        step = 1

        #搜索文章并检查样式
        get_to_search(self.driver)
        seach_by_ui(self.driver,THREE_PIC_ARTICLE)
        sleep(WAIT_TIME)
        el_list = [THREE_PIC_TITLE]
        el_list.extend(THREE_PIC_IMAGE)
        for el in el_list:
            assert element_exsist(self.driver,'id',el)
        print u'Step %s:搜索结果中三小图新闻显示测试：OK' % (str(step))
        step+=1
    
    def testFlagArticle(self):
        step = 1

        #搜索文章并检查样式
        get_to_search(self.driver)
        seach_by_ui(self.driver,FLAG_ARTICLE)
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',NORMAL_TITLE) and element_exsist(self.driver,'id',ARTICLE_FLAG) == False
        print u'Step %s:搜索结果中角标不显示测试：OK' % (str(step))
        step+=1

    def testVideoArticle(self):
        step = 1

        #搜索文章并检查样式
        get_to_search(self.driver)
        seach_by_ui(self.driver,VIDEO_ARTICLE)
        sleep(WAIT_TIME)
        el_list = [NORMAL_TITLE,NORMAL_IMAGE]
        non_exsist_el_list = [VIDEO_TITLE,VIDEO_IMAGE]
        for el in el_list:
            assert element_exsist(self.driver,'id',el)
        for non_el in non_exsist_el_list:
            assert element_exsist(self.driver,'id',non_el) == False
        print u'Step %s:搜索结果中视频以单小图样式展示测试：OK' % (str(step))
        step+=1


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

