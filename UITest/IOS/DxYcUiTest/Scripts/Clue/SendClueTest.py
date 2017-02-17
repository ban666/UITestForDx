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
from adb import get_config_by_adb
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
        self.clue = BaoliaoRequest()
        self.db = DbLib()
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        start_to_index(self.driver,self.mode)
        if not is_login(self.desired_caps['appPackage']):
            login_to_index(self.driver,TEST_PHONE)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.tsl.set_tc_status(self.case_id,self.result,self.msg)
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self):
        step = 1

        go_to_clue(self.driver)
        dc = get_config_by_adb()['dc']
        for i in range(4):
            self.driver.find_element_by_id(SEND_CLUE_BUTTON).click()
            content = u'发送报料测试'+str(randint(1,10000))
            assert send_txt_clue(self.driver,i,content)
            assert element_exsist(self.driver,'id',CLUE_LIST_MY_CLUE_ENTRY)
            sleep(WAIT_TIME)
            self.clue.review_head(dc,1)
            self.driver.find_element_by_id(eval('SUBTYPE_'+str(i+1))).click()
            slide_down(self.driver)
            assert self.driver.find_element_by_id(CLUE_LIST_DESC).text == content
            print u'Step %s:第%d个频道发布报料能够发布成功测试：OK' % (str(step),i+1)
            step+=1
        return True

    def name_check(self):
        step = 1
        subtype_ret = self.db.get_subtype_by_db()
        subtype_ret = [x.get('name').decode('utf-8') for x in subtype_ret]
        go_to_clue(self.driver)

        self.driver.find_element_by_id(SEND_CLUE_BUTTON).click()
        sleep(WAIT_TIME)

        self.driver.find_element_by_id(SEND_CLUE_TYPE_CHOOSE).click()
        subtype_choose_list = self.driver.find_elements_by_id(SEND_CLUE_TYPE_TXT)
        for sub in range(len(subtype_choose_list)):
            assert subtype_choose_list[sub].text == subtype_ret[sub]
        print u'Step %s:发布报料界面栏目选择与服务器配置一致：OK' % (str(step))
        step+=1

        return True

    def locatioon_check(self,loc):
        step = 1

        go_to_clue(self.driver)
        dc = get_config_by_adb()['dc']
        self.driver.find_element_by_id(SEND_CLUE_BUTTON).click()
        content = u'发送报料测试'+str(randint(1,10000))
        assert send_txt_clue(self.driver,0,content,loc=loc)
        assert element_exsist(self.driver,'id',CLUE_LIST_MY_CLUE_ENTRY)
        sleep(WAIT_TIME)
        self.clue.review_head(dc,1)
        self.driver.find_element_by_id(eval('SUBTYPE_'+str(0+1))).click()
        slide_down(self.driver)
        assert self.driver.find_element_by_id(CLUE_LIST_DESC).text == content
        print u'Step %s:非匿名发布时默认地理位置能够手动修改测试：OK' % (str(step))
        step+=1
        return True

    #excute TestCase
    def test(self):
        self.case_id = get_case(__file__)
        self.result = self.common_check()

    def testSubTypeName(self):
        self.case_id = get_case(__file__)
        self.result = self.name_check()

    def testLocationEdit(self):
        self.case_id = get_case(__file__)
        loc = u'武汉市洪山区吴家湾33号'
        self.result = self.locatioon_check(loc)

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

