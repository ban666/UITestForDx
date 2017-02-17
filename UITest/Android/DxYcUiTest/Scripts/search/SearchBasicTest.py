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

class SearchBasicTest(unittest.TestCase):

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

    def common_check(self,article,model):
        step = 1
        try:
            model = model.decode('gbk')
        except:
            pass
        #搜索文章并检查样式
        get_to_article_by_search(self.driver,article,self.mode)
        sleep(WAIT_TIME)
        print self.driver.current_activity
        assert self.driver.current_activity == ACTIVITY.get(article)
        print u'Step %s: %s新闻能够搜索并查看测试：OK' % (str(step),model)
        step+=1

    def ext_check(self,article):
        step = 1

        #搜索文章并检查样式
        get_to_article_by_search(self.driver,article)
        sleep(WAIT_TIME)
        #print self.driver.current_activity
        assert element_exsist(self.driver,'id',COMMENT_INPUT)
        assert self.driver.current_activity == ACTIVITY.get(EXT_ARTICLE)
        print u'Step %s:外链新闻能够搜索并查看测试：OK' % (str(step))
        step+=1

    def targeturl_check(self,article):
        step = 1

        #搜索文章并检查样式
        get_to_article_by_search(self.driver,article)
        sleep(WAIT_TIME)
        print self.driver.current_activity
        assert element_exsist(self.driver,'id',COMMENT_INPUT) == False
        assert self.driver.current_activity == ACTIVITY.get(EXT_ARTICLE)
        print u'Step %s:TargetUrl新闻能够搜索并查看测试：OK' % (str(step))
        step+=1

    def testArticleSearch(self):
        self.common_check(NORMAL_ARTICLE,u'普通文字')

    def testVideoSearch(self):
        self.common_check(VIDEO_ARTICLE,u'视频')

    def testAudioSearch(self):
        self.common_check(AUDIO_ARTICLE,u'音频')

    def testExtSearch(self):
        self.ext_check(EXT_ARTICLE)

    def testPhotoSearch(self):
        self.common_check(PHOTO_ARTICLE,u'组图')

    def testTargeturlSearch(self):
        self.targeturl_check(TARGETURL_ARTICLE)

    def testZhuantiSearch(self):
        self.common_check(ZHUANTI_ARTICLE,u'专题')

    def testZhuanlanSearch(self):
        self.common_check(ZHUANLAN_ARTICLE,u'专栏')

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

