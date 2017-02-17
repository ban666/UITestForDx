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
        go_to_settings(self.driver)
        version = get_version_code(self.driver)
        db_ver = self.db.get_update_version()['version']
        if db_ver <= version:
            up_ver = vesion_plus(version)
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

        el_list = [UPDATE_MSG,IGNORE_BOX,BUTTON_OK,BUTTON_CANCEL]
        assert element_exsist(self.driver,'id',UPDATE_MSG)
        print u'Step %s:服务器有更新包时，wifi环境弹出更新提示框测试：OK' % (str(step))
        step+=1
        for el in el_list:
            assert element_exsist(self.driver,'id',el)
        print u'Step %s:更新提示框中包含版本升级提示、忽略更新框、更新和取消按钮测试：OK' % (str(step))
        step+=1
        self.driver.find_element_by_id(BUTTON_CANCEL).click()
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',UPDATE_MSG) == False
        self.driver.quit()
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        sleep(10)
        assert element_exsist(self.driver,'id',BUTTON_CANCEL)
        print u'Step %s:更新提示框中选择以后再说，提示框消失后重启客户端提示框依然存在测试：OK' % (str(step))
        step+=1

        return True

    #excute TestCase
    def test(self):
        self.case_id = get_case(__file__)
        self.result = self.common_check()

    def testElements(self):
        self.case_id = get_case(__file__)
        self.result = self.common_check()

    def testRemind(self):
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
