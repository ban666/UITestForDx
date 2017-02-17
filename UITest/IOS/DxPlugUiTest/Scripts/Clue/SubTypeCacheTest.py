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
        self.clue = BaoliaoRequest()
        self.db = DbLib()
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        start_to_index(self.driver,self.mode)

    def tearDown(self):
        print 'Test End...................................'
        try:
            change_network(self.driver,'wifi')
            self.tsl.set_tc_status(self.case_id,self.result,self.msg)
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self):
        step = 1

        for i in range(4,8,1):
            self.clue.send_clue_and_review(u'报料测试'+str(randint(1,100)),1,subtype=i)

        go_to_clue(self.driver)

        sub_1 = self.driver.find_element_by_id(SUBTYPE_1).text
        sub_2 = self.driver.find_element_by_id(SUBTYPE_2).text
        sub_3 = self.driver.find_element_by_id(SUBTYPE_3).text
        sub_4 = self.driver.find_element_by_id(SUBTYPE_4).text

        for i in range(1,5,1):
            self.driver.find_element_by_id(eval('SUBTYPE_'+str(i))).click()
            sleep(WAIT_TIME)

        change_network(self.driver,'none')
        self.driver.quit()
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        start_to_index(self.driver,self.mode)
        sleep(WAIT_TIME)

        go_to_clue(self.driver)
        assert self.driver.find_element_by_id(SUBTYPE_1).text == sub_1
        assert self.driver.find_element_by_id(SUBTYPE_2).text == sub_2
        assert self.driver.find_element_by_id(SUBTYPE_3).text == sub_3
        assert self.driver.find_element_by_id(SUBTYPE_4).text == sub_4
        print u'Step %s:报料栏目名称均支持缓存测试：OK' % (str(step))
        step+=1

        for i in range(1,5,1):
            self.driver.find_element_by_id(eval('SUBTYPE_'+str(i))).click()
            sleep(WAIT_TIME)
            assert element_exsist(self.driver,'id',CLUE_LIST_DESC)
        print u'Step %s:报料四个栏目数据均支持缓存测试：OK' % (str(step))
        step+=1
        return True

    #excute TestCase
    def test(self):
        self.case_id = get_case(__file__)
        self.result = self.common_check()


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

