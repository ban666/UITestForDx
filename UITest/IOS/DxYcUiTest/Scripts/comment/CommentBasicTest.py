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
from config import *
from elements_id import *
from common import exception_handler
from configrw import get_case
from TestlinkHandler import TestlinkHandler

class CommentBasicTest(unittest.TestCase):

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
        self.first_article = self.db.get_infoid_by_article_name(VIDEO_ARTICLE)
        self.db.change_comment_state_by_db(self.first_article,2)
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        start_to_index(self.driver,self.mode)
        # if not is_login(self.desired_caps['appPackage']):
        #     login_to_index(self.driver,TEST_PHONE)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.tsl.set_tc_status(self.case_id,self.result,self.msg)
            self.db.change_comment_state_by_db(self.first_article,0)
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self,driver,input_button=COMMENT_INPUT_BUTTON):
        step = 1
        #发表评论
        content = u'中文'+str(randint(1,100))
        send_comment(driver,content,input_button)
        sleep(5)
        info = get_comment_info(driver,1)
        check_elements = ['content','author','loc_time','digg_count']
        assert check_elements.sort() == info.keys().sort()
        assert info['content'] == content
        print u'Step %s:发表评论测试结果：OK' % (str(step))
        step+=1

        #对此评论点赞
        comment_handle(driver,1,'support')
        first_digg_count = get_comment_info(driver,1)['digg_count']
        assert first_digg_count == '1'
        print u'Step %s:评论气泡点赞测试结果：OK' % (str(step))
        step+=1

        #复制评论
        comment_handle(driver,1,'copy')
        assert check_copy_content(driver,content,input_button)
        print u'Step %s:复制评论测试结果：OK' % (str(step))
        step+=1

        #回复评论
        quote_content = u'回复评论'+str(randint(1,100))
        # quote_content = u'二'*140
        comment_handle(driver,1,'reply',content=quote_content)
        reply_comment = get_comment_info(driver,1)
        assert reply_comment['content'] == quote_content
        assert reply_comment['quote_content'] == content
        print u'Step %s:回复评论测试结果：OK' % (str(step))
        step+=1

        #复制外部评论
        comment_handle(driver,1,'copy')
        assert check_copy_content(driver,quote_content,input_button)
        print u'Step %s:嵌套评论-复制外部评论测试结果：OK' % (str(step))
        step+=1

        #复制嵌套内部评论
        comment_handle(driver,1,'copy',quote=True)
        assert check_copy_content(driver,content,input_button)
        print u'Step %s:嵌套评论-复制嵌套内部评论测试结果：OK' % (str(step))
        step+=1

        #回复嵌套评论-嵌套外评论
        quote_content_reply = u'回复嵌套外评论'+str(randint(1,100))
        comment_handle(driver,1,'reply',content=quote_content_reply)
        reply_info = get_comment_info(driver,1) #[点赞次数，地理位置_时间，评论用户名，评论内容，引用用户名，引用评论详情]
        assert reply_info['quote_content'] == quote_content
        assert reply_info['content'] == quote_content_reply
        print u'Step %s:嵌套评论-回复嵌套外评论测试结果：OK' % (str(step))
        step+=1

        #回复嵌套评论-嵌套内评论
        content_reply = u'回复嵌套内评论'+str(randint(1,100))
        comment_handle(driver,1,'reply',quote=True,content=content_reply)
        reply_info = get_comment_info(driver,1) #[点赞次数，地理位置_时间，评论用户名，评论内容，引用用户名，引用评论详情]
        assert reply_info['quote_content'] == quote_content
        assert reply_info['content'] == content_reply
        print u'Step %s:嵌套评论-回复嵌套内评论测试结果：OK' % (str(step))
        step+=1

        #点赞嵌套内评论
        comment_handle(driver,1,'support',quote=True)
        first_digg_count = get_comment_info(driver,3)['digg_count']
        assert first_digg_count == '1'
        print u'Step %s:嵌套评论-嵌套评论内气泡点赞测试结果：OK' % (str(step))
        step+=1

        #点赞嵌套外评论
        comment_handle(driver,1,'support')
        first_digg_count = get_comment_info(driver,1)['digg_count']
        assert first_digg_count == '1'
        print u'Step %s:嵌套评论-嵌套评论外气泡点赞测试结果：OK' % (str(step))
        step+=1

        return True

    #excute TestCase
    #TODO dianzan bu tongping
    def testVideoComment(self):
        assert get_to_article_by_search(self.driver,VIDEO_ARTICLE)
        self.case_id = get_case(__file__)
        self.result = self.common_check(self.driver,input_button=COMMENT_INPUT_IN_ARTICLE)

    def testArticleComment(self):
        assert get_to_article_by_search(self.driver,NORMAL_ARTICLE)
        go_to_comment_page(self.driver)
        self.case_id = get_case(__file__)
        self.result = self.common_check(self.driver)

    def testPhotoComment(self):
        assert get_to_article_by_search(self.driver,PHOTO_ARTICLE)
        go_to_comment_page(self.driver)
        self.case_id = get_case(__file__)
        self.result = self.common_check(self.driver)

    def testExtComment(self):
        assert get_to_article_by_search(self.driver,EXT_ARTICLE)
        go_to_comment_page(self.driver)
        self.case_id = get_case(__file__)
        self.result = self.common_check(self.driver)

    def testAudioComment(self):
        assert get_to_article_by_search(self.driver,AUDIO_ARTICLE,self.mode)
        go_to_comment_page(self.driver,COMMENT_ENTRANCE_AUDIO)
        self.case_id = get_case(__file__)
        self.result = self.common_check(self.driver)

    #SDK暂不支持
    # def testHeadComment(self):
    #     assert go_to_head(self.driver)
    #     self.driver.find_element_by_id(HEAD_REPLY_BUTTON).click()
    #     self.common_check(self.driver)

if __name__ == '__main__':
    pass
    # a = TestLogin()
    # a.setUp()
    # a.testFunc1()
    # a.tearDown()
    #d =DbLib()

    import HTMLTestRunner
    t = unittest.TestSuite()
    t.addTest(unittest.makeSuite(CommentBasicTest))
    unittest.TextTestRunner().run(t)
    filename = 'F:\\dx_comment.html'
    #fp = file(filename,'wb')
    # runner = HTMLTestRunner.HTMLTestRunner(
    #         stream = fp,
    #         title ='Dx_Test',
    #         description = 'Report_discription')

    #runner.run(t)
    #fp.close()

