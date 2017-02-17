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

class UnsupportTest(unittest.TestCase):

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

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self,model,infoid):
        step = 1
        sleep(WAIT_TIME)
        go_to_settings(self.driver)
        sleep(WAIT_TIME)
        assert set_push_state(self.driver,'true')
        clear_notification(self.driver)

        #推送一条不支持的新闻
        self.jpush.push_article(model,infoid)
        ret = get_push_el(self.driver,timeout=20)
        assert len(ret)==1
        open_notifications(self.driver)
        ret[0].click()
        sleep(WAIT_TIME)

        assert self.driver.current_activity == ACTIVITY.get('unsupport')
        # contexts = self.driver.contexts
        # self.driver.switch_to.context(contexts[-1])
        # el = self.driver.find_element_by_tag_name('img')
        # print dir(el)
        print u'Step %s:推送不识别类型可正确跳转到提示界面测试：OK' % (str(step))
        step+=1

    #excute TestCase
    def testBasic(self):
        unsupport = [789,123]
        self.common_check(*unsupport)
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

