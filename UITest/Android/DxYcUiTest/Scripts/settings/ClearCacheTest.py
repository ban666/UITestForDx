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
import re
from appium_lib import *
from dx_action import *
from ui_comment import *
from ChnlRequest import ChnlRequest
from DbLib import DbLib
from config import *
from loglib import log
from elements_id import *
from ui_settings import *
from adb import push_file
from configrw import get_case
from TestlinkHandler import TestlinkHandler

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
        #self.api = ChnlRequest(MODE)
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        start_to_index(self.driver,self.mode)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.tsl.set_tc_status(self.case_id,self.result,self.msg)
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self):
        step = 1

        go_to_settings(self.driver)

        cache_txt = self.driver.find_element_by_id(CACHE_CLEAR).text

        assert cache_txt.find('B')!=-1

        print u'Step %s:展示清理缓存的入口，展示样式为：标识+“清理缓存”文字+缓存数据大小：OK' % (str(step))
        step+=1
        return True

    def tips_check(self):
        step = 1

        go_to_settings(self.driver)

        self.driver.find_element_by_id(CACHE_CLEAR).click()
        txt = self.driver.find_element_by_id(CACHE_TIPS).text
        print txt
        assert txt == MSG.get('cache_tips')
        print u'Step %s:单击清理缓存时弹出确认是否清理缓存的提示框，提示语与需求一致：OK' % (str(step))
        step+=1
        return True

    def display_check(self):
        step = 1

        path = '/data/data/com.cnhubei.ycdx/cache/Image'

        go_to_settings(self.driver)

        clear_cache(self.driver)

        self.driver.find_element_by_id(INFORMATION).click()
        push = IMAGE_PATH+'/'+IMAGES.get('image_10.2')
        push_file(push,path)
        sleep(WAIT_TIME)

        go_to_settings(self.driver)
        txt = self.driver.find_element_by_id(CACHE_CLEAR).text
        print txt
        pat = '(\d+\.\d+)'
        assert re.findall(pat,txt)[0]>='10.2'
        print u'Step %s:缓存大小<=30MB时，显示为实际值，保留2位小数：OK' % (str(step))
        step+=1

        self.driver.find_element_by_id(INFORMATION).click()
        sleep(WAIT_TIME)

        push = IMAGE_PATH+'/'+IMAGES.get('image_30')
        push_file(push,path)
        go_to_settings(self.driver)
        txt = self.driver.find_element_by_id(CACHE_CLEAR).text
        assert txt == u'大于 30MB'
        clear_cache(self.driver)
        print u'Step %s:缓存大于30M时，显示为“大于30MB”：OK' % (str(step))
        step+=1
        return True

    def cancel_check(self):
        step = 1

        path = '/data/data/com.cnhubei.ycdx/cache/Image'

        go_to_settings(self.driver)

        clear_cache(self.driver)

        self.driver.find_element_by_id(INFORMATION).click()
        push = IMAGE_PATH+'/'+IMAGES.get('image_10.2')
        push_file(push,path)
        sleep(WAIT_TIME)

        go_to_settings(self.driver)
        txt = self.driver.find_element_by_id(CACHE_CLEAR).text
        self.driver.find_element_by_id(CACHE_CLEAR).click()
        self.driver.find_element_by_id(CACHE_CLEAR_CANCEL).click()
        assert self.driver.find_element_by_id(CACHE_CLEAR).text == txt
        self.driver.find_element_by_id(INFORMATION).click()
        go_to_settings(self.driver)
        assert self.driver.find_element_by_id(CACHE_CLEAR).text == txt
        print u'Step %s:设置中清理缓存时点击取消，能够关闭对话框，不清理缓存：OK' % (str(step))
        step+=1
        return True

    def clear_check(self):
        step = 1

        go_to_settings(self.driver)

        clear_cache(self.driver)

        self.driver.find_element_by_id(INFORMATION).click()
        push = IMAGE_PATH+'/'+IMAGES.get('image_10.2')
        push_file(push,path)
        sleep(WAIT_TIME)

        go_to_settings(self.driver)
        txt = self.driver.find_element_by_id(CACHE_CLEAR).text
        self.driver.find_element_by_id(CACHE_CLEAR).click()
        self.driver.find_element_by_id(CACHE_CLEAR_CANCEL).click()
        assert self.driver.find_element_by_id(CACHE_CLEAR).text == txt
        self.driver.find_element_by_id(INFORMATION).click()
        go_to_settings(self.driver)
        assert self.driver.find_element_by_id(CACHE_CLEAR).text == txt
        print u'Step %s:设置中清理缓存时点击取消，能够关闭对话框，不清理缓存：OK' % (str(step))
        step+=1
        return True

    #excute TestCase
    def test(self):
        self.case_id = get_case(__file__)
        self.result = self.common_check()

    def testTips(self):
        self.case_id = get_case(__file__)
        self.result = self.tips_check()

    def testCacheDisplay(self):
        self.case_id = get_case(__file__)
        self.result = self.display_check()

    def testCancel(self):
        self.case_id = get_case(__file__)
        self.result = self.cancel_check()


if __name__ == '__main__':
    pass
    # a = TestLogin()
    # a.setUp()
    # a.testFunc1()
    # a.tearDown()
    #d =DbLib()

