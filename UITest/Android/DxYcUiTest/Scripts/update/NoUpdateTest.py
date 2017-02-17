# -*- coding: utf-8 -*-
__author__ = 'liaoben'

import sys
sys.path.append('../../Lib')
from appium import webdriver
from time import sleep
import unittest
from appium_lib import *
from dx_action import *
from ui_comment import *
from ChnlRequest import ChnlRequest
from DbLib import DbLib
from config import *
from loglib import log
from elements_id import *
from common import exception_handler,vesion_plus
from ui_push import *
from configrw import get_case
from TestlinkHandler import TestlinkHandler

class UpdateBasicTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.result = 'f'
        self.msg = ''
        self.tsl = TestlinkHandler()
        self.mode = MODE
        self.db = DbLib()
        #self.api = ChnlRequest(self.mode)
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
        version = get_version_code(self.driver)
        db_ver = self.db.get_update_version()['version']
        if db_ver > version:
            self.db.set_update_version(version)
        self.driver.quit()
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        start_to_index(self.driver,self.mode)
        sleep(10)

        #验证设置中手动升级情况
        go_to_settings(self.driver)
        self.driver.find_element_by_id(VERSION).click()
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',VERSION)
        print u'Step %s:服务器未配置升级时，设置中手动检测到无更新且不弹出任何窗口测试：OK' % (str(step))
        step+=1
        # el_list = [UPDATE_MSG,BUTTON_OK,BUTTON_CANCEL]
        # for el in el_list:
        #     assert element_exsist(self.driver,'id',el)
        # self.driver.find_element_by_id(BUTTON_CANCEL).click()
        # self.driver.find_element_by_id(VERSION).click()
        # self.driver.find_element_by_id(BUTTON_OK).click()
        # assert self.driver.current_activity == ACTIVITY.get('install')
        # print u'Step %s:非强制更新时，设置中手动检测到更新将会弹出提示，更新和取消功能有效测试：OK' % (str(step))
        # step+=1
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

