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
from elements_id import *
from common import exception_handler
from configrw import get_case
from TestlinkHandler import TestlinkHandler


class ReplyCountTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.result = 'f'
        self.msg = ''
        self.tsl = TestlinkHandler()
        self.mode = MODE
        self.db = DbLib()
        self.api = ChnlRequest(self.mode)
        self.first_article = self.api.get_first_chnl_article_by_model(13)
        self.db.change_comment_state_by_db(self.first_article['infoid'],2)
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        start_to_index(self.driver,self.mode)
        # if not is_login(self.desired_caps['appPackage']):
        #     login_to_index(self.driver,self.mode,self.desired_caps['appPackage'],TEST_PHONE,DEVICE_TID)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.tsl.set_tc_status(self.case_id,self.result,self.msg)
            self.db.change_comment_state_by_db(self.first_article['infoid'],0)
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self,article):
        step = 1

        #获取原始评论数
        self.count = self.db.get_comment_count_by_name(article)

        #进入文章页
        get_to_article_by_search(self.driver,article,self.mode)

        #评论数为0显示测试
        self.db.change_comment_count_by_name(article,0)
        refresh_article(self.driver)
        article_count = self.driver.find_element_by_id(COMMENT_COUNT).text
        assert article_count == str(0)
        print u'Step %s:正文页评论数为0时显示测试：OK' % (str(step))
        step+=1

        #评论数为0-9999显示测试
        self.db.change_comment_count_by_name(article,999999)
        refresh_article(self.driver)
        article_count = self.driver.find_element_by_id(COMMENT_COUNT).text
        assert article_count == str(999999)
        print u'Step %s:正文页评论数为<=999999时显示测试：OK' % (str(step))
        step+=1


        #评论数大于1万小于10万显示测试
        self.db.change_comment_count_by_name(article,1000000)
        refresh_article(self.driver)
        article_count = self.driver.find_element_by_id(COMMENT_COUNT).text
        assert article_count == u'999999'
        print u'Step %s:正文页评论数大于999999时显示测试：OK' % (str(step))
        step+=1

        self.db.change_comment_count_by_name(article,self.count)

        return True

    def photo_check(self,article):
        step = 1

        #获取原始评论数
        self.count = self.db.get_comment_count_by_name(article)

        #进入文章页
        get_to_article_by_search(self.driver,article,self.mode)

        #评论数为0显示测试
        self.db.change_comment_count_by_name(article,0)
        refresh_article(self.driver)
        article_count = self.driver.find_element_by_id(COMMENT_PHOTO_ENTRANCE).text
        assert article_count == u'抢沙发'
        print u'Step %s:正文页评论数为0时显示测试：OK' % (str(step))
        step+=1

        #评论数为0-9999显示测试
        self.db.change_comment_count_by_name(article,999999)
        refresh_article(self.driver)
        article_count = self.driver.find_element_by_id(COMMENT_PHOTO_ENTRANCE).text
        assert article_count == str(999999)+u'评论'
        print u'Step %s:正文页评论数为<=999999时显示测试：OK' % (str(step))
        step+=1


        #评论数大于1万小于10万显示测试
        self.db.change_comment_count_by_name(article,1000000)
        refresh_article(self.driver)
        article_count = self.driver.find_element_by_id(COMMENT_PHOTO_ENTRANCE).text
        assert article_count == u'999999'+u'评论'
        print u'Step %s:正文页评论数大于999999时显示测试：OK' % (str(step))
        step+=1

        self.db.change_comment_count_by_name(article,self.count)

        return True

    #excute TestCase
    def testCommentArticle(self):
        article = NORMAL_ARTICLE
        self.case_id = get_case(__file__)
        self.result = self.common_check(article)

    def testCommentPhoto(self):
        article = PHOTO_ARTICLE
        self.case_id = get_case(__file__)
        self.result = self.photo_check(article)

    def testCommentAudio(self):
        article = AUDIO_ARTICLE
        self.case_id = get_case(__file__)
        self.result = self.photo_check(article)

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

