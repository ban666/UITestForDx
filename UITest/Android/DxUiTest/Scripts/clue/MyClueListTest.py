# -*- coding: utf-8 -*-
__author__ = 'ld'

import sys
from appium import webdriver
from time import sleep
import unittest
from random import randint
sys.path.append('../../Lib')
import time
import os
from adb import *
from appium_lib import *
from dx_action import *
from ui_comment import *
from DbLib import DbLib
from config import *
from ui_clue import *
from ui_search import *
from screenshot import Appium_Extend

from elements_id import *

class MyClueListTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.db = DbLib()
        self.mode = MODE
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        self.extend = Appium_Extend(self.driver)
        start_to_index(self.driver,self.mode)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def send_clue(self,count = 0):
        current_time = time.strftime( ISOTIMEFORMAT, time.localtime() )
        content = str(count) + ' test for cluelist ' + str(current_time)
        send_txt_clue(self.driver,content,0,False,False)
        return content

    def testSlideDownMyClueList(self):
        result = True
        BeLogin(self.driver)
        go_to_clue(self.driver)
        content =  self.send_clue()
        cluelist_to_myclue(self.driver)
        frist_clue_state = self.driver.find_elements_by_id(CLUE_REVIEW_STATE)[0].text
        if frist_clue_state != u'未审核':
            result = False
        self.db.review_clue_by_content(content)
        slide_down(self.driver)
        sleep(WAIT_TIME)
        frist_clue_state = self.driver.find_elements_by_id(CLUE_REVIEW_STATE)[0].text
        if frist_clue_state != u'审核通过':
            print u'FAIL!!!--------------------------》列表没有被更新！'
            result = False
        else:
            print u'列表刷新成功'
        assert result

    def testMyClueListPageDown(self):
        result = True
        BeLogin(self.driver)
        go_to_clue(self.driver)
        # content = '1 test for cluelist\n ' + '2017-02-16 09:16:03'
        content = self.send_clue(1)
        for i in range(2,22,1):
            self.send_clue(i)
        cluelist_to_myclue(self.driver)
        sleep(WAIT_TIME)
        change_network(self.driver,'none')
        sleep(2)
        confirm1 = element_exsist_in_list(self.driver,'name',SYSTEMCONFIRM)
        if confirm1:
            confirm1.click()
        is_bottom = element_exsist(self.driver,'id',SEARCH_EMPTY_TIPS)
        trynum = 0
        while not is_bottom or trynum < 15:
            slide_up(self.driver,6,2)
            sleep(3)
            is_bottom = element_exsist(self.driver,'id',SEARCH_EMPTY_TIPS)
            trynum += 1
        if is_bottom:
            if self.driver.find_element_by_id(SEARCH_EMPTY_TIPS).text == PAGEDOWNERROR:
                print u'加载失败提示语正确'
            else:
                print u'FAIL!!!---------------------》加载失败提示语错误'
        else:
            result = False
            print u'FAIL!!!---------------------》页面底部没有显示加载状态栏'
        change_network(self.driver,'all')
        sleep(3)
        confirm2 = element_exsist_in_list(self.driver,'name',SYSTEMCONFIRM)
        if confirm2:
            confirm2.click()
        sleep(WAIT_TIME)
        self.driver.find_element_by_id(SEARCH_EMPTY_TIPS).click()
        slide_up(self.driver)
        sleep(WAIT_TIME)
        if not element_exsist(self.driver,'name',content):
            result = False
            print u'FAIL!!!-----------------------》翻页失败'
        else:
            print u'翻页加载成功'
        assert result






