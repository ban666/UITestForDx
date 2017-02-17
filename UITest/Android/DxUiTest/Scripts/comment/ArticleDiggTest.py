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

class ArticleDiggTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.mode = 'mcp/dx'
        self.db = DbLib()
        self.api = ChnlRequest(self.mode)
        self.article_list = [NORMAL_ARTICLE,VIDEO_ARTICLE,EXT_ARTICLE,PHOTO_ARTICLE]
        self.first_article = self.api.get_first_chnl_article_by_model(13)
        self.db.change_comment_state_by_db(self.first_article['id'],2)
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        start_to_index(self.driver,self.mode)
        # if is_login(self.driver):
        #     logout_to_index(self.driver,self.mode)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.db.change_comment_state_by_db(self.first_article['id'],0)
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self,article_name):
        step = 1
        #获取原始点赞与点踩数
        article = self.db.get_infoid_by_article_name(article_name)
        self.support_count = self.db.get_support_count_by_db(article)
        self.opposition_count = self.db.get_opposition_count_by_db(article)
        print article
        #进入文章页
        get_to_article_by_search(self.driver,article_name,self.mode)
        sleep(5)

        #点赞与点踩数为0显示测试
        self.db.set_support_count_by_db(article,0)
        self.db.set_opposition_count_by_db(article,0)
        refresh_article(self.driver)
        sleep(5)
        #print self.driver.context
        self.driver.switch_to.context(self.driver.contexts[-1])
        article_count = self.driver.find_element_by_accessibility_id('count_like_article').text
        unlike_count = self.driver.find_element_by_id('count_unlike_article').text
        #self.driver.switch_to.context(self.driver.contexts[0])
        assert article_count == str(0)
        assert unlike_count == str(0)
        print u'Step %s:正文页点赞与点踩数为0时显示测试：OK' % (str(step))
        step+=1

        #点赞与点踩数为0-9999显示测试
        self.db.set_support_count_by_db(article,9999)
        self.db.set_opposition_count_by_db(article,9999)
        refresh_article(self.driver)
        sleep(5)
        #print self.driver.context
        #print self.driver.contexts
        self.driver.switch_to.context(self.driver.contexts[-1])
        print self.driver.context
        article_count = self.driver.find_element_by_id('count_like_article').text
        unlike_count = self.driver.find_element_by_id('count_unlike_article').text
        self.driver.switch_to.context(self.driver.contexts[0])
        assert article_count == str(9999)
        assert unlike_count == str(9999)
        print u'Step %s:正文页点赞与点踩数为<=9999时显示测试：OK' % (str(step))
        step+=1

        #点赞与点踩数大于1万小于10万显示测试
        self.db.set_support_count_by_db(article,10000)
        self.db.set_opposition_count_by_db(article,10000)
        refresh_article(self.driver)
        sleep(5)
        #print self.driver.contexts[-1]
        self.driver.switch_to.context(self.driver.contexts[-1])
        article_count = self.driver.find_element_by_id('count_like_article').text
        unlike_count = self.driver.find_element_by_id('count_unlike_article').text
        self.driver.switch_to.context(self.driver.contexts[0])
        assert article_count == u'9999 +'
        assert unlike_count == u'9999 +'
        print u'Step %s:正文页点赞与点踩数大于1万显示测试：OK' % (str(step))
        step+=1


        self.db.set_support_count_by_db(article,self.support_count)
        self.db.set_opposition_count_by_db(article,self.opposition_count)

    #excute TestCase
    def testArticleComment(self):
        article = NORMAL_ARTICLE
        self.common_check(article)



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

