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


class MyCommentDiggCountTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.mode = 'mcp/dx'
        self.db = DbLib()
        self.api = ChnlRequest(self.mode)
        self.first_article = self.api.get_first_chnl_article_by_model(13)
        self.db.change_comment_state_by_db(self.first_article['id'],2)
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        start_to_index(self.driver,self.mode)
        if not is_login(self.driver):
            login_to_index(self.driver,self.mode,self.desired_caps['appPackage'],TEST_PHONE,DEVICE_TID)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.db.change_comment_state_by_db(self.first_article['id'],0)
            self.db.set_digg_count_by_db(self.comid, 0)
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self,article=u'自动化文字新闻'):
        step = 1

        #发送评论
        self.comid = self.api.send_comment_by_name(article,'digg count test')
        #print self.comid
        #进入文章页
        go_to_mycomm(self.driver,self.mode)

        #点赞数<=9999显示测试
        self.db.set_digg_count_by_db(self.comid, 9999)
        slide_down(self.driver,3)
        sleep(3)
        article_count = self.driver.find_element_by_id(DIGG_COUNT).text
        
        assert article_count == u'9999'
        print u'Step %s:评论点赞数为<=9999时显示测试：OK' % (str(step))
        step+=1

        #评论数大于1万小于10万显示测试
        self.db.set_digg_count_by_db(self.comid, 10001)
        slide_down(self.driver,3)
        sleep(3)
        article_count = self.driver.find_element_by_id(DIGG_COUNT).text
        
        assert article_count == u'1万'

        #评论数大于1万小于10万显示测试
        self.db.set_digg_count_by_db(self.comid, 10500)
        slide_down(self.driver,3)
        sleep(3)
        article_count = self.driver.find_element_by_id(DIGG_COUNT).text
        
        assert article_count == u'1.1万'

        #评论数大于1万小于10万显示测试
        self.db.set_digg_count_by_db(self.comid, 99999)
        slide_down(self.driver,3)
        sleep(3)
        article_count = self.driver.find_element_by_id(DIGG_COUNT).text
        
        assert article_count == u'10万'
        print u'Step %s:正文页评论数大于1万小于10万时显示测试：OK' % (str(step))
        step+=1

        #评论数大于10万显示测试
        self.db.set_digg_count_by_db(self.comid, 100001)
        slide_down(self.driver,3)
        sleep(3)
        article_count = self.driver.find_element_by_id(DIGG_COUNT).text
        
        assert article_count == u'10万'

        self.db.set_digg_count_by_db(self.comid, 105001)
        slide_down(self.driver,3)
        sleep(3)
        article_count = self.driver.find_element_by_id(DIGG_COUNT).text
        
        assert article_count == u'11万'

        self.db.set_digg_count_by_db(self.comid, 995001)
        slide_down(self.driver,3)
        sleep(3)
        article_count = self.driver.find_element_by_id(DIGG_COUNT).text
        
        assert article_count == u'99万'
        print u'Step %s:正文页评论数大于10万小于100万时显示测试：OK' % (str(step))
        step+=1

        self.db.set_digg_count_by_db(self.comid, 1005001)
        slide_down(self.driver,3)
        sleep(3)
        article_count = self.driver.find_element_by_id(DIGG_COUNT).text
        
        assert article_count == u'99万'
        print u'Step %s:正文页评论数大于100万时显示测试：OK' % (str(step))
        step+=1

    #excute TestCase
    def testMyCommentArticle(self):
        self.common_check()

    def testMyCommentArticlePhoto(self):
        article = NORMAL_ARTICLE
        self.common_check(article)

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

