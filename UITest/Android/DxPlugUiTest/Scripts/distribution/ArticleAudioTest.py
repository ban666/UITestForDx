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
from adb import is_login
from elements_id import *
from common import exception_handler,get_now,time_range_for_audio,get_time_total


class ArticleAudioTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.mode = MODE
        self.db = DbLib()
        #self.api = ChnlRequest(self.mode)
        remote_url = get_appium_url_from_config()
        self.driver = webdriver.Remote(remote_url, self.desired_caps)
        start_to_index(self.driver,self.mode)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self,article):
        step = 1

        #进入含音频的正文页
        get_to_article_by_search(self.driver,article,self.mode)
        sleep(8)

        #切换到webview并打开音频
        # self.driver.switch_to.context(self.driver.contexts[-1])
        # self.driver.find_element_by_class_name('audio-start').click()
        # sleep(WAIT_TIME)
        # self.driver.switch_to.context(self.driver.contexts[0])
        #由於不同手機webview機制不同，此處採取坐標點擊方式實現
        click_audio_in_webview(self.driver)

        #切换回NATIVE并验证详情页与通知栏播放器是否存在

        open_notifications(self.driver)
        sleep(WAIT_TIME)
        elements_list = [NOTIFICATION_AUDIO_ICON,NOTIFICATION_AUDIO_TITLE,NOTIFICATION_AUDIO_PLAY,NOTIFICATION_AUDIO_CLOSE]
        for el in elements_list:
            assert element_exsist(self.driver,'id',el)
        print u'Step %s:正文页播放音频时通知栏播放器打开测试：OK' % (str(step))
        step +=1

        close_notification(self.driver)
        sleep(WAIT_TIME)
        article_el_list = [AUDIO_PAUSE,AUDIO_PLAY_TIME,AUDIO_ALL_TIME,AUDIO_PROGRESS,AUDIO_CLOSE]
        for el in article_el_list:
            assert element_exsist(self.driver,'id',el)
        print u'Step %s:正文页播放音频时详情页播放器打开测试：OK' % (str(step))
        step +=1

        #关闭播放器并验证通知栏是否销毁
        self.driver.find_element_by_id(AUDIO_CLOSE).click()
        for el in article_el_list:
            assert element_exsist(self.driver,'id',el) == False
        open_notifications(self.driver)
        sleep(WAIT_TIME)
        for el in elements_list:
            assert element_exsist(self.driver,'id',el) == False
        print u'Step %s:点击关闭按钮播放器销毁测试：OK' % (str(step))

    def location_check(self,article):
        step = 1

        #进入含音频的正文页
        get_to_article_by_search(self.driver,article,self.mode)
        sleep(8)

        #切换到webview并打开音频
        # self.driver.switch_to.context(self.driver.contexts[-1])
        # self.driver.find_element_by_class_name('audio-start').click()
        # sleep(WAIT_TIME)
        # self.driver.switch_to.context(self.driver.contexts[0])
        #由於不同手機webview機制不同，此處採取坐標點擊方式實現
        click_audio_in_webview(self.driver)


        #切换回NATIVE判断播放状态下上下滑动，播放器的位置

        location = self.driver.find_element_by_id(AUDIO_TITLE).location #取title的位置作为固定值
        slide_up(self.driver)
        location_up = self.driver.find_element_by_id(AUDIO_TITLE).location
        slide_custom(self.driver,0.5,0.5,0.5,0.9)
        location_down = self.driver.find_element_by_id(AUDIO_TITLE).location
        #print location,location_down,location_up
        assert location == location_down == location_up
        print u'Step %s:正文页播放器处于播放状态时上下滑动位置不变测试：OK' % (str(step))
        step +=1


        #验证暂停状态下上下滑动，播放器的位置
        self.driver.find_element_by_id(AUDIO_PAUSE).click()
        location = self.driver.find_element_by_id(AUDIO_TITLE).location #取title的位置作为固定值
        slide_up(self.driver)
        location_up = self.driver.find_element_by_id(AUDIO_TITLE).location
        slide_custom(self.driver,0.5,0.5,0.5,0.9)
        location_down = self.driver.find_element_by_id(AUDIO_TITLE).location
        #print location,location_down,location_up
        assert location == location_down == location_up
        print u'Step %s:正文页播放器处于暂停状态时上下滑动位置不变测试：OK' % (str(step))
        step +=1

    def back_check(self,article):
        step = 1

        #进入含音频的正文页
        get_to_article_by_search(self.driver,article,self.mode)
        sleep(8)

        #切换到webview并打开音频
        # self.driver.switch_to.context(self.driver.contexts[-1])
        # self.driver.find_element_by_class_name('audio-start').click()
        # sleep(WAIT_TIME)
        # self.driver.switch_to.context(self.driver.contexts[0])
        #由於不同手機webview機制不同，此處採取坐標點擊方式實現
        click_audio_in_webview(self.driver)


        #切换回NATIVE

        start_play_time = get_played_time(self.driver)
        start_time = time.time()

        #退出当前页
        search_article_to_index(self.driver)
        sleep(10)

        #回到文章页验证音频是否持续播放
        get_to_article_by_search(self.driver,article,self.mode)
        sleep(WAIT_TIME)

        end_play_time = get_played_time(self.driver)
        end_time = time.time()
        print time_range_for_audio(end_play_time,start_play_time),end_time-start_time
        assert abs(time_range_for_audio(start_play_time,end_play_time)-(end_time-start_time)) <=5
        assert element_exsist(self.driver,'id',AUDIO_PAUSE)
        print u'Step %s:正文页音频播放时退出详情页，播放未完成时返回详情页测试：OK' % (str(step))
        step +=1

        #等待音频播放完成进入详情页
        seekbar_sendkey(self.driver,0.9)
        wait = get_time_total(get_alltime(self.driver))*0.1
        search_article_to_index(self.driver)
        sleep(wait+5)
        get_to_article_by_search(self.driver,article,self.mode)
        sleep(WAIT_TIME)
        #验证音频框仍然展示，且为初始状态
        assert element_exsist(self.driver,'id',AUDIO_START)
        assert get_played_time(self.driver) == '00:00'
        #点击播放可重新播放
        self.driver.find_element_by_id(AUDIO_START).click()
        sleep(WAIT_TIME)
        assert get_played_time(self.driver) != '00:00'
        print u'Step %s:正文页音频播放时退出详情页，播放完成返回详情页测试：OK' % (str(step))
        step +=1

    def destroy_check(self,article):
        step = 1

        #进入含音频的正文页
        get_to_article_by_search(self.driver,article,self.mode)
        sleep(8)

        #切换到webview并打开音频
        # self.driver.switch_to.context(self.driver.contexts[-1])
        # self.driver.find_element_by_class_name('audio-start').click()
        # sleep(WAIT_TIME)
        # self.driver.switch_to.context(self.driver.contexts[0])
        #由於不同手機webview機制不同，此處採取坐標點擊方式實現
        click_audio_in_webview(self.driver)

        #切换回NATIVE并暂停播放

        assert element_exsist(self.driver,'id',AUDIO_PAUSE)
        open_notifications(self.driver)
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',NOTIFICATION_AUDIO_TITLE)
        close_notification(self.driver)
        sleep(WAIT_TIME)
        self.driver.find_element_by_id(AUDIO_PAUSE).click()
        search_article_to_index(self.driver)
        sleep(WAIT_TIME)
        #验证通知栏播放器是否销毁
        open_notifications(self.driver)
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',NOTIFICATION_AUDIO_TITLE) == False
        print u'Step %s:正文页音频暂停退出后，通知栏播放器销毁测试：OK' % (str(step))
        step +=1
        #重新进入文章页
        close_notification(self.driver)
        sleep(WAIT_TIME)
        get_to_article_by_search(self.driver,article,self.mode)
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',AUDIO_TITLE) == False
        print u'Step %s:正文页音频暂停退出后，文章页播放器销毁测试：OK' % (str(step))
        step +=1

    #excute TestCase
    def testDestroy(self):
        self.common_check(NORMAL_AUDIO_ARTICLE)

    def testPlayerLocation(self):
        self.location_check(NORMAL_AUDIO_ARTICLE)

    def testBack(self):
        self.back_check(NORMAL_AUDIO_ARTICLE)

    def testPauseBack(self):
        self.destroy_check(NORMAL_AUDIO_ARTICLE)
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

