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


class MyCommentErrNetworkTest(unittest.TestCase):

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
        quote_content = u'回复评论'+str(randint(1,1000))
        assert get_to_article_by_search(self.driver,article)
        go_to_comment_page(self.driver)
        send_comment(self.driver,content)
        comment_handle(self.driver,1,'reply',content=quote_content)
        back(self.driver)
        search_article_to_index(self.driver)

        self.comid = self.db.get_latest_comid_by_article(article)
        #print self.comid

        change_network(self.driver,'none')
        #进入文章页
        go_to_mycomm(self.driver,self.mode)
        sleep(16)
        #无网络时表现
        assert self.driver.find_element(*NETERROR_TIPS).is_displayed()
        print u'Step %s:我的评论-发布评论 无网络加载失败时有错误提示测试结果：OK' % (str(step))
        step+=1
        #恢复网络重新加载
        change_network(self.driver,'wifi')
        sleep(10)
        self.driver.find_element(*NETERROR_TIPS).click()
        sleep(WAIT_TIME)
        assert get_comment_info(self.driver,1,True)['content'] == quote_content
        print u'Step %s:我的评论-发布评论 加载失败可重新加载测试结果：OK' % (str(step))
        step+=1

        change_network(self.driver,'none')
        self.driver.find_element(*MY_COMM_REPLY).click()
        sleep(16)
        #无网络时表现
        assert self.driver.find_element(*NETERROR_TIPS).is_displayed()
        print u'Step %s:我的评论-回复评论 无网络加载失败时有错误提示测试结果：OK' % (str(step))
        step+=1
        #恢复网络重新加载
        change_network(self.driver,'wifi')
        sleep(10)
        self.driver.find_element(*NETERROR_TIPS).click()
        sleep(WAIT_TIME)
        assert get_comment_info(self.driver,1,True)['content'] == quote_content
        print u'Step %s:我的评论-回复评论 加载失败可重新加载测试结果：OK' % (str(step))
        step+=1



    #excute TestCase
    # def testMyCommentArticle(self):
    #     self.common_check()




if __name__ == '__main__':
    pass
    # a = TestLogin()
    # a.setUp()
    # a.testFunc1()
    # a.tearDown()
    #d =DbLib()

    import HTMLTestRunner
    t = unittest.TestSuite()
    t.addTest(unittest.makeSuite(MyCommentErrNetworkTest))
    #unittest.TextTestRunner.run(t)
    filename = 'F:\\dx_comment.html'
    fp = file(filename,'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
            stream = fp,
            title ='Dx_Test',
            description = 'Report_discription')

    runner.run(t)
    fp.close()

