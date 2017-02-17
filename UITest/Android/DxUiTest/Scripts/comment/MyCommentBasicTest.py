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


class MyCommentBasicTest(unittest.TestCase):

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
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self,content,quote_content):
        step = 1

        go_to_mycomm(self.driver,self.mode)
        #对此评论点赞
        find_first_comment_and_support(self.driver)
        first_digg_count = self.driver.find_element_by_id('com.zc.hubei_news:id/tv_digg').text
        assert first_digg_count == '1'
        print u'Step %s:评论气泡点赞测试结果：OK' % (str(step))
        step+=1

        #复制评论
        find_first_comment_and_copy(self.driver,0)
        assert check_copy_content_by_reply(self.driver,content)
        print u'Step %s:复制评论测试结果：OK' % (str(step))
        step+=1

        #回复评论
        quote_content = u'回复评论'+str(randint(1,100))
        # quote_content = u'二'*140
        find_first_comment_and_reply(self.driver,quote_content)
        self.driver.find_element_by_id(MY_COMM_REPLY).click()
        slide_down(self.driver,2)
        sleep(WAIT_TIME)
        reply_comment = self.driver.find_element_by_id('com.zc.hubei_news:id/rl_comment')
        reply_info = get_comment_info(self.driver,reply_comment,1) #[点赞次数，地理位置_时间，评论用户名，评论内容，引用用户名，引用评论详情]
        assert reply_info[-1] == content
        assert reply_info[3] == quote_content
        print u'Step %s:回复评论测试结果：OK' % (str(step))
        step+=1

        #复制外部评论
        find_first_comment_and_copy(self.driver,1)
        assert check_copy_content_by_reply(self.driver,quote_content)
        print u'Step %s:嵌套评论-复制外部评论测试结果：OK' % (str(step))
        step+=1

        #复制嵌套内部评论
        find_first_comment_and_copy(self.driver,0)
        assert check_copy_content_by_reply(self.driver,content)
        print u'Step %s:嵌套评论-复制嵌套内部评论测试结果：OK' % (str(step))
        step+=1

        #回复嵌套评论-嵌套外评论
        quote_content_reply = u'回复嵌套外评论'+str(randint(1,100))
        find_first_comment_and_reply(self.driver,quote_content_reply,1)
        reply_comment = self.driver.find_element_by_id('com.zc.hubei_news:id/rl_comment')
        reply_info = get_comment_info(self.driver,reply_comment,1) #[点赞次数，地理位置_时间，评论用户名，评论内容，引用用户名，引用评论详情]
        assert reply_info[-1] == quote_content
        assert reply_info[3] == quote_content_reply
        print u'Step %s:嵌套评论-回复嵌套外评论测试结果：OK' % (str(step))
        step+=1

        #回复嵌套评论-嵌套内评论
        content_reply = u'回复嵌套内评论'+str(randint(1,100))
        find_first_comment_and_reply(self.driver,content_reply,0)
        reply_comment = self.driver.find_element_by_id('com.zc.hubei_news:id/rl_comment')
        reply_info = get_comment_info(self.driver,reply_comment,1) #[点赞次数，地理位置_时间，评论用户名，评论内容，引用用户名，引用评论详情]
        assert reply_info[-1] == quote_content
        assert reply_info[3] == content_reply
        print u'Step %s:嵌套评论-回复嵌套内评论测试结果：OK' % (str(step))
        step+=1

        #点赞嵌套内评论
        find_first_comment_and_support(self.driver,0)
        first_digg_count = self.driver.find_elements_by_id('com.zc.hubei_news:id/tv_digg')[2].text
        assert first_digg_count == '1'
        print u'Step %s:嵌套评论-嵌套评论内气泡点赞测试结果：OK' % (str(step))
        step+=1

        #点赞嵌套外评论
        find_first_comment_and_support(self.driver,1)
        first_digg_count = self.driver.find_elements_by_id('com.zc.hubei_news:id/tv_digg')[0].text
        assert first_digg_count == '1'
        print u'Step %s:嵌套评论-嵌套评论外气泡点赞测试结果：OK' % (str(step))
        step+=1


    #excute TestCase
    def testMyComment(self):
        article = NORMAL_ARTICLE
        content = u'评论'
        quote_content = u'回复评论'
        comid = self.api.send_comment_by_name(article,content)
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

