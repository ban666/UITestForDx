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

from elements_id import *
from ui_settings import *
from jpush_handler import JpushHandler
from ui_push import *

class PushBackTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.mode = MODE
        self.db = DbLib()
        self.jpush = JpushHandler()
        #self.api = ChnlRequest(self.mode)
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        start_to_index(self.driver,self.mode)

    def tearDown(self):
        print 'Test End...................................'
        try:
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
        setting_to_index(self.driver)

        push_info = self.db.get_push_info_by_name(article)

        #退出客户端并发送推送
        quit_app(self.driver)
        self.jpush.push_article(push_info['model'],push_info['infoid'])
        sleep(WAIT_TIME)
        ret = get_push_el(self.driver,timeout=20)
        assert len(ret)==1
        #print ret
        open_notifications(self.driver)
        ret[0].click()
        sleep(WAIT_TIME)
        #print self.driver.current_activity
        assert self.driver.current_activity == ACTIVITY.get(article)

        #返回上级页面并验证是否为主页
        back(self.driver)
        assert self.driver.current_activity == ACTIVITY.get('index')
        assert element_exsist(self.driver,'id',MENU_ICON) or element_exsist(self.driver,'id',BUTTON_CANCEL)
        print u'Step %s:客户端未启动时打开推送内容，点击返回能回到客户端首页测试：OK' % (str(step))
        step+=1

    def start_check(self,article):
        step = 1
        sleep(WAIT_TIME)
        go_to_settings(self.driver)
        sleep(WAIT_TIME)
        assert set_push_state(self.driver,'true')
        clear_notification(self.driver)
        settings_activity = self.driver.current_activity

        push_info = self.db.get_push_info_by_name(article)

        #在设置页面点击推送
        self.jpush.push_article(push_info['model'],push_info['infoid'])
        sleep(WAIT_TIME)
        ret = get_push_el(self.driver,timeout=20)
        assert len(ret)==1
        #print ret
        open_notifications(self.driver)
        ret[0].click()
        sleep(WAIT_TIME)
        #print self.driver.current_activity
        assert self.driver.current_activity == ACTIVITY.get(article)

        #返回上级页面并验证是否为主页
        back(self.driver)

        assert self.driver.current_activity == settings_activity
        print u'Step %s:客户端启动时打开推送内容，点击返回能回到上级页面首页测试：OK' % (str(step))
        step+=1

    #excute TestCase
    def testBasic(self):
        self.common_check(NORMAL_ARTICLE)

    def testStart(self):
        self.start_check(NORMAL_ARTICLE)
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

