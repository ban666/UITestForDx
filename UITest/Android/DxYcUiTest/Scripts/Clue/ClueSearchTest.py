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
        self.clue = BaoliaoRequest()
        #st = self.clue.get_clue_type()[0]['subtype']
        #self.clue.send_clue_and_review(u'报料测试'+str(randint(1,100)),1,st,pic_list=[IMAGE_PATH+'/'+IMAGES.get('image1')]*randint(1,9),reply=u'审查通过')
        self.api = ChnlRequest(MODE)
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        start_to_index(self.driver,self.mode)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.tsl.set_tc_status(self.case_id,self.result,self.msg)
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self,content):
        step = 1


        sleep(WAIT_TIME)
        go_to_clue(self.driver)

        self.driver.find_element_by_id(CLUE_SEARCH).click()
        sleep(WAIT_TIME)
        self.driver.find_element_by_id(CLUE_SEARCH_EDIT).send_keys(content)
        sleep(WAIT_TIME)
        self.driver.press_keycode(66)
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',SEARCH_EMPTY_TIPS)
        assert self.driver.find_element_by_id(SEARCH_EMPTY_TIPS).text == u'找不到与“%s”相符的结果' % (content)
        print u'Step %s:搜索无结果能够提示：OK' % (str(step))
        step+=1

        return True

    def jump_check(self,content):
        step = 1

        sleep(WAIT_TIME)
        go_to_clue(self.driver)

        self.driver.find_element_by_id(CLUE_SEARCH).click()
        sleep(WAIT_TIME)
        self.driver.find_element_by_id(CLUE_SEARCH_EDIT).send_keys(content)
        sleep(WAIT_TIME)
        self.driver.press_keycode(66)
        sleep(WAIT_TIME)
        self.driver.find_elements_by_class_name('android.widget.ImageView')[2].click()
        sleep(WAIT_TIME)
        print self.driver.current_activity
        assert self.driver.current_activity == ACTIVITY.get('clue_pic')
        print u'Step %s:点击搜索结果中的图片能够进入图集模式：OK' % (str(step))
        step+=1

        back(self.driver)
        sleep(WAIT_TIME)
        self.driver.find_element_by_id(CLUE_LIST_DESC).click()
        sleep(WAIT_TIME)
        assert self.driver.current_activity == ACTIVITY.get('clue')
        print u'Step %s:搜索报料后，点击报料正文能够进入报料详情页：OK' % (str(step))
        step+=1

        return True

    def style_check(self,content):
        step = 1

        sleep(WAIT_TIME)
        go_to_clue(self.driver)

        self.driver.find_element_by_id(CLUE_SEARCH).click()
        sleep(WAIT_TIME)
        self.driver.find_element_by_id(CLUE_SEARCH_EDIT).send_keys(content)
        sleep(WAIT_TIME)
        self.driver.press_keycode(66)
        sleep(WAIT_TIME)

        el_list = [CLUE_LIST_ICON,CLUE_LIST_USERNAME ,CLUE_LIST_TIME ,CLUE_LIST_FLAG ,CLUE_LIST_DESC,CLUE_LIST_PIC,CLUE_SEARCH_LIST_TYPE]
        loc_el = CLUE_LOCATION
        #点击切换
        for el in el_list:
            assert element_exsist(self.driver,'id',el)
        assert element_exsist(self.driver,'id',loc_el) == False
        print u'Step %s:报料列表格式显示正确：OK' % (str(step))
        step+=1
        return True

    #excute TestCase
    def test(self):
        self.case_id = get_case(__file__)
        search_txt = u'11111111111111111123131231'
        self.result = self.common_check(search_txt)

    def testJump(self):
        self.case_id = get_case(__file__)
        search_txt = u'900*500'
        self.result = self.jump_check(search_txt)

    def testStyle(self):
        self.case_id = get_case(__file__)
        search_txt = u'九宫格竖图缩放后小于1600'
        self.result = self.style_check(search_txt)


if __name__ == '__main__':
    pass
    # a = TestLogin()
    # a.setUp()
    # a.testFunc1()
    # a.tearDown()
    #d =DbLib()

    bl = BaoliaoRequest()
    st = bl.get_clue_type()[0]['subtype']
    print st
    bl.send_clue_and_review(u'报料测试'+str(randint(1,100)),1,st,location='123')