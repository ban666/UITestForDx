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

        sub_1 = self.driver.find_element_by_id(SUBTYPE_1)
        sub_2 = self.driver.find_element_by_id(SUBTYPE_2)
        sub_3 = self.driver.find_element_by_id(SUBTYPE_3)
        sub_4 = self.driver.find_element_by_id(SUBTYPE_4)

        sub_list = [sub_1,sub_2,sub_3,sub_4]

        # assert sub_1.text == u'投诉'
        # assert sub_2.text == u'咨询'
        # assert sub_3.text == u'求助'
        # assert sub_4.text == u'建议'

        assert get_checked(sub_1) == True
        assert get_checked(sub_2) == False
        assert get_checked(sub_3) == False
        assert get_checked(sub_4) == False

        #点击切换
        for sub in sub_list:
            sub.click()
            assert get_checked(sub) == True
        print u'Step %s:点击切换报料测试：OK' % (str(step))
        step+=1

        #左划切换
        for i in range(len(sub_list)-1):
            slide_right(self.driver,per=3)
            sleep(3)
            index = len(sub_list)-2-i
            #print index
            assert get_checked(sub_list[index]) == True
        print u'Step %s:右划切换我的报料测试：OK' % (str(step))
        step+=1

        #右划切换
        for i in range(len(sub_list)-1):
            slide_left(self.driver)
            sleep(3)
            assert get_checked(sub_list[i+1]) == True
        print u'Step %s:左划切换我的报料测试：OK' % (str(step))
        step+=1

        return True

    def name_check(self):
        step = 1
        subtype_ret = self.db.get_subtype_by_db()
        subtype_ret = [x.get('name').decode('utf-8') for x in subtype_ret]
        go_to_clue(self.driver)

        sub_1 = self.driver.find_element_by_id(SUBTYPE_1).text
        sub_2 = self.driver.find_element_by_id(SUBTYPE_2).text
        sub_3 = self.driver.find_element_by_id(SUBTYPE_3).text
        sub_4 = self.driver.find_element_by_id(SUBTYPE_4).text

        sub_list = [sub_1,sub_2,sub_3,sub_4]
        for i in range(len(sub_list)):
            print sub_list[i],subtype_ret[i]
            assert sub_list[i] == subtype_ret[i]
        print u'Step %s:报料栏目名称与服务器配置一致：OK' % (str(step))
        step+=1

        self.driver.find_element_by_id(SEND_CLUE_BUTTON).click()
        sleep(WAIT_TIME)

        self.driver.find_element_by_id(SEND_CLUE_TYPE_CHOOSE).click()
        subtype_choose_list = self.driver.find_elements_by_id(SEND_CLUE_TYPE_TXT)
        for sub in range(len(subtype_choose_list)):
            assert subtype_choose_list[sub].text == subtype_ret[sub]
        print u'Step %s:报料分类选择内容与服务器配置一致：OK' % (str(step))
        step+=1

        return True

    #excute TestCase
    def test(self):
        self.case_id = get_case(__file__)
        self.result = self.common_check()

    def testSubTypeName(self):
        self.case_id = get_case(__file__)
        self.result = self.name_check()

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

