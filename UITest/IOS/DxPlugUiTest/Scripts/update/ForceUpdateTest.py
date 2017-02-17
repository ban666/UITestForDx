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
from ui_settings import *
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
        self.db.set_update_version('1.0.0',force_ver='')
        #self.api = ChnlRequest(self.mode)
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        sleep(10)
        start_to_index(self.driver,self.mode)
        go_to_settings(self.driver)
        self.version = get_version_code(self.driver)
        db_ver = self.db.get_update_version()['version']
        if db_ver <= self.version:
            up_ver = vesion_plus(self.version)
            self.db.set_update_version(up_ver,force_ver=self.version)
        self.driver.quit()
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        sleep(10)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.db.set_update_version(self.version,force_ver='')
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self):
        step = 1

        assert element_exsist(self.driver,*IGNORE_BUTTON) == False
        assert element_exsist(self.driver,*UPDATE_BUTTON) and element_exsist(self.driver,*UPDATE_DIALOG)
        back(self.driver)
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,*IGNORE_BUTTON) == False
        assert element_exsist(self.driver,*UPDATE_BUTTON) and element_exsist(self.driver,*UPDATE_DIALOG)
        print u'Step %s:强制更新无法取消和忽略此版本测试：OK' % (str(step))
        step+=1

        self.driver.quit()
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        sleep(10)
        assert element_exsist(self.driver,*IGNORE_BUTTON) == False
        assert element_exsist(self.driver,*UPDATE_BUTTON) and element_exsist(self.driver,*UPDATE_DIALOG)
        print u'Step %s:退出客户端，再次启动客户端时仍会弹出升级提示测试：OK' % (str(step))
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
    db =DbLib()

    # import HTMLTestRunner
    # t = unittest.TestSuite()
    # t.addTest(unittest.makeSuite(TestComment))
    # #unittest.TextTestRunner.run(t)
    # filename = 'F:\\dx_comment.html'
    # fp = file(filename,'wb')
    # runner = HTMLTestRunner.HTMLTestRunner(
    #         stream = fp,
    #         title ='Dx_Test',
    #         description = 'Report_discription')
    #
    # runner.run(t)
    # fp.close()
    db.set_update_version('1.0.1',force_ver='')

