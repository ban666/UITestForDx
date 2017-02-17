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
from adb import is_login
from config import *
from elements_id import *
from common import exception_handler

class CommentBasicTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.mode = MODE
        self.db = DbLib()
        self.api = ChnlRequest(self.mode)
        self.first_article = self.api.get_first_chnl_article_by_model(13)
        self.db.change_comment_state_by_db(self.first_article['infoid'],2)
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        start_to_index(self.driver,self.mode)
        # if not is_login(self.desired_caps['appPackage']):
        #     login_to_index(self.driver,self.mode,self.desired_caps['appPackage'],TEST_PHONE,DEVICE_TID)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.db.change_comment_state_by_db(self.first_article['infoid'],0)
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self,driver):
        step = 1
        #发表评论
        content = u'中文'+str(randint(1,100))
        #content = u'一'*140
        send_comment(driver,content)
        sleep(5)
        new_comment = driver.find_element_by_id('com.cnhubei.dxxwhw:id/rl_comment')
        info = get_comment_info(driver,new_comment,0)
        check_reply_elements = check_comment(driver,new_comment)
        assert check_reply_elements == 1
        assert info[3] == content
        print u'Step %s:发表评论测试结果：OK' % (str(step))
        step+=1

        #对此评论点赞
        find_first_comment_and_support(driver)
        first_digg_count = driver.find_element_by_id('com.cnhubei.dxxwhw:id/tv_digg').text
        assert first_digg_count == '1'
        print u'Step %s:评论气泡点赞测试结果：OK' % (str(step))
        step+=1

        #复制评论
        find_first_comment_and_copy(driver,0)
        assert check_copy_content(driver,content)
        print u'Step %s:复制评论测试结果：OK' % (str(step))
        step+=1

        #回复评论
        quote_content = u'回复评论'+str(randint(1,100))
        # quote_content = u'二'*140
        find_first_comment_and_reply(driver,quote_content)
        reply_comment = driver.find_element_by_id('com.cnhubei.dxxwhw:id/rl_comment')
        reply_info = get_comment_info(driver,reply_comment,1) #[点赞次数，地理位置_时间，评论用户名，评论内容，引用用户名，引用评论详情]
        assert reply_info[-1] == content
        assert reply_info[3] == quote_content
        print u'Step %s:回复评论测试结果：OK' % (str(step))
        step+=1

        #复制外部评论
        find_first_comment_and_copy(driver,1)
        assert check_copy_content(driver,quote_content)
        print u'Step %s:嵌套评论-复制外部评论测试结果：OK' % (str(step))
        step+=1

        #复制嵌套内部评论
        find_first_comment_and_copy(driver,0)
        assert check_copy_content(driver,content)
        print u'Step %s:嵌套评论-复制嵌套内部评论测试结果：OK' % (str(step))
        step+=1

        #回复嵌套评论-嵌套外评论
        quote_content_reply = u'回复嵌套外评论'+str(randint(1,100))
        find_first_comment_and_reply(driver,quote_content_reply,1)
        reply_comment = driver.find_element_by_id('com.cnhubei.dxxwhw:id/rl_comment')
        reply_info = get_comment_info(driver,reply_comment,1) #[点赞次数，地理位置_时间，评论用户名，评论内容，引用用户名，引用评论详情]
        assert reply_info[-1] == quote_content
        assert reply_info[3] == quote_content_reply
        print u'Step %s:嵌套评论-回复嵌套外评论测试结果：OK' % (str(step))
        step+=1

        #回复嵌套评论-嵌套内评论
        content_reply = u'回复嵌套内评论'+str(randint(1,100))
        find_first_comment_and_reply(driver,content_reply,0)
        reply_comment = driver.find_element_by_id('com.cnhubei.dxxwhw:id/rl_comment')
        reply_info = get_comment_info(driver,reply_comment,1) #[点赞次数，地理位置_时间，评论用户名，评论内容，引用用户名，引用评论详情]
        assert reply_info[-1] == quote_content
        assert reply_info[3] == content_reply
        print u'Step %s:嵌套评论-回复嵌套内评论测试结果：OK' % (str(step))
        step+=1

        #点赞嵌套内评论
        find_first_comment_and_support(driver,0)
        first_digg_count = driver.find_elements_by_id('com.cnhubei.dxxwhw:id/tv_digg')[2].text
        assert first_digg_count == '1'
        print u'Step %s:嵌套评论-嵌套评论内气泡点赞测试结果：OK' % (str(step))
        step+=1

        #点赞嵌套外评论
        find_first_comment_and_support(driver,1)
        first_digg_count = driver.find_elements_by_id('com.cnhubei.dxxwhw:id/tv_digg')[0].text
        assert first_digg_count == '1'
        print u'Step %s:嵌套评论-嵌套评论外气泡点赞测试结果：OK' % (str(step))
        step+=1

    #excute TestCase
    def testVideoComment(self):
        assert get_to_article_by_search(self.driver,VIDEO_ARTICLE)
        self.common_check(self.driver)

    def testArticleComment(self):
        assert get_to_article_by_search(self.driver,NORMAL_ARTICLE)
        go_to_comment_page(self.driver)
        self.common_check(self.driver)

    def testPhotoComment(self):
        assert get_to_article_by_search(self.driver,PHOTO_ARTICLE)
        go_to_comment_page(self.driver,is_photo =True)
        self.common_check(self.driver)

    def testExtComment(self):
        assert get_to_article_by_search(self.driver,EXT_ARTICLE)
        go_to_comment_page(self.driver)
        self.common_check(self.driver)

    def testAudioComment(self):
        get_to_article_by_search(self.driver,AUDIO_ARTICLE,self.mode)
        go_to_comment_page(self.driver,is_photo =True)
        self.common_check(self.driver)

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

