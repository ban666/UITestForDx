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
from common import exception_handler,caclulate_for_audio,time_range_for_audio

class ElementsTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.mode = MODE
        self.db = DbLib()
        #self.api = ChnlRequest(self.mode)
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        start_to_index(self.driver,self.mode,'all')

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self):
        step = 1
        # 1、能够显示分享按钮、有入口返回列表页、评论数及评论列表入口
        #
        # 2、全屏显示音频框，音频框中包含音频标题、播放/暂停键、播放进度条、播放总时长、已播放时长和播放窗口背景图。
        get_to_article_by_search(self.driver,AUDIO_ARTICLE,self.mode)
        #菜单栏检查
        self.driver.find_element_by_id(AUDIO_MENU).click()
        menu_items = self.driver.find_elements_by_id(AUDIO_MENU_ITEMS)
        items = [u'写评论',u'分享']
        items = set(items)
        check_items = set()
        for item in menu_items:
            check_items.add(item.text)
        check_items = map(unicode,check_items)
        assert items.issubset(check_items)
        click_center(self.driver)

        #返回键检查
        assert self.driver.find_element_by_class_name('android.widget.ImageButton')

        #音频播放器元素检查
        elements_list = [AUDIO_BG,AUDIO_TITLE,AUDIO_ICON,AUDIO_PAUSE,AUDIO_PLAY_TIME,AUDIO_ALL_TIME,AUDIO_PROGRESS,AUDIO_MENU,COMMENT_AUDIO_ENTRANCE ]
        for el in elements_list:
            #print el
            assert self.driver.find_element_by_id(el)

        print u'Step %s:音频详情页元素检查测试：OK' % (str(step))
        step+=1


    #excute TestCase
    def testExsit(self):
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

