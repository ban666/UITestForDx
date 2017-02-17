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
from adb import del_ignore_version_by_adb,clear_cache_by_adb

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
        go_to_settings(self.driver)
        self.version = get_version_code(self.driver)
        up_ver = vesion_plus(self.version)
        self.db.set_update_version(up_ver)
        self.driver.quit()
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        sleep(10)

    def tearDown(self):
        print 'Test End...................................'
        try:
             self.tsl.set_tc_status(self.case_id,self.result,self.msg)
             self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self):
        step = 1

        # el_list = [UPDATE_MSG,IGNORE_BOX,BUTTON_OK,BUTTON_CANCEL]
        assert element_exsist(self.driver,*UPDATE_MSG)

        self.driver.find_element(*IGNORE_BUTTON).click()
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,*UPDATE_DIALOG) == False
        self.driver.quit()
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        sleep(10)
        assert element_exsist(self.driver,*UPDATE_DIALOG) == False
        print u'Step %s:设置为忽略此版本后，启动时客户端不弹出此版本的升级提示测试：OK' % (str(step))
        step+=1

        go_to_settings(self.driver)
        self.driver.find_element(*VERSIONS).click()
        el_list = [UPDATE_DIALOG,UPDATE_BUTTON,IGNORE_BUTTON]
        for el in el_list:
            assert element_exsist(self.driver,*el)
        print u'Step %s:设置为忽略此版本后，在设置中手动检测版本仍能弹出升级提示测试：OK' % (str(step))
        step+=1

        up_ver = vesion_plus(self.version,2)
        self.db.set_update_version(up_ver)
        self.driver.quit()
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        sleep(10)
        assert element_exsist(self.driver,*UPDATE_DIALOG)
        print u'Step %s:存在非忽略版本的版本升级时，仍能弹出升级提示测试：OK' % (str(step))
        step+=1


        # up_ver = vesion_plus(self.version)
        # self.db.set_update_version(up_ver)
        # self.driver.quit()
        # del_ignore_version_by_adb()
        # clear_cache_by_adb()
        # self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        # sleep(10)
        # assert element_exsist(self.driver,'id',UPDATE_MSG)
        #
        # print u'Step %s:清除忽略版本配置后，可自动弹出升级提示测试：OK' % (str(step))
        # step+=1

        return True

    #excute TestCase
    # def test(self):
    #     self.case_id = get_case(__file__)
    #     self.result = self.common_check()


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

