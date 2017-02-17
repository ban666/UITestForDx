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
from ui_settings import *
from adb import *


class AnonymousMyCommentTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.mode = MODE
        self.db = DbLib()
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        start_to_index(self.driver,self.mode)
        if is_login(self.driver):
            logout_to_index(self.driver,self.mode)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down'

    def common_check(self,content,quote_content):
        step = 1

        go_to_mycomm(self.driver,self.mode)
        sleep(WAIT_TIME)
        #对此评论点赞
        #reply_comment = self.driver.find_element_by_id(COMMENT)
        reply_info = get_comment_info(self.driver,1,True)#[点赞次数，地理位置_时间，评论用户名，评论内容，引用用户名，引用评论详情]
        assert reply_info['content'] == quote_content
        assert reply_info['quote_content'] == content
        print u'Step %s:我的评论-发布评论 未登录评论测试结果：OK' % (str(step))
        step+=1

        self.driver.find_element(*MY_COMM_REPLY).click()
        slide_down(self.driver,2)
        reply_info = get_comment_info(self.driver,1,True,reply=True)#[点赞次数，地理位置_时间，评论用户名，评论内容，引用用户名，引用评论详情]
        assert reply_info['content'] == quote_content
        assert reply_info['quote_content'] == content
        print u'Step %s:我的评论-回复评论 未登录评回复评论测试结果：OK' % (str(step))
        step+=1



    #excute TestCase
    def testAnonymous(self):
        article = NORMAL_ARTICLE
        content = u'评论'+str(randint(1,1000))
        quote_content = u'回复评论'+str(randint(1,1000))
        assert get_to_article_by_search(self.driver,NORMAL_ARTICLE)
        go_to_comment_page(self.driver)
        send_comment(self.driver,content)
        comment_handle(self.driver,1,'reply',content=quote_content)
        back(self.driver)
        search_article_to_index(self.driver)
        self.common_check(content,quote_content)




if __name__ == '__main__':
    pass
    # a = TestLogin()
    # a.setUp()
    # a.testFunc1()
    # a.tearDown()
    #d =DbLib()

    import HTMLTestRunner
    t = unittest.TestSuite()
    t.addTest(unittest.makeSuite(AnonymousMyCommentTest))
    #unittest.TextTestRunner.run(t)
    filename = 'F:\\dx_comment.html'
    fp = file(filename,'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
            stream = fp,
            title ='Dx_Test',
            description = 'Report_discription')

    runner.run(t)
    fp.close()

