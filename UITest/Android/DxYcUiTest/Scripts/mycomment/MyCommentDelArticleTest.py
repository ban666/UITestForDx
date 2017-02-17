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


class MyCommentDelArticleTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.mode = MODE
        self.db = DbLib()
        self.article_list = [NORMAL_ARTICLE,VIDEO_ARTICLE,EXT_ARTICLE,PHOTO_ARTICLE,AUDIO_ARTICLE]
        for article in self.article_list:
            infoid = self.db.get_infoid_by_article_name(article)
            self.db.publish_del_article_by_db(infoid)
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
            for article in self.article_list:
                infoid = self.db.get_infoid_by_article_name(article)
                self.db.publish_del_article_by_db(infoid)
            self.db.change_comment_state_by_db(self.first_article['infoid'],0)
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self,article,info_str):
        step = 1
        try:
            info_str = info_str.decode('gbk')
        except:
            pass
        sleep(WAIT_TIME)
        go_to_mycomm(self.driver,self.mode)
        infoid = self.db.get_infoid_by_article_name(article)
        self.db.del_article_by_db(infoid)

        self.driver.find_element_by_id(COMM_SRC).click()
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',ARTICLE_EMPTY_TIPS)
        assert self.driver.find_element_by_id(ARTICLE_EMPTY_TIPS).text == u'内容不存在,无法查看'
        back(self.driver)
        print u'Step %s:我的评论-发布评论%s原文被删除时，点击查看原文能够正确提示测试：OK' % (str(step),info_str)
        step+=1

        self.driver.find_element_by_id(MY_COMM_REPLY).click()
        self.driver.find_element_by_id(COMM_SRC).click()
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',ARTICLE_EMPTY_TIPS)
        assert self.driver.find_element_by_id(ARTICLE_EMPTY_TIPS).text == u'内容不存在,无法查看'
        print u'Step %s:我的评论-回复评论%s原文被删除时，点击查看原文能够正确提示测试：OK' % (str(step),info_str)
        step+=1

        self.db.publish_del_article_by_db(infoid)

    def clue_check(self,clue_id,info_str):
        step = 1
        try:
            info_str = info_str.decode('gbk')
        except:
            pass
        sleep(WAIT_TIME)
        go_to_mycomm(self.driver,self.mode)
        self.db.del_article_by_db(clue_id)

        self.driver.find_element_by_id(COMM_SRC).click()
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',ARTICLE_EMPTY_TIPS)
        assert self.driver.find_element_by_id(ARTICLE_EMPTY_TIPS).text == u'内容不存在,无法查看'
        back(self.driver)
        print u'Step %s:我的评论-发布评论%s原文被删除时，点击查看原文能够正确提示测试：OK' % (str(step),info_str)
        step+=1

        self.driver.find_element_by_id(MY_COMM_REPLY).click()
        self.driver.find_element_by_id(COMM_SRC).click()
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',ARTICLE_EMPTY_TIPS)
        assert self.driver.find_element_by_id(ARTICLE_EMPTY_TIPS).text == u'内容不存在,无法查看'
        print u'Step %s:我的评论-回复评论%s原文被删除时，点击查看原文能够正确提示测试：OK' % (str(step),info_str)
        step+=1

        self.db.publish_del_article_by_db(clue_id)

    def article_test(self,article,info_str):
        step = 1
        try:
            info_str = info_str.decode('gbk')
        except:
            pass
        sleep(WAIT_TIME)
        go_to_mycomm(self.driver,self.mode)
        infoid = self.db.get_infoid_by_article_name(article)
        #print infoid
        self.db.del_article_by_db(infoid)

        self.driver.find_element_by_id(COMM_SRC).click()
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',ARTICLE_EMPTY_TIPS)
        assert self.driver.find_element_by_id(ARTICLE_EMPTY_TIPS).text == u'内容不存在,无法查看'
        slide_left(self.driver)
        assert element_exsist(self.driver,'id',ARTICLE_EMPTY_TIPS)
        assert self.driver.find_element_by_id(ARTICLE_EMPTY_TIPS).text == u'内容不存在,无法查看'
        back(self.driver)
        sleep(WAIT_TIME)
        print u'Step %s:我的评论-发布评论%s原文被删除时，点击查看原文能够正确提示且左划手势屏蔽测试：OK' % (str(step),info_str)
        step+=1

        self.driver.find_element_by_id(MY_COMM_REPLY).click()
        sleep(WAIT_TIME)
        self.driver.find_element_by_id(COMM_SRC).click()
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',ARTICLE_EMPTY_TIPS)
        assert self.driver.find_element_by_id(ARTICLE_EMPTY_TIPS).text == u'内容不存在,无法查看'
        slide_left(self.driver)
        assert element_exsist(self.driver,'id',ARTICLE_EMPTY_TIPS)
        assert self.driver.find_element_by_id(ARTICLE_EMPTY_TIPS).text == u'内容不存在,无法查看'
        print u'Step %s:我的评论-回复评论%s原文被删除时，点击查看原文能够正确提示且左划手势屏蔽测试：OK' % (str(step),info_str)
        step+=1

        self.db.publish_del_article_by_db(infoid)

    #excute TestCase
    def testMyCommentArticle(self):
        article = NORMAL_ARTICLE
        info_str = u'新闻'
        comid = self.api.send_comment_by_name(article,'A'+str(randint(1,100)))
        self.api.send_comment_by_name(article,'B'+str(randint(1,100)),comid)
        activity = ACTIVITY[article]
        self.article_test(article,info_str)

    def testMyCommentArticlePhoto(self):
        article = PHOTO_ARTICLE
        info_str = u'组图'
        comid = self.api.send_comment_by_name(article,'A'+str(randint(1,100)))
        self.api.send_comment_by_name(article,'B'+str(randint(1,100)),comid)
        activity = ACTIVITY[article]
        self.common_check(article,info_str)

    def testMyCommentArticleExt(self):
        article = EXT_ARTICLE
        info_str = u'外链'
        comid = self.api.send_comment_by_name(article,'A'+str(randint(1,100)))
        self.api.send_comment_by_name(article,'B'+str(randint(1,100)),comid)
        activity = ACTIVITY[article]
        self.common_check(article,info_str)

    def testMyCommentArticleVideo(self):
        article = VIDEO_ARTICLE
        info_str = u'视频'
        comid = self.api.send_comment_by_name(article,'A'+str(randint(1,100)))
        self.api.send_comment_by_name(article,'B'+str(randint(1,100)),comid)
        activity = ACTIVITY[article]
        self.common_check(article,info_str)

    def testMyCommentArticleAudio(self):
        article = AUDIO_ARTICLE
        info_str = u'音频'
        comid = self.api.send_comment_by_name(article,'A'+str(randint(1,100)))
        self.api.send_comment_by_name(article,'B'+str(randint(1,100)),comid)
        activity = ACTIVITY[article]
        self.common_check(article,info_str)

    #head
    def testMyCommentClue(self):
        article = 'clue'
        info_str = u'报料'
        clue_id = self.db.get_first_clue(4)
        comid = self.api.send_comment(clue_id,'A'+str(randint(1,100)))
        self.api.send_comment(clue_id,'B'+str(randint(1,100)),comid)
        self.clue_check(clue_id,info_str)

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
