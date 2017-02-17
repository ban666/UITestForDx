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

    def common_check(self,article):
        step = 1


        #对此评论点赞

        #回复评论
        content = u'评论'+str(randint(1,1000))
        assert get_to_article_by_search(self.driver,article)
        go_to_comment_page(self.driver)
        send_comment(self.driver,content)
        back(self.driver)
        search_article_to_index(self.driver)

        go_to_mycomm(self.driver,self.mode)
        sleep(WAIT_TIME)

        quote_content = u'二'*141
        my_comment_handle(self.driver,1,'reply',content=quote_content)
        sleep(WAIT_TIME)
        reply_info = get_comment_info(self.driver,1,True) #[点赞次数，地理位置_时间，评论用户名，评论内容，引用用户名，引用评论详情]
        assert reply_info['quote_content'] == content
        assert reply_info['content'] == quote_content[:140]
        print u'Step %s:我的评论-发布评论最大字数140测试结果：OK' % (str(step))
        step+=1

        self.driver.find_element(*MY_COMM_REPLY).click()
        slide_down(self.driver,2)
        sleep(WAIT_TIME)
        reply_info = get_comment_info(self.driver,1,True) #[点赞次数，地理位置_时间，评论用户名，评论内容，引用用户名，引用评论详情]
        assert reply_info['quote_content'] == content
        assert reply_info['content'] == quote_content[:140]
        print u'Step %s:我的评论-回复评论最大字数140测试结果：OK' % (str(step))
        step+=1



    #excute TestCase
    def testMyComment(self):
        article = NORMAL_ARTICLE
        #self.api.send_comment_by_name(article,quote_content,comid)
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

