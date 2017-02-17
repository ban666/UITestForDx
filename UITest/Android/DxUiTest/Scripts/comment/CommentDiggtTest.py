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

from config import TEST_PHONE,DEVICE_TID
from elements_id import *
from common import exception_handler

class CommentDiggtTest(unittest.TestCase):

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

    def common_check(self,driver):
        step = 1
        #发表评论
        content = u'A'+str(randint(1,100))
        send_comment(driver,content)
        sleep(5)
        new_comment = driver.find_element_by_id('com.zc.hubei_news:id/rl_comment')
        info = get_comment_info(driver,new_comment,0)
        assert info[3] == content
        print u'Step %s:发表评论A：OK' % (str(step))
        step+=1

        #对此评论气泡点赞
        find_first_comment_and_support(driver)
        first_digg_count = driver.find_element_by_id('com.zc.hubei_news:id/tv_digg').text
        assert first_digg_count == '1'
        print u'Step %s:评论气泡点赞测试结果：OK' % (str(step))
        step+=1

        #对此评论气泡重复点赞
        find_first_comment_and_support(driver)
        first_digg_count = driver.find_element_by_id('com.zc.hubei_news:id/tv_digg').text
        assert first_digg_count == '1'
        print u'Step %s:评论气泡重复点赞测试结果：OK' % (str(step))
        step+=1

        #发表评论B
        content = u'B'+str(randint(1,100))
        send_comment(driver,content)
        sleep(5)
        new_comment = driver.find_element_by_id('com.zc.hubei_news:id/rl_comment')
        info = get_comment_info(driver,new_comment,0)
        check_reply_elements = check_comment(driver,new_comment)
        assert info[3] == content
        print u'Step %s:发表评论B：OK' % (str(step))
        step+=1

        #对此评论按钮点赞
        driver.find_element_by_id('com.zc.hubei_news:id/iv_common_zan').click()
        first_digg_count = driver.find_element_by_id('com.zc.hubei_news:id/tv_digg').text
        assert first_digg_count == '1'
        print u'Step %s:评论按钮点赞测试结果：OK' % (str(step))
        step+=1

        #对此评论按钮重复点赞
        driver.find_element_by_id('com.zc.hubei_news:id/iv_common_zan').click()
        first_digg_count = driver.find_element_by_id('com.zc.hubei_news:id/tv_digg').text
        assert first_digg_count == '1'
        print u'Step %s:评论按钮重复点赞测试结果：OK' % (str(step))
        step+=1

    #excute TestCase
    def testVideoComment(self):
        get_to_article_by_search(self.driver,u'自动化视频新闻',self.mode)
        self.common_check(self.driver)

    def testArticleComment(self):
        get_to_article_by_search(self.driver,u'自动化文字新闻',self.mode)
        self.driver.find_element_by_id('com.zc.hubei_news:id/rl_coments').click()
        self.common_check(self.driver)

    def testPhotoComment(self):
        get_to_article_by_search(self.driver,u'自动化组图新闻',self.mode)
        self.driver.find_element_by_id('com.zc.hubei_news:id/rl_coments').click()
        self.common_check(self.driver)

    def testExtComment(self):
        get_to_article_by_search(self.driver,u'自动化外链新闻',self.mode)
        self.driver.find_element_by_id('com.zc.hubei_news:id/rl_coments').click()
        self.common_check(self.driver)


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

