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


class CommentDiggCountTest(unittest.TestCase):

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
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        start_to_index(self.driver,self.mode)
        # if not is_login(self.desired_caps['appPackage']):
        #     login_to_index(self.driver,TEST_PHONE)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.tsl.set_tc_status(self.case_id,self.result,self.msg)
            self.db.set_digg_count_by_db(self.comid, 0)
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self,article):
        step = 1

        #发送评论
        self.comid = self.api.send_comment_by_name(article,'digg count test')
        print self.comid
        #进入文章页
        get_to_article_by_search(self.driver,article,self.mode)
        go_to_comment_page(self.driver)

        #点赞数<=999999显示测试
        self.db.set_digg_count_by_db(self.comid, 0)
        slide_down(self.driver,3)
        sleep(WAIT_TIME)
        article_count = get_comment_info(self.driver,1)['digg_count']
        assert article_count == u'0'

        self.db.set_digg_count_by_db(self.comid, 999999)
        slide_down(self.driver,3)
        sleep(WAIT_TIME)
        article_count = get_comment_info(self.driver,1)['digg_count']
        assert article_count == u'999999'
        print u'Step %s:评论点赞数为<=999999时显示测试：OK' % (str(step))
        step+=1

        #点赞数为999999时点赞测试
        comment_handle(self.driver,1,'support')
        article_count = get_comment_info(self.driver,1)['digg_count']
        assert article_count == u'999999'
        print u'Step %s:评论点赞数为999999时点赞测试：OK' % (str(step))
        step+=1

        #点赞数大于100万显示测试
        self.db.set_digg_count_by_db(self.comid, 1000000)
        slide_down(self.driver,3)
        sleep(WAIT_TIME)
        article_count = get_comment_info(self.driver,1)['digg_count']
        assert article_count == u'999999'
        print u'Step %s:评论点赞数大于999999时显示测试：OK' % (str(step))
        step+=1

        return True

    #excute TestCase
    def test(self):
        article = NORMAL_ARTICLE
        self.case_id = get_case(__file__)
        self.result = self.common_check(article)


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

