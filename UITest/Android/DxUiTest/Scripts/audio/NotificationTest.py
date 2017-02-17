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
from common import exception_handler,get_now,get_time_total
from screenshot import Appium_Extend

class NotificationTest(unittest.TestCase):

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
        elements_list = [NOTIFICATION_AUDIO_ICON,NOTIFICATION_AUDIO_TITLE,NOTIFICATION_AUDIO_PLAY,NOTIFICATION_AUDIO_CLOSE]
        for el in elements_list:
            assert element_exsist(self.driver,'id',el)
        print u'Step %s:音频播放器开启即创建通知栏控制器测试：OK' % (str(step))
        step+=1
        print u'Step %s:通知栏元素检查测试：OK' % (str(step))
        step+=1

    def jump_check(self,article):
        step = 1

        #进入音频页
        get_to_article_by_search(self.driver,article,self.mode)
        sleep(WAIT_TIME)

        #退出当前页并将客户端后台
        search_article_to_index(self.driver)
        home(self.driver)
        sleep(WAIT_TIME)

        #点击通知栏控制器验证跳转
        open_notifications(self.driver)
        sleep(WAIT_TIME)
        notification_title = self.driver.find_element_by_id(NOTIFICATION_AUDIO_TITLE).text
        self.driver.find_element_by_id(NOTIFICATION_AUDIO_TITLE).click()
        sleep(WAIT_TIME)
        article_title = self.driver.find_element_by_id(AUDIO_TITLE).text
        assert notification_title == article_title
        assert self.driver.current_activity == ACTIVITY.get(AUDIO_ARTICLE)
        assert get_played_time(self.driver) != '00:00'
        print u'Step %s:点击通知栏播放跳转对应详情页测试：OK' % (str(step))
        step+=1

    def finish_check(self,article):
        step = 1

        #进入音频页并拖動進度條等待音頻播放完成
        get_to_article_by_search(self.driver,article,self.mode)
        sleep(WAIT_TIME)
        all_time = get_time_total(get_alltime(self.driver))
        seekbar_sendkey(self.driver,0.99)
        wait = all_time*0.01+5
        sleep(wait)
        assert get_played_time(self.driver)  == '00:00'
        assert element_exsist(self.driver,'id',AUDIO_START)

        #
        open_notifications(self.driver)
        sleep(WAIT_TIME)
        notification_status_judge(self.driver,'play')
        print u'Step %s:音频播放完成后通知按钮变为播放测试：OK' % (str(step))
        step+=1

        self.driver.find_element_by_id(NOTIFICATION_AUDIO_PLAY).click()
        close_notification(self.driver)
        sleep(WAIT_TIME)
        assert get_played_time(self.driver) != '00:00'
        print u'Step %s:点击通知栏播放可重新播放测试：OK' % (str(step))
        step+=1

    #excute TestCase
    def testPlayCount(self):
        self.common_check(AUDIO_ARTICLE)

    def testFinish(self):
        self.finish_check(AUDIO_ARTICLE)

    def testJump(self):
        self.jump_check(AUDIO_ARTICLE)
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

