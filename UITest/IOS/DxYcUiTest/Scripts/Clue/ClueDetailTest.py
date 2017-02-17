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
        st = self.clue.get_clue_type()[0]['subtype']
        self.clue.send_clue_and_review(u'报料测试'+str(randint(1,100)),1,st,pic_list=[IMAGE_PATH+'/'+IMAGES.get('image1')]*randint(1,9),reply=u'审查通过')
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

    def digg_check(self):
        step = 1


        sleep(WAIT_TIME)
        go_to_clue(self.driver)

        self.driver.find_element_by_id(CLUE_LIST_DESC).click()
        sleep(WAIT_TIME)
        assert self.driver.current_activity == ACTIVITY.get('clue')

        old_digg_count = self.driver.find_element_by_id(CLUE_DETAIL_DIGG_COUNT).text
        self.driver.find_element_by_id(CLUE_DETAIL_DIGG_BUTTON).click()
        new_digg_count = self.driver.find_element_by_id(CLUE_DETAIL_DIGG_COUNT).text
        assert int(old_digg_count)+1 == int(new_digg_count)
        print u'Step %s:报料详情页能够对帖子点赞：OK' % (str(step))
        step+=1

        return True

    def common_check(self):
        step = 1


        sleep(WAIT_TIME)
        go_to_clue(self.driver)

        self.driver.find_element_by_id(CLUE_LIST_DESC).click()
        sleep(WAIT_TIME)
        assert self.driver.current_activity == ACTIVITY.get('clue')

        #用户头像、用户昵称、发布时间、报料栏目、报料正文（可包含1-9张图片）、地理位置、处理结果。
        el_list = [CLUE_LIST_ICON,CLUE_LIST_USERNAME,CLUE_LIST_TIME,CLUE_DETAIL_SUBTYPE,CLUE_LIST_DESC,CLUE_LIST_PIC,CLUE_LOCATION,CLUE_DETAIL_REPLY_TXT]
        for el in el_list:
            element_exsist(self.driver,'id',el)
        print u'Step %s:报料详情中需显示：用户头像、用户昵称、发布时间、报料栏目、报料正文（可包含1-9张图片）、地理位置、处理结果。：OK' % (str(step))
        step+=1

        return True

    def share_check(self):
        step = 1


        sleep(WAIT_TIME)
        go_to_clue(self.driver)

        self.driver.find_element_by_id(CLUE_LIST_DESC).click()
        sleep(WAIT_TIME)
        assert self.driver.current_activity == ACTIVITY.get('clue')

        self.driver.find_element_by_id(CLUE_LIST_SHARE_BUTTON).click()

        assert element_exsist(self.driver,'id',SHARE_METHOD_TEXT)
        print u'Step %s:报料详情页能够点击分享：OK' % (str(step))
        step+=1

        return True

    def slide_check(self):
        step = 1

        sleep(WAIT_TIME)
        go_to_clue(self.driver)

        self.driver.find_element_by_id(CLUE_LIST_DESC).click()
        sleep(WAIT_TIME)
        assert self.driver.current_activity == ACTIVITY.get('clue')

        #click back button
        self.driver.find_element_by_class_name('android.widget.ImageButton').click()
        assert element_exsist(self.driver,'id',CLUE_SEARCH)
        print u'Step %s:报料详情页点击返回按钮生效：OK' % (str(step))
        step+=1

        self.driver.find_element_by_id(CLUE_LIST_DESC).click()
        sleep(WAIT_TIME)
        assert self.driver.current_activity == ACTIVITY.get('clue')

        #右划
        slide_right(self.driver)
        assert element_exsist(self.driver,'id',CLUE_SEARCH)
        print u'Step %s:报料详情页右划手势按钮生效：OK' % (str(step))
        step+=1
        return True

    #excute TestCase
    def test(self):
        self.case_id = get_case(__file__)
        self.result = self.common_check()

    def testDigg(self):
        self.case_id = get_case(__file__)
        self.result = self.digg_check()

    def testShare(self):
        self.case_id = get_case(__file__)
        self.result = self.share_check()

    def testSlide(self):
        self.case_id = get_case(__file__)
        self.result = self.slide_check()

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