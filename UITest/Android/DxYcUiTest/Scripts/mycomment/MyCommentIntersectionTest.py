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
from config import ACTIVITY
from elements_id import *
from common import exception_handler
from ui_settings import *
from adb import *


class MyCommentBasicTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.mode = MODE
        self.db = DbLib()
        dc = get_config_by_adb()['dc']
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        start_to_index(self.driver,self.mode)
        if not is_login(self.driver):
            login_to_index(self.driver,self.mode,self.desired_caps['appPackage'],TEST_PHONE,DEVICE_TID)
        self.dc = get_config_by_adb()['dc']
        self.api = ChnlRequest(self.mode,dc=dc)
        self.first_article = self.api.get_first_chnl_article_by_model(13)
        self.db.change_comment_state_by_db(self.first_article['infoid'],2)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.db.change_comment_state_by_db(self.first_article['infoid'],0)
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self,content,info_str):
        step = 1

        go_to_mycomm(self.driver,self.mode)
        sleep(WAIT_TIME)
        #对此评论点赞
        comment = self.driver.find_elements_by_id(COMMENT_TEXT)
        comments = [x.text for x in comment]
        assert content in comments == False
        print u'Step %s:%s 禁止评论测试结果：OK' % (str(step),str(info_str))
        step+=1



    #excute TestCase
    def testMyComment(self):
        article = NORMAL_ARTICLE
        info_str = u'新闻'
        content = u'动向评论'+str(randint(1,1000))
        self.dxapi = ChnlRequest('mcp/dx',dc=self.dc)
        comid = self.dxapi.send_comment_by_name(article,content,'','hd_ak=7')
        self.common_check(content,info_str)




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

