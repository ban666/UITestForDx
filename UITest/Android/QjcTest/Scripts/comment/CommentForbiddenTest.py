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
from adb import is_login
from config import *
from elements_id import *
from common import exception_handler

class CommentForbiddenTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.mode = MODE
        self.db = DbLib()
        self.article_list = [NORMAL_ARTICLE,VIDEO_ARTICLE,EXT_ARTICLE,PHOTO_ARTICLE,AUDIO_ARTICLE]
        for article in self.article_list:
            self.db.close_comment_by_name(article)
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        start_to_index(self.driver,self.mode)
        # if not is_login(self.desired_caps['appPackage']):
        #     login_to_index(self.driver,self.mode,self.desired_caps['appPackage'],TEST_PHONE,DEVICE_TID)

    def tearDown(self):
        print 'Test End...................................'
        try:
            for article in self.article_list:
                self.db.open_comment_by_name(article)
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self):
        step = 1
        #验证评论框是否存在
        exsits = element_exsist(self.driver,'id',COMMENT_INPUT)
        assert exsits == False
        print u'Step %s:禁止评论测试结果：OK' % (str(step))
        step+=1

        #验证左划手势
        slide_left(self.driver)
        sleep(WAIT_TIME)
        assert  self.driver.current_activity != ACTIVITY.get('comment')
        print u'Step %s:左划手势屏蔽测试结果：OK' % (str(step))
        step+=1

    def photo_check(self):
        step = 1
        #验证评论框是否存在
        exsits = element_exsist(self.driver,'id',COMMENT_PHOTO_ENTRANCE)
        assert exsits == False
        print u'Step %s:禁止评论测试结果：OK' % (str(step))
        step+=1

        #验证左划手势
        slide_left(self.driver)
        sleep(WAIT_TIME)
        assert  self.driver.current_activity != ACTIVITY.get('comment')
        print u'Step %s:左划手势屏蔽测试结果：OK' % (str(step))
        step+=1

    def video_check(self):
        step = 1
        #验证评论框是否存在
        exsits = element_exsist(self.driver,'id',COMMENT_INPUT)
        assert exsits == False
        print u'Step %s:禁止评论测试结果：OK' % (str(step))
        step+=1

        #视频列表提示语测试
        tips = self.driver.find_element_by_id(VIDEO_FORBBIDEN_COMMENT).text
        assert tips == u'对不起，此视频评论已关闭'
        print u'Step %s:视频列表提示语测试结果：OK' % (str(step))
        step+=1

    #excute TestCase
    def testVideoComment(self):
        get_to_article_by_search(self.driver,VIDEO_ARTICLE,self.mode)
        sleep(5)
        self.video_check()


    def testArticleComment(self):
        get_to_article_by_search(self.driver,NORMAL_ARTICLE,self.mode)
        sleep(5)
        self.common_check()

    def testPhotoComment(self):
        get_to_article_by_search(self.driver,PHOTO_ARTICLE,self.mode)
        sleep(5)
        self.photo_check()

    def testExtComment(self):
        get_to_article_by_search(self.driver,EXT_ARTICLE,self.mode)
        sleep(5)
        self.common_check()

    def testAudioComment(self):
        get_to_article_by_search(self.driver,AUDIO_ARTICLE,self.mode)
        sleep(5)
        self.photo_check()

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
            description = 'Report_discription'
            )

    runner.run(t)
    fp.close()

