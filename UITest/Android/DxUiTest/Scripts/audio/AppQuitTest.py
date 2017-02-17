# -*- coding: utf-8 -*-
__author__ = 'liaoben'

import sys
from appium import webdriver
from time import sleep
import unittest
from random import randint
sys.path.append('../../Lib')
import time
import os
from appium_lib import *
from dx_action import *
from ui_comment import *
from ChnlRequest import ChnlRequest
from DbLib import DbLib
from config import *
from loglib import log

from elements_id import *
from common import exception_handler,get_now,time_range_for_audio
from screenshot import Appium_Extend

class AppQuitTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.mode = MODE
        self.db = DbLib()
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

        #进入音频页并查看通知栏
        get_to_article_by_search(self.driver,article,self.mode)
        sleep(WAIT_TIME)
        open_notifications(self.driver)
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',NOTIFICATION_AUDIO_PLAY)
        print u'Step %s:播放音频时通知栏上显示控制器测试：OK' % (str(step))
        step+=1
        close_notification(self.driver)
        sleep(WAIT_TIME)
        played_time = get_played_time(self.driver)
        start_time = time.time()

        #退出客户端并验证通知栏
        search_article_to_index(self.driver)
        quit_app(self.driver)
        open_notifications(self.driver)
        sleep(WAIT_TIME)
        assert notification_status_judge(self.driver,'pause')
        print u'Step %s:退出客户端后通知栏仍为播放状态测试：OK' % (str(step))
        step+=1

        #点击通知栏查看播放进度
        self.driver.find_element_by_id(NOTIFICATION_AUDIO_TITLE).click()
        played_time_now = get_played_time(self.driver)
        end_time = time.time()
        real_cost_time = time_range_for_audio(played_time,played_time_now)
        cost_time = end_time-start_time
        #print real_cost_time,cost_time
        assert abs(real_cost_time-cost_time)<=2
        print u'Step %s:退出客户端后音频仍在持续播放测试：OK' % (str(step))
        step+=1

    def pause_check(self,article):
        step = 1

        #进入音频页并查看通知栏
        get_to_article_by_search(self.driver,article,self.mode)
        sleep(WAIT_TIME)
        open_notifications(self.driver)
        sleep(WAIT_TIME)
        assert notification_status_judge(self.driver,'pause')
        print u'Step %s:播放音频时通知栏上显示控制器测试：OK' % (str(step))
        step+=1
        close_notification(self.driver)
        sleep(WAIT_TIME)
        played_time = get_played_time(self.driver)
        start_time = time.time()

        #退出当前页并在通知栏暂停音频
        search_article_to_index(self.driver)
        open_notifications(self.driver)
        sleep(WAIT_TIME)
        self.driver.find_element_by_id(NOTIFICATION_AUDIO_PLAY).click()
        end_time = time.time()
        assert notification_status_judge(self.driver,'play')

        #退出客户端并验证通知栏状态
        close_notification(self.driver)
        sleep(WAIT_TIME)
        quit_app(self.driver)
        open_notifications(self.driver)
        sleep(WAIT_TIME)
        assert notification_status_judge(self.driver,'play')
        print u'Step %s:退出客户端后通知栏仍为暂停状态测试：OK' % (str(step))
        step+=1

        #点击通知栏按钮可继续播放
        open_notifications(self.driver)
        sleep(WAIT_TIME)

        self.driver.find_element_by_id(NOTIFICATION_AUDIO_PLAY).click()
        start_time2 = time.time()
        assert notification_status_judge(self.driver,'pause')

        #进入详情页查看播放进度
        self.driver.find_element_by_id(NOTIFICATION_AUDIO_TITLE).click()
        sleep(WAIT_TIME)
        #real_time = played_time+end_time-start_time
        end_time2 = time.time()
        played_time_now = get_played_time(self.driver)
        cost_time = end_time-start_time
        cost_time2 = end_time2 -start_time2
        real_cost_time = time_range_for_audio(played_time,played_time_now)-cost_time-cost_time2

        #print played_time,played_time_now,real_cost_time,cost_time,cost_time2
        assert abs(real_cost_time)<=2
        print u'Step %s:退出客户端后音频仍在持续播放测试：OK' % (str(step))
        step+=1

    def back_check(self,article):
        step = 1
        #进入音频页
        get_to_article_by_search(self.driver,article,self.mode)
        sleep(WAIT_TIME)

        #退出客户端
        search_article_to_index(self.driver)
        sleep(WAIT_TIME)
        quit_app(self.driver)

        #点击通知栏控制器打开音频页面
        open_notifications(self.driver)
        sleep(WAIT_TIME)
        self.driver.find_element_by_id(NOTIFICATION_AUDIO_TITLE).click()
        sleep(WAIT_TIME)
        assert self.driver.current_activity == ACTIVITY.get(AUDIO_ARTICLE)
        print u'Step %s:点击通知栏跳转到音频详情页测试：OK' % (str(step))
        step+=1

        #点击返回跳转测试
        back(self.driver)
        sleep(WAIT_TIME)
        current = self.driver.current_activity
        assert current.find(self.desired_caps['appPackage']) == -1
        print u'Step %s:点击返回退出客户端测试：OK' % (str(step))
        step+=1

    #excute TestCase
    def testQuit(self):
        self.common_check(AUDIO_ARTICLE)

    def testNotificationPause(self):
        self.pause_check(AUDIO_ARTICLE)

    def testBackLocation(self):
        self.back_check(AUDIO_ARTICLE)


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

