# -*- coding: utf-8 -*-
__author__ = 'liaoben'

import sys
from appium import webdriver
from appium.webdriver.errorhandler import WebDriverException
from time import sleep
import unittest
from random import randint
sys.path.append('../../Lib')
from appium_lib import *
from DbLib import DbLib
from config import *
from loglib import log
from elements_id import *
from ui_settings import *
from jpush_handler import JpushHandler
from ui_push import *
from configrw import get_case
from TestlinkHandler import TestlinkHandler
from adb import download_and_install


class DefaultTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        #下载新包并重新安装
        assert download_and_install()
        #self.desired_caps['appActivity'] = ACTIVITY.get('first_start')
        self.result = 'f'
        self.msg = ''
        self.tsl = TestlinkHandler()
        self.mode = MODE
        self.db = DbLib()
        self.jpush = JpushHandler()
        #self.api = ChnlRequest(self.mode)
        try:
            self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        except Exception,e:
            pass
        finally:
            try:
                self.driver.quit()
            except:
                pass
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        start_to_index(self.driver,self.mode)

    def tearDown(self):
        print 'Test End...................................'
        try:
             self.tsl.set_tc_status(self.case_id,self.result,self.msg)
             self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e


    #excute TestCase
    def test(self):
        self.case_id = get_case(__file__)

        step = 1
        go_to_settings(self.driver)
        sleep(WAIT_TIME)
        assert get_push_state(self.driver) == 'true'
        print u'Step %s:设置中消息推送默认开启测试：OK' % (str(step))
        step+=1

        self.result = True

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

