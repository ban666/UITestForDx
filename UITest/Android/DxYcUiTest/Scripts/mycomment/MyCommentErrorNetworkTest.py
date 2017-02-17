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
            login_to_index(self.driver,self.mode,self.desired_caps['appPackage'],TEST_PHONE,DEVICE_TID)
        dc = get_config_by_adb()['dc']
        self.api = ChnlRequest(self.mode,dc=dc)
        self.first_article = self.api.get_first_chnl_article_by_model(13)
        self.db.change_comment_state_by_db(self.first_article['infoid'],2)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.db.change_comment_state_by_db(self.first_article['infoid'],0)
            self.db.set_digg_count_by_db(self.comid, 0)
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self,article=u'自动化文字新闻'):
        step = 1

        #发送评论
        self.comid = self.api.send_comment_by_name(article,'digg count test')
        #print self.comid

        change_network(self.driver,'none')
        #进入文章页
        go_to_mycomm(self.driver,self.mode)
        sleep(16)
        #无网络时表现
        assert element_exsist(self.driver,'id',NETERROR_TIPS)
        assert self.driver.find_element_by_id(NETERROR_TIPS).text == u'点击屏幕　重新加载'
        print u'Step %s:我的评论-发布评论 无网络加载失败时有错误提示测试结果：OK' % (str(step))
        step+=1
        #恢复网络重新加载
        change_network(self.driver,'wifi')
        sleep(10)
        self.driver.find_element_by_id(NETERROR_TIPS).click()
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',COMMENT)
        print u'Step %s:我的评论-发布评论 加载失败可重新加载测试结果：OK' % (str(step))
        step+=1

        change_network(self.driver,'none')
        self.driver.find_element_by_id(MY_COMM_REPLY).click()
        sleep(16)
        #无网络时表现
        assert element_exsist(self.driver,'id',NETERROR_TIPS)
        assert self.driver.find_element_by_id(NETERROR_TIPS).text == u'点击屏幕　重新加载'
        print u'Step %s:我的评论-回复评论 无网络加载失败时有错误提示测试结果：OK' % (str(step))
        step+=1
        #恢复网络重新加载
        change_network(self.driver,'wifi')
        sleep(10)
        self.driver.find_element_by_id(NETERROR_TIPS).click()
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',COMMENT)
        print u'Step %s:我的评论-回复评论 加载失败可重新加载测试结果：OK' % (str(step))
        step+=1



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

