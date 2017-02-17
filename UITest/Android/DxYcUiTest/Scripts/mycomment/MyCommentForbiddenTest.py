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
from adb import *
from config import *
from config import ACTIVITY
from elements_id import *
from common import exception_handler


class MyCommentJumpTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.mode = MODE
        self.db = DbLib()
        self.article_list = [NORMAL_ARTICLE,VIDEO_ARTICLE,EXT_ARTICLE,PHOTO_ARTICLE,AUDIO_ARTICLE]
        for article in self.article_list:
            self.db.open_comment_by_name(article)
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        start_to_index(self.driver,self.mode)
        if not is_login(self.driver):
            login_to_index(self.driver,self.mode,self.desired_caps['appPackage'],TEST_PHONE,DEVICE_TID)
        dc = get_config_by_adb()['dc']
        self.api = ChnlRequest(self.mode,dc=dc)
        self.first_article = self.api.get_first_chnl_article_by_model(13)
        self.db.change_comment_state_by_db(self.first_article['infoid'],2)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.db.change_comment_state_by_db(self.first_article['infoid'],0)
            for article in self.article_list:
                self.db.open_comment_by_name(article)
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self,article,info_str,content):
        step = 1
        try:
            info_str = info_str.decode('gbk')
        except:
            pass
        go_to_mycomm(self.driver,self.mode)
        self.db.close_comment_by_name(article)

        #回复评论
        quote_content = u'禁止评论测试'+str(randint(1,100))
        find_first_comment_and_reply(self.driver,quote_content)
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',COMMENT_EDIT_TEXT)
        assert self.driver.find_element_by_id(COMMENT_EDIT_TEXT).text == quote_content
        print u'Step %s:%s 禁止评论测试结果：OK' % (str(step),info_str)
        step+=1

        self.db.open_comment_by_name(article)

    def clue_check(self,clue_id,info_str,content):
        step = 1
        try:
            info_str = info_str.decode('gbk')
        except:
            pass
        go_to_mycomm(self.driver,self.mode)
        self.db.change_comment_state_by_db(clue_id,1)

        #回复评论
        quote_content = u'禁止评论测试'+str(randint(1,100))
        find_first_comment_and_reply(self.driver,quote_content)
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',COMMENT_EDIT_TEXT)
        assert self.driver.find_element_by_id(COMMENT_EDIT_TEXT).text == quote_content
        print u'Step %s:%s 禁止评论测试结果：OK' % (str(step),info_str)
        step+=1

        self.db.change_comment_state_by_db(clue_id,0)

    #excute TestCase
    def testMyCommentArticle(self):
        article = NORMAL_ARTICLE
        info_str = u'新闻'
        content = u'A'+str(randint(1,100))
        comid = self.api.send_comment_by_name(article,content)
        activity = ACTIVITY[article]
        self.common_check(article,info_str,content)

    def testMyCommentArticlePhoto(self):
        article = PHOTO_ARTICLE
        info_str = u'组图'
        content = 'A'+str(randint(1,100))
        comid = self.api.send_comment_by_name(article,content)
        activity = ACTIVITY[article]
        self.common_check(article,info_str,content)

    def testMyCommentArticleExt(self):
        article = EXT_ARTICLE
        info_str = u'外链'
        content = 'A'+str(randint(1,100))
        comid = self.api.send_comment_by_name(article,content)
        activity = ACTIVITY[article]
        self.common_check(article,info_str,content)

    def testMyCommentArticleVideo(self):
        article = VIDEO_ARTICLE
        info_str = u'视频'
        content = 'A'+str(randint(1,100))
        comid = self.api.send_comment_by_name(article,content)
        activity = ACTIVITY[article]
        self.common_check(article,info_str,content)

    def testMyCommentArticleAudio(self):
        article = AUDIO_ARTICLE
        info_str = u'音频'
        content = 'A'+str(randint(1,100))
        comid = self.api.send_comment_by_name(article,content)
        #print comid
        activity = ACTIVITY[article]
        self.common_check(article,info_str,content)

    #head
    def testMyCommentClue(self):
        article = 'clue'
        info_str = u'报料'
        content = 'A'+str(randint(1,100))
        clue_id = self.db.get_first_clue(4)
        comid = self.api.send_comment(clue_id,'A'+str(randint(1,100)))
        activity = ACTIVITY.get(article)
        self.clue_check(clue_id,info_str,content)

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

