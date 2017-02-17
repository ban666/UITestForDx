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


class MyCommentForbiddenTest(unittest.TestCase):

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
            login_to_index(self.driver,TEST_PHONE)

    def tearDown(self):
        print 'Test End...................................'
        try:
            for article in self.article_list:
                self.db.open_comment_by_name(article)
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down'

    def common_check(self,article,info_str,content,input_button=COMMENT_INPUT_BUTTON,entrance=COMMENT_ENTRANCE):
        step = 1
        try:
            info_str = info_str.decode('gbk')
        except:
            pass
        assert get_to_article_by_search(self.driver,article)
        go_to_comment_page(self.driver,entrance)
        send_comment(self.driver,content,input_button)
        back(self.driver)
        search_article_to_index(self.driver)
        go_to_mycomm(self.driver,self.mode)
        self.db.close_comment_by_name(article)

        #回复评论
        quote_content = u'禁止评论测试'+str(randint(1,100))
        my_comment_handle(self.driver,1,'reply',content=quote_content)
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,*COMMENT_INPUT_EDIT)
        assert self.driver.find_element(*COMMENT_INPUT_EDIT).text == quote_content
        print u'Step %s:%s 禁止评论测试结果：OK' % (str(step),info_str)
        step+=1

        self.db.open_comment_by_name(article)

    def clue_check(self,clue_id,info_str,content):
        step = 1
        try:
            info_str = info_str.decode('gbk')
        except:
            pass
        self.driver.find_element_by_id('menu2 1').click()
        sleep(3)
        clue = CLUE_ITEM[1] % (1,1)
        self.driver.find_element_by_xpath(clue+CLUE_LIST_DICT['comment'][1]).click()
        sleep(3)
        send_comment(self.driver,content,CLUE_DETAIL_COMMENT_BUTTON)
        back(self.driver)
        self.driver.find_element_by_id('menu1 1').click()

        go_to_mycomm(self.driver,self.mode)
        self.db.change_comment_state_by_db(clue_id,1)

        #回复评论
        quote_content = u'禁止评论测试'+str(randint(1,100))
        my_comment_handle(self.driver,1,'reply',content=quote_content)
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,*COMMENT_INPUT_EDIT)
        assert self.driver.find_element(*COMMENT_INPUT_EDIT).text == quote_content
        print u'Step %s:%s 禁止评论测试结果：OK' % (str(step),info_str)
        step+=1

        self.db.change_comment_state_by_db(clue_id,0)

    #excute TestCase
    def testMyCommentArticle(self):
        article = NORMAL_ARTICLE
        info_str = u'新闻'
        content = u'评论'+str(randint(1,100))

        self.common_check(article,info_str,content)

    def testMyCommentArticlePhoto(self):
        article = PHOTO_ARTICLE
        info_str = u'组图'
        content = u'评论'+str(randint(1,100))
        self.common_check(article,info_str,content)

    def testMyCommentArticleExt(self):
        article = EXT_ARTICLE
        info_str = u'外链'
        content = u'评论'+str(randint(1,100))
        self.common_check(article,info_str,content)

    def testMyCommentArticleVideo(self):
        article = VIDEO_ARTICLE
        info_str = u'视频'
        content = u'评论'+str(randint(1,100))
        self.common_check(article,info_str,content,input_button=COMMENT_INPUT_IN_ARTICLE)

    def testMyCommentArticleAudio(self):
        article = AUDIO_ARTICLE
        info_str = u'音频'
        content = u'评论'+str(randint(1,100))
        self.common_check(article,info_str,content,entrance=COMMENT_ENTRANCE_AUDIO)

    #head
    def testMyCommentClue(self):
        article = 'clue'
        info_str = u'报料'
        content = u'评论'+str(randint(1,100))
        t = self.db.get_subtype_by_db()[0]['clcaid']
        clue_id = self.db.get_first_clue(t)
        self.db.clear_comment_by_id(clue_id)
        self.clue_check(clue_id,info_str,content)

if __name__ == '__main__':
    pass
    # a = TestLogin()
    # a.setUp()
    # a.testFunc1()
    # a.tearDown()
    import HTMLTestRunner
    t = unittest.TestSuite()
    t.addTest(unittest.makeSuite(MyCommentForbiddenTest))
    #unittest.TextTestRunner.run(t)
    filename = 'F:\\dx_comment.html'
    fp = file(filename,'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
            stream = fp,
            title ='Dx_Test',
            description = 'Report_discription')

    runner.run(t)
    fp.close()
