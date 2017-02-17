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

class SearchBasicTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.result = 'f'
        self.msg = ''
        self.tsl = TestlinkHandler()
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

    def common_check(self,article,model,article_type):
        step = 1
        try:
            model = model.decode('gbk')
        except:
            pass
        #搜索文章并检查样式
        get_to_article_by_search(self.driver,article,self.mode)
        sleep(WAIT_TIME)
        assert judge_article_type(self.driver,article_type)
        print u'Step %s: %s新闻能够搜索并查看测试：OK' % (str(step),model)
        step+=1
        return True

    def ext_check(self,article):
        step = 1

        #搜索文章并检查样式
        get_to_article_by_search(self.driver,article)
        sleep(WAIT_TIME)
        #print self.driver.current_activity
        assert judge_article_type(self.driver,'ext')
        print u'Step %s:外链新闻能够搜索并查看测试：OK' % (str(step))
        step+=1
        return True

    def targeturl_check(self,article):
        step = 1

        #搜索文章并检查样式
        get_to_article_by_search(self.driver,article)
        sleep(WAIT_TIME)
        assert judge_article_type(self.driver,'targeturl')
        print u'Step %s:TargetUrl新闻能够搜索并查看测试：OK' % (str(step))
        step+=1
        return True

    def testArticleSearch(self):
        self.case_id = get_case(__file__)
        self.result = self.common_check(NORMAL_ARTICLE,u'普通文字','article')

    def testVideoSearch(self):
        self.case_id = get_case(__file__)
        self.result = self.common_check(VIDEO_ARTICLE,u'视频','video')

    def testAudioSearch(self):
        self.case_id = get_case(__file__)
        self.result = self.common_check(AUDIO_ARTICLE,u'音频','audio')

    def testExtSearch(self):
        self.case_id = get_case(__file__)
        self.result = self.common_check(EXT_ARTICLE,u'外链','ext')

    def testPhotoSearch(self):
        self.case_id = get_case(__file__)
        self.result = self.common_check(PHOTO_ARTICLE,u'组图','photo')

    def testTargeturlSearch(self):
        self.case_id = get_case(__file__)
        self.result = self.common_check(TARGETURL_ARTICLE,u'targeturl','targeturl')

    def testZhuantiSearch(self):
        self.case_id = get_case(__file__)
        self.result = self.common_check(ZHUANTI_ARTICLE,u'专题','zhuanti')

    def testZhuanlanSearch(self):
        self.case_id = get_case(__file__)
        self.result = self.common_check(ZHUANLAN_ARTICLE,u'专栏','zhuanlan')

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

