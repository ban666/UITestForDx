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
from ui_settings import *
from adb import *


class MyCommentBasicTest(unittest.TestCase):

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
        sleep(WAIT_TIME)
        #对此评论点赞
        my_comment_handle(self.driver,1,'support')
        first_digg_count = get_comment_info(self.driver,1,True)['digg_count']
        assert first_digg_count == '1'
        print u'Step %s:评论气泡点赞测试结果：OK' % (str(step))
        step+=1

        #复制评论
        my_comment_handle(self.driver,1,'copy')
        assert check_copy_content_in_my_comm(self.driver,content)
        print u'Step %s:复制评论测试结果：OK' % (str(step))
        step+=1

        #回复评论
        quote_content = u'回复评论'+str(randint(1,100))
        # quote_content = u'二'*140
        my_comment_handle(self.driver,1,'reply',content=quote_content)
        reply_comment = get_comment_info(self.driver,1,True)
        assert reply_comment['content'] == quote_content
        assert reply_comment['quote_content'] == content
        print u'Step %s:回复评论测试结果：OK' % (str(step))
        step+=1

        #复制外部评论
        my_comment_handle(self.driver,1,'copy')
        assert check_copy_content_in_my_comm(self.driver,quote_content)
        print u'Step %s:嵌套评论-复制外部评论测试结果：OK' % (str(step))
        step+=1

        #复制嵌套内部评论
        my_comment_handle(self.driver,1,'copy',quote=True)
        assert check_copy_content_in_my_comm(self.driver,content)
        print u'Step %s:嵌套评论-复制嵌套内部评论测试结果：OK' % (str(step))
        step+=1

        #回复嵌套评论-嵌套外评论
        quote_content_reply = u'回复嵌套外评论'+str(randint(1,100))
        my_comment_handle(self.driver,1,'reply',content=quote_content_reply)
        reply_info = get_comment_info(self.driver,1,True) #[点赞次数，地理位置_时间，评论用户名，评论内容，引用用户名，引用评论详情]
        assert reply_info['quote_content'] == quote_content
        assert reply_info['content'] == quote_content_reply
        print u'Step %s:嵌套评论-回复嵌套外评论测试结果：OK' % (str(step))
        step+=1

        #回复嵌套评论-嵌套内评论
        content_reply = u'回复嵌套内评论'+str(randint(1,100))
        my_comment_handle(self.driver,1,'reply',quote=True,content=content_reply)
        reply_info = get_comment_info(self.driver,1,True) #[点赞次数，地理位置_时间，评论用户名，评论内容，引用用户名，引用评论详情]
        assert reply_info['quote_content'] == quote_content
        assert reply_info['content'] == content_reply
        print u'Step %s:嵌套评论-回复嵌套内评论测试结果：OK' % (str(step))
        step+=1

        #点赞嵌套内评论
        my_comment_handle(self.driver,1,'support',quote=True)
        first_digg_count = get_comment_info(self.driver,3,True)['digg_count']
        assert first_digg_count == '1'
        print u'Step %s:嵌套评论-嵌套评论内气泡点赞测试结果：OK' % (str(step))
        step+=1

        #点赞嵌套外评论
        my_comment_handle(self.driver,1,'support')
        first_digg_count = get_comment_info(self.driver,1,True)['digg_count']
        assert first_digg_count == '1'
        print u'Step %s:嵌套评论-嵌套评论外气泡点赞测试结果：OK' % (str(step))
        step+=1

        return True


    #excute TestCase
    def testMyComment(self):
        article = NORMAL_ARTICLE
        content = u'评论'
        quote_content = u'回复评论'
        assert get_to_article_by_search(self.driver,NORMAL_ARTICLE)
        go_to_comment_page(self.driver)
        send_comment(self.driver,content)
        back(self.driver)
        search_article_to_index(self.driver)
        #self.api.send_comment_by_name(article,quote_content,comid)
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
    t.addTest(unittest.makeSuite(MyCommentBasicTest))
    #unittest.TextTestRunner.run(t)
    filename = 'F:\\dx_comment.html'
    fp = file(filename,'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
            stream = fp,
            title ='Dx_Test',
            description = 'Report_discription')

    runner.run(t)
    fp.close()

