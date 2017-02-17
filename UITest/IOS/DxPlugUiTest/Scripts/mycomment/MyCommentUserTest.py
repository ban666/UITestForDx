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


class MyCommentBasicTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.mode = MODE
        self.db = DbLib()
        self.new_phone = '13187654321'
        self.db.delete_user_by_phone(self.new_phone)
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        start_to_index(self.driver,self.mode)
        sleep(WAIT_TIME)
        if is_login(self.driver):
            logout_to_index(self.driver,self.mode)


    def tearDown(self):
        print 'Test End...................................'
        try:
            self.driver.quit()
            self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
            start_to_index(self.driver,self.mode)
            sleep(WAIT_TIME)
            if is_login(self.driver):
                logout_to_index(self.driver,self.mode)
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down'
        finally:
            self.db.delete_user_by_phone(self.new_phone)

    def common_check(self,content,quote_content):
        step = 1

        login_to_index(self.driver,self.new_phone)
        sleep(WAIT_TIME)
        go_to_mycomm(self.driver,self.mode)
        sleep(WAIT_TIME)
        #对此评论点赞
        reply_info = get_comment_info(self.driver,1,True) #[点赞次数，地理位置_时间，评论用户名，评论内容，引用用户名，引用评论详情]
        assert reply_info['quote_content'] == content
        assert reply_info['content'] == quote_content
        print u'Step %s:我的评论-发布评论 未登录评论同步到新账号测试结果：OK' % (str(step))
        step+=1

        self.driver.find_element(*MY_COMM_REPLY).click()
        slide_down(self.driver,2)
        sleep(WAIT_TIME)
        reply_info = get_comment_info(self.driver,1,True,True) #[点赞次数，地理位置_时间，评论用户名，评论内容，引用用户名，引用评论详情]
        assert reply_info['quote_content'] == content
        assert reply_info['content'] == quote_content
        print u'Step %s:我的评论-回复评论 未登录评论同步到新账号测试结果：OK' % (str(step))
        step+=1


    def old_user_check(self,content,quote_content):
        step = 1

        login_to_index(self.driver,TEST_PHONE)
        sleep(WAIT_TIME)
        go_to_mycomm(self.driver,self.mode)
        sleep(WAIT_TIME)
        #对此评论点赞
        reply_info = get_comment_info(self.driver,1,True) #[点赞次数，地理位置_时间，评论用户名，评论内容，引用用户名，引用评论详情]
        assert reply_info['content'] != quote_content
        print u'Step %s:我的评论-发布评论 登录老账号后不显示未登录时发布的评论测试结果：OK' % (str(step))
        step+=1

        self.driver.find_element(*MY_COMM_REPLY).click()
        slide_down(self.driver,2)
        sleep(WAIT_TIME)
        reply_info = get_comment_info(self.driver,1,True,True) #[点赞次数，地理位置_时间，评论用户名，评论内容，引用用户名，引用评论详情]
        assert reply_info['content'] != quote_content
        print u'Step %s:我的评论-回复评论 登录老账号后不显示未登录时发布的评论测试结果：OK' % (str(step))
        step+=1

    #excute TestCase
    def testNewUser(self):
        article = NORMAL_ARTICLE
        content = u'评论'+str(randint(1,1000))
        quote_content = u'回复评论'+str(randint(1,1000))
        assert get_to_article_by_search(self.driver,article)
        go_to_comment_page(self.driver)
        send_comment(self.driver,content)
        comment_handle(self.driver,1,'reply',content=quote_content)
        back(self.driver)
        search_article_to_index(self.driver)
        self.common_check(content,quote_content)

    def testUser(self):
        article = NORMAL_ARTICLE
        content = u'评论'+str(randint(1,1000))
        quote_content = u'回复评论'+str(randint(1,1000))
        assert get_to_article_by_search(self.driver,article)
        go_to_comment_page(self.driver)
        send_comment(self.driver,content)
        comment_handle(self.driver,1,'reply',content=quote_content)
        back(self.driver)
        search_article_to_index(self.driver)
        self.old_user_check(content,quote_content)



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

