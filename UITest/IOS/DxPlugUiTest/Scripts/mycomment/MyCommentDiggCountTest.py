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


class MyCommentDiggCountTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.mode = MODE
        self.db = DbLib()
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        start_to_index(self.driver,self.mode)
        if not is_login(self.driver):
            login_to_index(self.driver,TEST_PHONE)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.db.set_digg_count_by_db(self.comid, 0)
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down'

    def common_check(self,article=NORMAL_ARTICLE):
        step = 1

        #发送评论
        content = u'评论'+str(randint(1,1000))
        assert get_to_article_by_search(self.driver,article)
        go_to_comment_page(self.driver)
        send_comment(self.driver,content)
        back(self.driver)
        search_article_to_index(self.driver)

        self.comid = self.db.get_latest_comid_by_article(article)
        #进入文章页
        go_to_mycomm(self.driver,self.mode)

        #点赞数<=999999显示测试
        self.db.set_digg_count_by_db(self.comid, 0)
        slide_down(self.driver,3)
        sleep(WAIT_TIME)
        article_count = get_comment_info(self.driver,1,True)['digg_count']
        assert article_count == u'0'

        self.db.set_digg_count_by_db(self.comid, 999999)
        slide_down(self.driver,3)
        sleep(WAIT_TIME)
        article_count = get_comment_info(self.driver,1,True)['digg_count']
        assert article_count == u'999999'
        print u'Step %s:评论点赞数为<=999999时显示测试：OK' % (str(step))
        step+=1

        #点赞数为999999时点赞测试
        my_comment_handle(self.driver,1,'support')
        article_count = get_comment_info(self.driver,1,True)['digg_count']
        assert article_count == u'999999'
        print u'Step %s:评论点赞数为999999时点赞测试：OK' % (str(step))
        step+=1

        #点赞数大于100万显示测试
        self.db.set_digg_count_by_db(self.comid, 1000000)
        slide_down(self.driver,3)
        sleep(WAIT_TIME)
        article_count = get_comment_info(self.driver,1,True)['digg_count']
        assert article_count == u'999999'
        print u'Step %s:评论点赞数大于999999时显示测试：OK' % (str(step))
        step+=1
        #self.db.set_digg_count_by_db(self.comid, 0)

    #excute TestCase
    def testMyCommentArticle(self):
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
    t.addTest(unittest.makeSuite(MyCommentDiggCountTest))
    #unittest.TextTestRunner.run(t)
    filename = 'F:\\dx_comment.html'
    fp = file(filename,'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
            stream = fp,
            title ='Dx_Test',
            description = 'Report_discription')

    runner.run(t)
    fp.close()

