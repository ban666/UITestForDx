# -*- coding: utf-8 -*-
__author__ = 'liaoben'

import sys
from appium import webdriver
from time import sleep
import unittest
from random import randint
sys.path.append('../../Lib')
from appium_lib import *
from DbLib import DbLib
from config import *
from loglib import log
from threading import Thread
from elements_id import *
from ui_settings import *
from jpush_handler import JpushHandler
from ui_push import *
from configrw import get_case
from TestlinkHandler import TestlinkHandler


class PushBackTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.result = 'f'
        self.msg = ''
        self.tsl = TestlinkHandler()
        self.mode = MODE
        self.db = DbLib()
        self.jpush = JpushHandler()
        #self.api = ChnlRequest(self.mode)
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        start_to_index(self.driver,self.mode)

    def tearDown(self):
        print 'Test End...................................'
        try:
             self.tsl.set_tc_status(self.case_id,self.result,self.msg)
             self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self,article):
        step = 1
        sleep(WAIT_TIME)
        print self.driver.current_activity
        go_to_settings(self.driver)
        sleep(WAIT_TIME)
        assert set_push_state(self.driver,'true')
        clear_notification(self.driver)

        push_info = self.db.get_push_info_by_name(article)

        #退出客户端并发送推送
        quit_app(self.driver)
        self.jpush.push_article(push_info['model'],push_info['infoid'])
        sleep(WAIT_TIME)
        ret = get_push_el(self.driver,timeout=20)
        #print ret
        assert len(ret)==1
        #print ret
        open_notifications(self.driver)
        ret[0].click()
        sleep(WAIT_TIME)
        print self.driver.current_activity
        assert self.driver.current_activity == ACTIVITY.get(article)

        #返回上级页面并验证是否为主页
        back(self.driver)
        sleep(WAIT_TIME)
        print self.driver.current_activity
        assert self.driver.current_activity == ACTIVITY.get('index')
        assert element_exsist(self.driver,'id',SEARCH_BUTTON) or element_exsist(self.driver,'id',UPDATE_DIALOG)
        print u'Step %s:纯文字新闻推送，点击调起客户端测试：OK' % (str(step))
        step+=1

        return True

    def basic_check(self,article):
        step = 1
        sleep(WAIT_TIME)
        print self.driver.current_activity
        go_to_settings(self.driver)
        sleep(WAIT_TIME)
        assert set_push_state(self.driver,'true')
        clear_notification(self.driver)

        push_info = self.db.get_push_info_by_name(article)

        #退出客户端并发送推送
        quit_app(self.driver)
        self.jpush.push_article(push_info['model'],push_info['infoid'])
        sleep(WAIT_TIME)
        ret = get_push_el(self.driver,timeout=20)
        #print ret
        assert len(ret)==1
        #print ret
        open_notifications(self.driver)
        ret[0].click()
        sleep(WAIT_TIME)
        print self.driver.current_activity
        assert self.driver.current_activity == ACTIVITY.get(article)

        #返回上级页面并验证是否为主页
        back(self.driver)
        sleep(WAIT_TIME)
        print self.driver.current_activity
        assert self.driver.current_activity == ACTIVITY.get('index')
        assert element_exsist(self.driver,'id',SEARCH_BUTTON) or element_exsist(self.driver,'id',UPDATE_DIALOG)
        print u'Step %s:客户端未启动时打开推送内容，点击返回能回到客户端首页测试：OK' % (str(step))
        step+=1

        return True

    def start_check(self,article):
        step = 1
        sleep(WAIT_TIME)
        self.driver.find_element(*HEAD).click()

        push_info = self.db.get_push_info_by_name(article)

        #在报料页面点击推送
        self.jpush.push_article(push_info['model'],push_info['infoid'])
        sleep(WAIT_TIME)
        ret = confirm_push(self.driver,timeout=20)
        assert ret
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'class','UIAWebView')

        #返回上级页面并验证是否为报料页面
        back(self.driver)
        assert element_exsist(self.driver,*MY_CLUE_BUTTON)
        print u'Step %s:客户端启动时打开推送内容，点击返回能回到上级页面测试：OK' % (str(step))
        step+=1

        return True

    def home_check(self,article):
        step = 1
        sleep(WAIT_TIME)

        clear_notification(self.driver)
        get_to_article_by_search(self.driver,NORMAL_ARTICLE,self.mode)
        sleep(WAIT_TIME)

        push_info = self.db.get_push_info_by_name(article)

        #退出客户端并发送推送
        self.driver.quit()
        self.jpush.push_article(push_info['model'],push_info['infoid'])
        #sleep(WAIT_TIME)
        ret = get_push_el(self.driver,timeout=20)
        #print ret
        assert len(ret)==1
        #print ret
        open_notifications(self.driver)
        ret[0].click()
        #sleep(WAIT_TIME)
        #print ret

        #返回上级页面并验证是否为主页
        back(self.driver)
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',SEARCH_BUTTON) or element_exsist(self.driver,'id',UPDATE_DIALOG)
        print u'Step %s:客户端在新闻详情页后台时，打开推送的内容后，点击返回，能够回到客户端在后台时保留的页面（安卓只能回到1级页面）：OK' % (str(step))
        step+=1

        get_to_article_by_search(self.driver,ZHUANTI_ARTICLE,self.mode)
        sleep(WAIT_TIME)

        push_info = self.db.get_push_info_by_name(article)

        #退出客户端并发送推送
        home(self.driver)
        self.jpush.push_article(push_info['model'],push_info['infoid'])
        sleep(WAIT_TIME)
        ret = get_push_el(self.driver,timeout=20)
        #print ret
        assert len(ret)==1
        #print ret
        open_notifications(self.driver)
        ret[0].click()
        sleep(WAIT_TIME)
        print self.driver.current_activity
        assert self.driver.current_activity == ACTIVITY.get(article)

        #返回上级页面并验证是否为主页
        back(self.driver)
        sleep(WAIT_TIME)
        print self.driver.current_activity
        assert self.driver.current_activity == ACTIVITY.get('index')
        assert element_exsist(self.driver,'id',SEARCH_BUTTON) or element_exsist(self.driver,'id',UPDATE_DIALOG)
        print u'Step %s:客户端在专题详情页后台时，打开推送的内容后，点击返回，能够回到客户端在后台时保留的页面（安卓只能回到1级页面）：OK' % (str(step))
        step+=1

        return True


    #excute TestCase
    # def testBasic(self):
    #     self.case_id = get_case(__file__)
    #     self.result = self.common_check(NORMAL_ARTICLE)

    def testStart(self):
        self.case_id = get_case(__file__)
        self.result = self.start_check(NORMAL_ARTICLE)

    # def testHome(self):
    #     self.case_id = get_case(__file__)
    #     self.result = self.home_check(NORMAL_ARTICLE)

    def testBack(self):
        self.case_id = get_case(__file__)
        self.result = self.start_check(NORMAL_ARTICLE)

    # def testAppStart(self):
    #     self.case_id = get_case(__file__)
    #     self.result = self.basic_check(NORMAL_ARTICLE)

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

