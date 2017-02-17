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
from common import exception_handler,get_now,time_range_for_audio,get_time_total,caclulate_for_audio

class BackTest(unittest.TestCase):

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

        #退出到其他页面后播放器持续播放
        get_to_article_by_search(self.driver,article,self.mode)
        sleep(WAIT_TIME)
        all_time = get_time_total(get_alltime(self.driver))
        play_time = self.driver.find_element_by_id(AUDIO_PLAY_TIME)
        while play_time.text == '00:00':
            sleep(WAIT_TIME)
        play_time_old = play_time.text
        #print play_time_old
        back(self.driver)
        sleep(5)
        self.driver.find_element_by_class_name('android.widget.RelativeLayout')\
            .find_element_by_class_name('android.widget.TextView').click()
        sleep(2)
        play_time_new = play_time.text
        #print play_time_new
        time_range = time_range_for_audio(play_time_old,play_time_new)
        assert time_range >= 7
        print u'Step %s:切换到客户端其他页面时音频继续播放测试：OK' % (str(step))
        step +=1

        #退出详情页等待音频播放完成再次进入，验证播放完成效果
        seekbar_sendkey(self.driver,0.95)
        wait = all_time*0.05
        back(self.driver)
        sleep(wait+10)
        self.driver.find_element_by_class_name('android.widget.RelativeLayout')\
            .find_element_by_class_name('android.widget.TextView').click()
        assert element_exsist(self.driver,'id',AUDIO_START)
        assert get_played_time(self.driver) == '00:00'
        print u'Step %s:音频播放完成效果测试：OK' % (str(step))
        step +=1

        #手动触发重新播放
        self.driver.find_element_by_id(AUDIO_START).click()
        sleep(10)
        assert get_time_total(get_played_time(self.driver))>0
        print u'Step %s:手动触发重新播放测试：OK' % (str(step))
        # step+=1

    #excute TestCase
    def testPlayCount(self):
        self.common_check(AUDIO_ARTICLE)


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

