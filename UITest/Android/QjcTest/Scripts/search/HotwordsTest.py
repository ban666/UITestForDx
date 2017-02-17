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
from adb import is_login
from elements_id import *
from common import exception_handler

class HotwordsTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.mode = MODE
        self.db = DbLib()
        #self.api = ChnlRequest(self.mode)
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        start_to_index(self.driver,self.mode)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self):
        step = 1

        #点击热词
        get_to_search(self.driver)
        hotwords = self.driver.find_element_by_id(HOTWORDS_GROUP).find_elements_by_class_name('android.widget.TextView')
        hotwords[0].click()
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',NORMAL_TITLE) or element_exsist(self.driver,'id',SEARCH_EMPTY_TIPS)
        assert element_exsist(self.driver,'id',SEARCH_CANCEL)
        assert element_exsist(self.driver,'id',HOTWORDS_GROUP) == False
        print u'Step %s:点击热词可直接上框搜索测试：OK' % (str(step))
        step+=1

    #excute TestCase
    def testPlayCount(self):
        self.common_check()


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

