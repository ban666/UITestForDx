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


    def tearDown(self):
        print 'Test End...................................'
        try:
            self.db.set_update_version(self.version,force_ver='')
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self):
        step = 1

        #设置为自动强制更新时，更新测试
        up_ver = vesion_plus(self.version)
        self.db.set_update_version(up_ver,force_ver=self.version)
        self.driver.quit()
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        sleep(10)
        assert element_exsist(self.driver,*IGNORE_BUTTON) == False
        assert element_exsist(self.driver,*UPDATE_BUTTON) and element_exsist(self.driver,*UPDATE_DIALOG)
        self.driver.find_element(*UPDATE_BUTTON).click()
        # #self.driver.find_element(*BACK_APP_BUTTON).click()
        # for button in self.driver.find_elements_by_class_name('UIAButton'):
        #     if button.text.find(u'宜昌动向')!=-1:
        #         print button.text
        #         print button.size
        #         postion = get_el_center(button)
        #         print postion
        #         self.driver.tap([postion])
        #         button.click()
        assert element_exsist(self.driver,'id',u'精品推荐')
        print u'Step %s:强制更新可跳转到升级页面测试：OK' % (str(step))
        step+=1

        #设置为非强制更新时，更新测试
        self.db.set_update_version(up_ver,force_ver='')
        self.driver.quit()
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        sleep(10)
        assert element_exsist(self.driver,*IGNORE_BUTTON)
        assert element_exsist(self.driver,*UPDATE_BUTTON) and element_exsist(self.driver,*UPDATE_DIALOG)
        self.driver.find_element(*UPDATE_BUTTON).click()
        assert element_exsist(self.driver,'id',u'精品推荐')
        print u'Step %s:非强制更新可跳转到升级页面测试：OK' % (str(step))
        step+=1

        #设置为非强制更新时，更新测试
        # self.driver.quit()
        # self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        # sleep(10)
        # start_to_index(self.driver,self.mode)
        # go_to_settings(self.driver)
        # self.driver.find_element(*VERSIONS).click()
        # self.driver.find_element(*UPDATE_BUTTON).click()
        # assert element_exsist(self.driver,'id',u'精品推荐')
        # print u'Step %s:非强制更新时，在设置中手动检测更新可跳转到升级页面测试：OK' % (str(step))
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

