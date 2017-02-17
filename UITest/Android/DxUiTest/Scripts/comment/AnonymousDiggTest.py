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

class AnonymousDiggTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.mode = 'mcp/dx'
        self.db = DbLib()
        self.api = ChnlRequest(self.mode)
        self.article_list = [NORMAL_ARTICLE,VIDEO_ARTICLE,EXT_ARTICLE,PHOTO_ARTICLE]
        for article in self.article_list:
            self.api.send_comment_by_name(article,'A'+str(randint(1,100)))
            self.api.send_comment_by_name(article,'B'+str(randint(1,100)))
        self.first_article = self.api.get_first_chnl_article_by_model(13)
        self.db.change_comment_state_by_db(self.first_article['id'],2)
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        start_to_index(self.driver,self.mode)
        if is_login(self.driver):
            logout_to_index(self.driver,self.mode)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.db.change_comment_state_by_db(self.first_article['id'],0)
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self):
        step = 1
        #对第一个评论气泡点赞
        find_first_comment_and_support(self.driver)
        first_digg_count = self.driver.find_elements_by_id('com.zc.hubei_news:id/tv_digg')[0].text
        assert first_digg_count == '1'
        print u'Step %s:匿名气泡点赞测试结果：OK' % (str(step))
        step+=1

        #对第二个评论按钮点赞
        self.driver.find_elements_by_id('com.zc.hubei_news:id/iv_common_zan')[1].click()
        second_digg_count = self.driver.find_elements_by_id('com.zc.hubei_news:id/tv_digg')[1].text
        assert second_digg_count == '1'
        print u'Step %s:匿名按钮点赞测试结果：OK' % (str(step))
        step+=1

    #excute TestCase
    def testArticleComment(self):
        get_to_article_by_search(self.driver,u'自动化文字新闻',self.mode)
        sleep(5)
        self.driver.find_element_by_id('com.zc.hubei_news:id/rl_coments').click()
        self.common_check()



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

