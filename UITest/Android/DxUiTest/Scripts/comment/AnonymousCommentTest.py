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
from config import *
from loglib import log

from config import TEST_PHONE,DEVICE_TID
from elements_id import *
from common import exception_handler

class AnonymousCommentTest(unittest.TestCase):

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
        if is_login(self.driver):
            logout_to_index(self.driver,self.mode)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.db.change_comment_state_by_db(self.first_article['id'],0)
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self):
        step = 1
        #匿名点击正文页评论框
        self.driver.find_element_by_id(COMMENT_INPUT).click()
        current_activity = self.driver.current_activity
        print u'当前activity：',current_activity
        back(self.driver)
        sleep(3)
        assert current_activity == 'com.cnhubei.dx.user.A_UserResigerActivity'
        print u'Step %s:匿名正文页评论跳转测试结果：OK' % (str(step))
        step+=1

        #匿名点击评论页评论框
        self.driver.find_element_by_id('com.zc.hubei_news:id/rl_coments').click()
        self.driver.find_element_by_id(COMMENT_INPUT).click()
        current_activity = self.driver.current_activity
        print u'当前activity：',current_activity
        back(self.driver)
        sleep(3)
        assert current_activity == 'com.cnhubei.dx.user.A_UserResigerActivity'
        print u'Step %s:匿名详情页评论跳转测试结果：OK' % (str(step))
        step+=1

    def video_check(self):
        step = 1
        #匿名点击正文页评论框
        new_comment = self.driver.find_element_by_id(COMMENT_INPUT_VIDEO)
        print self.driver.current_activity
        print u'Step %s:匿名点击评论测试结果：OK' % (str(step))
        step+=1

    def photo_check(self):
        step = 1
        #匿名点击评论页评论框
        self.driver.find_element_by_id('com.zc.hubei_news:id/rl_coments').click()
        self.driver.find_element_by_id(COMMENT_INPUT).click()
        current_activity = self.driver.current_activity
        print u'当前activity：',current_activity
        back(self.driver)
        sleep(3)
        assert current_activity == 'com.cnhubei.dx.user.A_UserResigerActivity'
        print u'Step %s:匿名详情页评论跳转测试结果：OK' % (str(step))
        step+=1

    def head_check(self):
        step = 1
        #匿名点击评论页评论框
        self.driver.find_element_by_id(HEAD_REPLY_BUTTON).click()
        self.driver.find_element_by_id(COMMENT_INPUT).click()
        current_activity = self.driver.current_activity
        print u'当前activity：',current_activity
        back(self.driver)
        sleep(3)
        assert current_activity == 'com.cnhubei.dx.user.A_UserResigerActivity'
        print u'Step %s:匿名详情页评论跳转测试结果：OK' % (str(step))
        step+=1


    #excute TestCase
    def testVideoComment(self):
        get_to_article_by_search(self.driver,u'自动化视频新闻',self.mode)
        self.video_check()

    def testArticleComment(self):
        get_to_article_by_search(self.driver,u'自动化文字新闻',self.mode)
        self.common_check()

    def testPhotoComment(self):
        get_to_article_by_search(self.driver,u'自动化组图新闻',self.mode)
        self.photo_check()

    def testExtComment(self):
        get_to_article_by_search(self.driver,u'自动化外链新闻',self.mode)
        self.common_check()

    def testHeadComment(self):
        assert go_to_head(self.driver)
        self.head_check()


if __name__ == '__main__':
    pass
    # a = TestLogin()
    # a.setUp()
    # a.testFunc1()
    # a.tearDown()
    #d =DbLib()
    __import__('AnonymousCommentTest')
    # import HTMLTestRunner
    # t = unittest.TestSuite()
    # t.addTest(unittest.makeSuite(TestComment))
    # #unittest.TextTestRunner.run(t)
    # filename = 'F:\\dx_comment.html'
    # fp = file(filename,'wb')
    # runner = HTMLTestRunner.HTMLTestRunner(
    #         stream = fp,
    #         title ='Dx_Test',
    #         description = 'Report_discription')
    #
    # runner.run(t)
    # fp.close()

