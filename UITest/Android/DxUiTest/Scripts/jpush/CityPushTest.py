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

class CityPushTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.mode = MODE
        self.db = DbLib()
        self.jpush = JpushHandler()
        #self.api = ChnlRequest(self.mode)
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        start_to_index(self.driver,self.mode)
        sleep(WAIT_TIME)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    #excute TestCase
    def testCityPush(self):
        step = 1
        go_to_settings(self.driver)
        sleep(WAIT_TIME)
        assert set_push_state(self.driver,'true')
        clear_notification(self.driver)

        app_location = '宜昌'
        push_location = '大悟'
        push_location_code = self.db.get_domaincode_by_name(push_location)
        app_location_code = self.db.get_domaincode_by_name(app_location)
        #print push_location_code,app_location_code
        msg1 = u'test'
        assert set_location(self.driver,app_location)
        push_info_a = self.db.get_push_info_by_name(NORMAL_ARTICLE)
        print self.jpush.push_notification(msg1,audience=push_location_code)
        ret = get_push_info(self.driver)
        assert ret == False
        clear_notification(self.driver)
        sleep(WAIT_TIME)
        print u'Step %s:无法接受其他地域推送测试：OK' % (str(step))
        step+=1


        print self.jpush.push_notification(msg1,audience=app_location_code)
        ret = get_push_info(self.driver)
        assert ret[0] == msg1
        clear_notification(self.driver)
        sleep(WAIT_TIME)
        print u'Step %s:可正确接收地域推送测试：OK' % (str(step))
        step+=1

        print self.jpush.push_notification(msg1)
        ret = get_push_info(self.driver)
        assert ret[0] == msg1
        clear_notification(self.driver)
        sleep(WAIT_TIME)
        print u'Step %s:可正确接收全部地区推送测试：OK' % (str(step))
        step+=1



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

