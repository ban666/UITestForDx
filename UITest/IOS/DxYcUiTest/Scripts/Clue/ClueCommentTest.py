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
from configrw import get_case
from TestlinkHandler import TestlinkHandler
from ui_clue import *
from BaoliaoRequest import BaoliaoRequest

class SubTypeTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.result = 'f'
        self.msg = ''
        self.tsl = TestlinkHandler()
        self.mode = MODE
        self.db = DbLib()
        self.clue = BaoliaoRequest()
        st = self.clue.get_clue_type()[0]['subtype']
        self.clue.send_clue_and_review(u'报料测试'+str(randint(1,100)),1,st)
        self.api = ChnlRequest(MODE)
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        start_to_index(self.driver,self.mode)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.tsl.set_tc_status(self.case_id,self.result,self.msg)
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self,driver):
        step = 1
        sleep(WAIT_TIME)
        go_to_clue(self.driver)

        self.driver.find_element_by_id(CLUE_LIST_DESC).click()
        sleep(WAIT_TIME)

        #发表评论
        content = u'中文'+str(randint(1,100))
        #content = u'一'*140
        send_comment(driver,content)
        sleep(5)
        new_comment = driver.find_element_by_id(COMMENT)
        info = get_comment_info(driver,new_comment,0)
        check_reply_elements = check_comment(driver,new_comment)
        assert check_reply_elements == 1
        assert info[3] == content
        print u'Step %s:发表评论测试结果：OK' % (str(step))
        step+=1

        #对此评论点赞
        find_first_comment_and_support(driver)
        first_CLUE_DETAIL_COMMENT_DIGG_COUNT = driver.find_elements_by_id(CLUE_DETAIL_COMMENT_DIGG_COUNT)[1].text
        assert first_CLUE_DETAIL_COMMENT_DIGG_COUNT == '1'
        print u'Step %s:评论气泡点赞测试结果：OK' % (str(step))
        step+=1

        #复制评论
        find_first_comment_and_copy(driver,0)
        assert check_copy_content_by_reply(driver,content)
        print u'Step %s:复制评论测试结果：OK' % (str(step))
        step+=1

        #回复评论
        quote_content = u'回复评论'+str(randint(1,100))
        # quote_content = u'二'*140
        find_first_comment_and_reply(driver,quote_content)
        reply_comment = driver.find_element_by_id(COMMENT)
        reply_info = get_comment_info(driver,reply_comment,1) #[点赞次数，地理位置_时间，评论用户名，评论内容，引用用户名，引用评论详情]
        assert reply_info[-1] == content
        assert reply_info[3] == quote_content
        print u'Step %s:回复评论测试结果：OK' % (str(step))
        step+=1

        #复制外部评论
        find_first_comment_and_copy(driver,1)
        assert check_copy_content_by_reply(driver,quote_content)
        print u'Step %s:嵌套评论-复制外部评论测试结果：OK' % (str(step))
        step+=1

        #复制嵌套内部评论
        find_first_comment_and_copy(driver,0)
        assert check_copy_content_by_reply(driver,content)
        print u'Step %s:嵌套评论-复制嵌套内部评论测试结果：OK' % (str(step))
        step+=1

        #回复嵌套评论-嵌套外评论
        quote_content_reply = u'回复嵌套外评论'+str(randint(1,100))
        find_first_comment_and_reply(driver,quote_content_reply,1)
        reply_comment = driver.find_element_by_id(COMMENT)
        reply_info = get_comment_info(driver,reply_comment,1) #[点赞次数，地理位置_时间，评论用户名，评论内容，引用用户名，引用评论详情]
        assert reply_info[-1] == quote_content
        assert reply_info[3] == quote_content_reply
        print u'Step %s:嵌套评论-回复嵌套外评论测试结果：OK' % (str(step))
        step+=1

        #回复嵌套评论-嵌套内评论
        content_reply = u'回复嵌套内评论'+str(randint(1,100))
        find_first_comment_and_reply(driver,content_reply,0)
        reply_comment = driver.find_element_by_id(COMMENT)
        reply_info = get_comment_info(driver,reply_comment,1) #[点赞次数，地理位置_时间，评论用户名，评论内容，引用用户名，引用评论详情]
        assert reply_info[-1] == quote_content
        assert reply_info[3] == content_reply
        print u'Step %s:嵌套评论-回复嵌套内评论测试结果：OK' % (str(step))
        step+=1

        #点赞嵌套内评论
        find_first_comment_and_support(driver,0)
        first_CLUE_DETAIL_COMMENT_DIGG_COUNT = driver.find_elements_by_id(CLUE_DETAIL_COMMENT_DIGG_COUNT)[3].text
        assert first_CLUE_DETAIL_COMMENT_DIGG_COUNT == '1'
        print u'Step %s:嵌套评论-嵌套评论内气泡点赞测试结果：OK' % (str(step))
        step+=1

        #点赞嵌套外评论
        find_first_comment_and_support(driver,1)
        first_CLUE_DETAIL_COMMENT_DIGG_COUNT = driver.find_elements_by_id(CLUE_DETAIL_COMMENT_DIGG_COUNT)[1].text
        assert first_CLUE_DETAIL_COMMENT_DIGG_COUNT == '1'
        print u'Step %s:嵌套评论-嵌套评论外气泡点赞测试结果：OK' % (str(step))
        step+=1


    #excute TestCase
    def test(self):
        self.case_id = get_case(__file__)
        self.result = self.common_check(self.driver)

if __name__ == '__main__':
    pass
    # a = TestLogin()
    # a.setUp()
    # a.testFunc1()
    # a.tearDown()
    #d =DbLib()

    bl = BaoliaoRequest()
    st = bl.get_clue_type()[0]['subtype']
    print st
    bl.send_clue_and_review(u'报料测试'+str(randint(1,100)),1,st,location='123')