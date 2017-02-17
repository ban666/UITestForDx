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

class CommentForbiddenTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.result = 'f'
        self.msg = ''
        self.tsl = TestlinkHandler()
        self.mode = MODE
        self.db = DbLib()
        self.article_list = [NORMAL_ARTICLE,VIDEO_ARTICLE,EXT_ARTICLE,PHOTO_ARTICLE,AUDIO_ARTICLE]
        for article in self.article_list:
            self.db.close_comment_by_name(article)
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        start_to_index(self.driver,self.mode)
        # if not is_login(self.desired_caps['appPackage']):
        #     login_to_index(self.driver,TEST_PHONE)

    def tearDown(self):
        print 'Test End...................................'
        try:
            for article in self.article_list:
                self.db.open_comment_by_name(article)
            self.tsl.set_tc_status(self.case_id,self.result,self.msg)
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self,entrance=COMMENT_ENTRANCE):
        step = 1
        #验证评论框是否存在
        exsits = self.driver.find_element(*entrance).is_displayed()
        assert exsits == False
        print u'Step %s:禁止评论测试结果：OK' % (str(step))
        step+=1

        #验证左划手势
        slide_left(self.driver)
        sleep(WAIT_TIME)
        assert self.driver.find_element(*COLLECT_BUTTON).is_displayed()
        print u'Step %s:左划手势屏蔽测试结果：OK' % (str(step))
        step+=1

        return True

    def audio_check(self,entrance=COMMENT_ENTRANCE_AUDIO):
        step = 1
        #验证评论框是否存在
        exsits = self.driver.find_element(*entrance).is_displayed()
        assert exsits == False
        print u'Step %s:禁止评论测试结果：OK' % (str(step))
        step+=1

        #验证左划手势
        slide_left(self.driver)
        sleep(WAIT_TIME)
        assert self.driver.find_element(*COLLECT_BUTTON_TYPE_B).is_displayed()
        print u'Step %s:左划手势屏蔽测试结果：OK' % (str(step))
        step+=1

        return True

    def video_check(self):
        step = 1
        #验证评论框是否存在
        assert element_exsist(self.driver,*COMMENT_INPUT_IN_ARTICLE) == False
        # assert self.driver.find_element(*COMMENT_INPUT_IN_ARTICLE).is_displayed() == False
        print u'Step %s:禁止评论测试结果：OK' % (str(step))
        step+=1

        #视频列表提示语测试
        # tips = self.driver.find_element_by_id(VIDEO_FORBBIDEN_COMMENT).text
        # assert tips == u'对不起，此视频评论已关闭'
        # print u'Step %s:视频列表提示语测试结果：OK' % (str(step))
        # step+=1

        return True

    #excute TestCase
    def testVideoComment(self):
        get_to_article_by_search(self.driver,VIDEO_ARTICLE,self.mode)
        sleep(5)
        self.case_id = get_case(__file__)
        self.result = self.video_check()


    def testArticleComment(self):
        get_to_article_by_search(self.driver,NORMAL_ARTICLE,self.mode)
        sleep(5)
        self.case_id = get_case(__file__)
        self.result = self.common_check()

    def testPhotoComment(self):
        get_to_article_by_search(self.driver,PHOTO_ARTICLE,self.mode)
        sleep(5)
        self.case_id = get_case(__file__)
        self.result = self.audio_check(COMMENT_ENTRANCE)

    def testExtComment(self):
        get_to_article_by_search(self.driver,EXT_ARTICLE,self.mode)
        sleep(5)
        self.case_id = get_case(__file__)
        self.result = self.common_check()

    def testAudioComment(self):
        get_to_article_by_search(self.driver,AUDIO_ARTICLE,self.mode)
        sleep(5)
        self.case_id = get_case(__file__)
        self.result = self.audio_check()

if __name__ == '__main__':

    db = DbLib()
    article_list = [NORMAL_ARTICLE,VIDEO_ARTICLE,EXT_ARTICLE,PHOTO_ARTICLE,AUDIO_ARTICLE]
    for article in article_list:
                db.close_comment_by_name(article)
