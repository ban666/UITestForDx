# -*- coding: utf-8 -*-
__author__ = 'liaoben'

import sys
from appium import webdriver
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


# class JpushBasicTest(unittest.TestCase):
#
#     def setUp(self):
#         #self.testcases = conf.readcfg(__file__)
#         self.desired_caps = desired_caps
#         print 'Test Start...................................'
#         self.result = 'f'
#         self.msg = ''
#         self.tsl = TestlinkHandler()
#         self.mode = MODE
#         self.db = DbLib()
#         self.jpush = JpushHandler()
#         #self.api = ChnlRequest(self.mode)
#         self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
#         start_to_index(self.driver,self.mode)
#         sleep(WAIT_TIME)
#
#     def tearDown(self):
#         print 'Test End...................................'
#         try:
#              self.tsl.set_tc_status(self.case_id,self.result,self.msg)
#              self.driver.quit()
#         except Exception as e:
#             print u'测试失败，失败环节:tear down',e
#
#
#
#     def test(self):
#         self.case_id = get_case(__file__)
#         step = 1
#         go_to_settings(self.driver)
#         sleep(WAIT_TIME)
#         assert set_push_state(self.driver,'true')
#         clear_notification(self.driver)
#         msg1 = u'test1'
#         self.jpush.push_notification(msg1)
#         ret = get_push_info(self.driver)
#         assert ret[0] ==msg1
#         print u'Step %s:推送开关打开时可接收推送测试：OK' % (str(step))
#         step+=1
#
#         #关闭推送并测试10秒内是否收的到
#         clear_notification(self.driver)
#         assert set_push_state(self.driver,'false')
#         msg2 = u'test2'
#         self.jpush.push_notification(msg2)
#         sleep(WAIT_TIME)
#         ret = get_push_info(self.driver,timeout=20)
#         assert ret == False
#         print u'Step %s:推送关闭时无法接收推送测试：OK' % (str(step))
#         step+=1
#
#         #等待20秒打开推送
#         sleep(20)
#         assert set_push_state(self.driver,'true')
#         assert get_push_info(self.driver)[0] == msg2
#         print u'Step %s:消息保留时间内打开通知开关接收推送测试：OK' % (str(step))
#         step+=1
#
#         #关闭网络后推送，等待20秒打开网络
#         assert set_push_state(self.driver,'true')
#         clear_notification(self.driver)
#         change_network(self.driver,'none')
#         msg3 = u'test3'
#         self.jpush.push_notification(msg3)
#         sleep(WAIT_TIME)
#         ret = get_push_info(self.driver,timeout=20)
#         assert ret == False
#         sleep(20)
#         change_network(self.driver,'wifi')
#         assert get_push_info(self.driver,timeout=20)[0] == msg3
#         assert set_push_state(self.driver,'true')
#         print u'Step %s:消息保留时间内重新打开网络接收推送测试：OK' % (str(step))
#         step+=1
#         self.result = True


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

