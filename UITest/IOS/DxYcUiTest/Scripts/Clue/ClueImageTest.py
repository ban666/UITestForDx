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
from configrw import get_case
from TestlinkHandler import TestlinkHandler
from ui_clue import *
from BaoliaoRequest import BaoliaoRequest
from adb import download_and_install
from Queue import Queue
from threading import Thread
from package import start_capture,get_result
from image_handler import CnvHandler

class SubTypeTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.result = 'f'
        self.msg = ''
        self.tsl = TestlinkHandler()
        self.mode = MODE
        self.db = DbLib()
        download_and_install()
        self.api = ChnlRequest(MODE)


    def tearDown(self):
        print 'Test End...................................'
        try:
            sleep(30)
            self.tsl.set_tc_status(self.case_id,self.result,self.msg)
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self,content,pic_width,pic_height,mode,msg):
        step = 1

        q = Queue()
        start_capture(q,70,'test.cnhubei.com','GET')
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        start_to_index(self.driver,self.mode)

        window_size = self.driver.get_window_size()
        x = window_size['width']
        y = window_size['height']
        print x,y
        sleep(WAIT_TIME)

        sleep(5)
        go_to_clue(self.driver)
        sleep(WAIT_TIME)
        self.driver.find_element_by_id(CLUE_SEARCH).click()
        self.driver.find_element_by_id(CLUE_SEARCH_EDIT).send_keys(content)
        sleep(WAIT_TIME)
        self.driver.press_keycode(66)
        sleep(WAIT_TIME)
        l = get_result(q)
        print l
        cnv_list = []
        for pac in l:
            if pac[0] == '/mcp/cutter/cnv':

                h = pac[1]['h']
                w = pac[1]['w']
                q = pac[1]['q']
                cnv_list.append((int(w),int(h),int(q)))

        ch = CnvHandler(self.driver,pic_width,pic_height,mode)
        #expect_w,expect_h,expect_q = ch.calculator()
        print 'cnv_list',cnv_list
        expect = ch.calculator()
        print 'expect',expect
        assert expect in cnv_list
        print u'Step %s:%s测试通过：OK' % (str(step),msg)
        step+=1

        return True


    #excute TestCase
    def test(self):
        self.case_id = get_case(__file__)
        msg = u'单图缩略图横图，宽等比缩放后小于1200时，裁剪请求'
        self.result = self.common_check('900*500',900,500,1,msg)

    def test2(self):
        self.case_id = get_case(__file__)
        msg = u'单图缩略图竖图，高等比缩放后小于1600，裁剪请求'
        self.result = self.common_check('500*900',500,900,1,msg)

    def test3(self):
        self.case_id = get_case(__file__)
        msg = u'九宫格缩略图横图，宽等比缩放后小于1200，裁剪请求'
        self.result = self.common_check(u'九宫格横图缩放后小于1200',2161,960,9,msg)

    def test4(self):
        self.case_id = get_case(__file__)
        msg =  u'九宫格缩略图竖图，高等比缩放后小于1600，裁剪请求'
        self.result = self.common_check(u'九宫格竖图缩放后小于1600',960,2461,9,msg)

    def test5(self):
        self.case_id = get_case(__file__)
        msg = u'单方图缩略图裁剪请求'
        self.result = self.common_check(u'单方图',900,900,1,msg)

    def test6(self):
        self.case_id = get_case(__file__)
        msg = u'九宫格方图缩略图裁剪请求'
        self.result = self.common_check(u'九宫格方图',900,900,9,msg)

if __name__ == '__main__':
    setp=1
    msg=u'中文'
    print u'Step %s:%s测试通过：OK' % (str(setp),msg)