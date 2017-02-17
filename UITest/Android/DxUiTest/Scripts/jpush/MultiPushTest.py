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

class MultiPushTest(unittest.TestCase):

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

    def common_check(self):
        step = 1
        #发表评论
        type_title = self.driver.find_element_by_id('com.cnhubei.dxxwhw:id/tv_typetitle').text
        print type_title
        assert type_title == u'精彩评论'
        print u'Step %s:评论页存在精彩评论测试：OK' % (str(step))
        step+=1

    #excute TestCase
    def testPushMsg(self):
        step = 1
        go_to_settings(self.driver)
        sleep(WAIT_TIME)
        assert set_push_state(self.driver,'true')
        clear_notification(self.driver)


        msg1 = u'test1'
        msg2 = u'test2'
        self.jpush.push_notification(msg1)
        self.jpush.push_notification(msg2)
        ret = get_push_info(self.driver)
        assert len(ret) == 2 and msg1 in ret and msg2 in ret
        print u'Step %s:推送多条消息时测试：OK' % (str(step))
        step+=1

    def testPushArticle(self):
        step = 1
        go_to_settings(self.driver)
        sleep(WAIT_TIME)
        assert set_push_state(self.driver,'true')
        clear_notification(self.driver)


        msg1 = u'test1'
        msg2 = u'test2'

        push_info_a = self.db.get_push_info_by_name(NORMAL_ARTICLE)
        push_info_b = self.db.get_push_info_by_name(PHOTO_ARTICLE)
        self.jpush.push_article(push_info_a['model'],push_info_a['infoid'],msg =msg1)
        self.jpush.push_article(push_info_b['model'],push_info_b['infoid'],msg =msg2)
        ret = get_push_info(self.driver)
        print ret
        assert len(ret) == 2 and msg1 in ret and msg2 in ret
        print u'Step %s:推送多条新闻时测试：OK' % (str(step))
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

