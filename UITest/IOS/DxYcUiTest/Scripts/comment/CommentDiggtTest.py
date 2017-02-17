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

class CommentDiggtTest(unittest.TestCase):

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

    def common_check(self,driver,input=COMMENT_INPUT_BUTTON):
        step = 1
        #发表评论
        # content = u'A'+str(randint(1,100))
        # send_comment(driver,content)
        # sleep(5)
        # info = get_comment_info(driver,1)
        # assert info['content'] == content
        # print u'Step %s:发表评论A：OK' % (str(step))
        # step+=1


        #对此评论气泡点赞
        comment_handle(driver,1,'support')
        first_digg_count = get_comment_info(driver,1)['digg_count']
        assert first_digg_count == '1'
        print u'Step %s:评论气泡点赞测试结果：OK' % (str(step))
        step+=1

        #对此评论气泡重复点赞
        comment_handle(driver,1,'support')
        first_digg_count = get_comment_info(driver,1)['digg_count']
        assert first_digg_count == '1'
        print u'Step %s:评论气泡重复点赞测试结果：OK' % (str(step))
        step+=1

        #发表评论B
        content = u'点赞测试B'+str(randint(1,100))
        send_comment(driver,content,input)
        sleep(5)
        info = get_comment_info(driver,1)
        assert info['content'] == content
        print u'Step %s:发表评论B：OK' % (str(step))
        step+=1

        #对此评论按钮点赞
        comment_handle(driver,1,'digg')
        first_digg_count = get_comment_info(driver,1)['digg_count']
        assert first_digg_count == '1'
        print u'Step %s:评论按钮点赞测试结果：OK' % (str(step))
        step+=1

        #对此评论按钮重复点赞
        comment_handle(driver,1,'digg')
        first_digg_count = get_comment_info(driver,1)['digg_count']
        assert first_digg_count == '1'
        print u'Step %s:评论按钮重复点赞测试结果：OK' % (str(step))
        step+=1

        return True

    #excute TestCase
    def testVideoComment(self):
        article = VIDEO_ARTICLE
        self.comid = self.api.send_comment_by_name(article,'digg count test')
        assert get_to_article_by_search(self.driver,article)
        
        self.case_id = get_case(__file__)
        self.result = self.common_check(self.driver,COMMENT_INPUT_IN_ARTICLE)

    def testArticleComment(self):
        article = NORMAL_ARTICLE
        self.comid = self.api.send_comment_by_name(article,'digg count test')
        assert get_to_article_by_search(self.driver,article)
        
        go_to_comment_page(self.driver)
        self.case_id = get_case(__file__)
        self.result = self.common_check(self.driver)

    def testPhotoComment(self):
        article = PHOTO_ARTICLE
        self.comid = self.api.send_comment_by_name(article,'digg count test')
        assert get_to_article_by_search(self.driver,article)
        
        go_to_comment_page(self.driver)
        self.case_id = get_case(__file__)
        self.result = self.common_check(self.driver)

    def testExtComment(self):
        article = EXT_ARTICLE
        self.comid = self.api.send_comment_by_name(article,'digg count test')
        assert get_to_article_by_search(self.driver,article)
        
        go_to_comment_page(self.driver)
        self.case_id = get_case(__file__)
        self.result = self.common_check(self.driver)

    def testAudioComment(self):
        article = AUDIO_ARTICLE
        self.comid = self.api.send_comment_by_name(article,'digg count test')
        assert get_to_article_by_search(self.driver,article)
        
        go_to_comment_page(self.driver,COMMENT_ENTRANCE_AUDIO)
        self.case_id = get_case(__file__)
        self.result = self.common_check(self.driver)

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

