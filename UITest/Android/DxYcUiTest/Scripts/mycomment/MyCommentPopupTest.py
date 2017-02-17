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
from adb import *
from config import *
from elements_id import *
from common import exception_handler

class MyCommentPopupTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.mode = MODE
        self.db = DbLib()
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        start_to_index(self.driver,self.mode)
        if not is_login(self.driver):
            login_to_index(self.driver,self.mode,self.desired_caps['appPackage'],TEST_PHONE,DEVICE_TID)
        dc = get_config_by_adb()['dc']
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

    def common_check(self):
        step = 1

        go_to_mycomm(self.driver,self.mode)
        self.driver.find_element_by_id(COMMENT).click()
        assert element_exsist(self.driver,'id',REPLY_BUTTON)
        assert element_exsist(self.driver,'id',COPY_BUTTON)
        assert element_exsist(self.driver,'id',MY_COMM_SUPPORT_BUTTON)
        back(self.driver)
        print u'Step %s:我的评论气泡菜单测试：OK' % (str(step))
        step+=1

        self.driver.find_element_by_id(MY_COMM_REPLY).click()
        self.driver.find_element_by_id(COMMENT).click()
        assert element_exsist(self.driver,'id',REPLY_BUTTON)
        assert element_exsist(self.driver,'id',COPY_BUTTON)
        assert element_exsist(self.driver,'id',MY_COMM_SUPPORT_BUTTON)
        print u'Step %s:回复我的气泡菜单测试：OK' % (str(step))
        step+=1


    #excute TestCase
    def testMyComment(self):
        article = PHOTO_ARTICLE
        comid = self.api.send_comment_by_name(article,'A'+str(randint(1,100)))
        self.api.send_comment_by_name(article,'B'+str(randint(1,100)),comid)
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

