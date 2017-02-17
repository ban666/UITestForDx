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
from elements_id import *
from common import exception_handler
from configrw import get_case
from TestlinkHandler import TestlinkHandler

class ArticleAmazingCommentTest(unittest.TestCase):

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
        self.first_article = self.api.get_first_chnl_article_by_model(13)
        self.db.change_comment_state_by_db(self.first_article['infoid'],2)
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        start_to_index(self.driver,self.mode)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.tsl.set_tc_status(self.case_id,self.result,self.msg)
            self.db.change_comment_state_by_db(self.first_article['infoid'],0)
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self):
        step = 1
        #验证精彩评论模块是否存在且仅存3条
        slide_up(self.driver,7)
        print self.driver.contexts
        self.driver.switch_to.context(self.driver.contexts[-1])
        type_title = self.driver.find_element_by_xpath('//*[@id="comment_box"]/h2/em').text
        comment_count = len(self.driver.find_elements_by_class_name('comment-avatar'))
        assert type_title == u'精彩评论'
        assert comment_count == 3
        print u'Step %s:正文页存在精彩评论且最大显示为3条测试：OK' % (str(step))
        step+=1

        self.driver.find_element_by_id('btn-comment-more').click()
        sleep(5)
        assert self.driver.current_activity == ACTIVITY.get('comment')
        print u'Step %s:点击精彩评论中查看更多评论按钮跳转测试：OK' % (str(step))
        step+=1
        return True

    #excute TestCase
    def testExsit(self):
        print get_to_article_by_search(self.driver,WONDERFUL_COMMENT_ARTICLE,self.mode)
        sleep(WAIT_TIME)
        self.case_id = get_case(__file__)
        self.result = self.common_check()

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

