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
from adb import *
from config import *
from elements_id import *
from common import exception_handler

class MyCommentPopupTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.mode = MODE
        self.db = DbLib()
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        start_to_index(self.driver,self.mode)
        if not is_login(self.driver):
            login_to_index(self.driver,TEST_PHONE)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down'

    def common_check(self,content,quote_content):
        step = 1

        go_to_mycomm(self.driver,self.mode)
        my_comment_handle(self.driver,1,'support')
        first_digg_count = get_comment_info(self.driver,1,True)['digg_count']
        assert first_digg_count == '1'
        print u'Step %s:我的评论-评论气泡点赞测试结果：OK' % (str(step))
        step+=1

        #复制评论
        my_comment_handle(self.driver,1,'copy')
        assert check_copy_content_in_my_comm(self.driver,quote_content)
        print u'Step %s:我的评论-复制评论测试结果：OK' % (str(step))
        step+=1

        #回复评论
        quote_content_2 = u'回复评论'+str(randint(1,100))
        my_comment_handle(self.driver,1,'reply',content=quote_content_2)
        reply_comment = get_comment_info(self.driver,1,True)
        assert reply_comment['content'] == quote_content_2
        assert reply_comment['quote_content'] == quote_content
        print u'Step %s:我的评论-回复评论测试结果：OK' % (str(step))
        step+=1
        print u'Step %s:我的评论气泡菜单测试：OK' % (str(step))
        step+=1


        self.driver.find_element(*MY_COMM_REPLY).click()
        my_comment_handle(self.driver,1,'support',reply=True)
        first_digg_count = get_comment_info(self.driver,1,True,reply=True)['digg_count']
        assert first_digg_count == '1'
        print u'Step %s:回复我的-评论气泡点赞测试结果：OK' % (str(step))
        step+=1

        #复制评论
        my_comment_handle(self.driver,1,'copy',reply=True)
        assert check_copy_content_in_my_comm(self.driver,quote_content_2,reply=True)
        print u'Step %s:回复我的-复制评论测试结果：OK' % (str(step))
        step+=1

        #回复评论
        quote_content_3 = u'回复评论'+str(randint(1,100))
        # quote_content = u'二'*140
        my_comment_handle(self.driver,1,'reply',content=quote_content_3,reply=True)
        reply_comment = get_comment_info(self.driver,1,True,reply=True)
        assert reply_comment['content'] == quote_content_3
        assert reply_comment['quote_content'] == quote_content_2
        print u'Step %s:回复我的-回复评论测试结果：OK' % (str(step))
        step+=1
        print u'Step %s:回复我的气泡菜单测试：OK' % (str(step))
        step+=1


    #excute TestCase
    def testMyComment(self):
        article = PHOTO_ARTICLE
        content = u'评论'+str(randint(1,1000))
        quote_content = u'回复评论'+str(randint(1,1000))
        assert get_to_article_by_search(self.driver,article)
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

