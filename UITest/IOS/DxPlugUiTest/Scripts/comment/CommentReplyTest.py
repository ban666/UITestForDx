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

class AricileCommentTest(unittest.TestCase):

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
             self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self,article_name):
        step = 1
        #发表10篇普通评论
        article = self.db.get_infoid_by_article_name(article_name)
        for i in range(10):
            comid = self.api.send_comment(article,'A'+str(randint(1,100)))

        #回复最后一篇评论
        self.api.send_comment(article,u'回复评论'+str(randint(1,100)),comid)
        #content = u'一'*140

        #检查回复评论的结构
        get_to_article_by_search(self.driver,article_name,self.mode)
        go_to_comment_page(self.driver)
        # comment = self.driver.find_element_by_id(COMMENT)
        # result = check_reply_comment(self.driver,comment)
        result = get_comment_info(self.driver,1)
        check_elements = ['content','author','loc_time','digg_count','quote_content']
        assert check_elements.sort() == result.keys().sort()
        print u'Step %s:回复评论结构测试结果：OK' % (str(step))
        step+=1
        return True


    #excute TestCase
    def testArticleComment(self):
        article = u'自动化文字新闻'
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

