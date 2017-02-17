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


class UnsupportTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.result = 'f'
        self.msg = ''
        self.tsl = TestlinkHandler()
        self.mode = MODE
        self.db = DbLib()
        self.jpush = JpushHandler()
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

    def common_check(self,model,infoid):
        step = 1
        sleep(WAIT_TIME)

        #推送一条不支持的新闻
        self.jpush.push_article(model,infoid)
        ret = confirm_push(self.driver,timeout=20)
        assert ret
        sleep(WAIT_TIME)
        texts = self.driver.find_elements_by_class_name('UIAStaticText')
        texts = [x.text for x in texts]
        assert MSG.get('unsupport') in texts
        print u'Step %s:推送不识别类型可正确跳转到提示界面测试：OK' % (str(step))
        step+=1

        #推送一条不支持的新闻
        push_info = self.db.get_push_info_by_name(UNSUPPORT_ARTICLE)

        self.jpush.push_article(push_info['model'],push_info['infoid'])
        ret = confirm_push(self.driver,timeout=20)
        assert ret

        texts = self.driver.find_elements_by_class_name('UIAStaticText')
        texts = [x.text for x in texts]
        assert u'不识别测试' in texts
        # contexts = self.driver.contexts
        # self.driver.switch_to.context(contexts[-1])
        # el = self.driver.find_element_by_tag_name('img')
        # print dir(el)
        print u'Step %s:客户端不识别的model新闻有对应的web页时，打开对应的web页：OK' % (str(step))
        step+=1

        return True


    #excute TestCase
    def testNonContent(self):
        unsupport = [789,123]
        self.case_id = get_case(__file__)
        self.result = self.common_check(*unsupport)

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

