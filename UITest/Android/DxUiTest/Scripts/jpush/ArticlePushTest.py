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

class ArticlePushTest(unittest.TestCase):

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

    def common_check(self,article):
        step = 1
        sleep(WAIT_TIME)
        go_to_settings(self.driver)
        sleep(WAIT_TIME)
        assert set_push_state(self.driver,'true')
        clear_notification(self.driver)


        push_info = self.db.get_push_info_by_name(article)

        self.jpush.push_article(push_info['model'],push_info['infoid'])
        ret = get_push_el(self.driver,timeout=20)
        assert len(ret)==1
        #print ret
        open_notifications(self.driver)
        ret[0].click()
        sleep(WAIT_TIME)
        print self.driver.current_activity
        assert self.driver.current_activity == ACTIVITY.get(article)
        print u'Step %s:点击普通新闻推送跳转测试：OK' % (str(step))
        step+=1

        #验证工具栏存在
        elements_list = [TOOLBAR_ITEM,COMMENT_ITEM,SHARE_BUTTON,COLLECT_BOTTON]
        for el in elements_list:
            print el
            assert element_exsist(self.driver,'id',el) == True
        print u'Step %s:正文页工具栏显示测试：OK' % (str(step))
        step+=1

        #验证左划进入评论
        slide_left(self.driver)
        sleep(WAIT_TIME)
        assert self.driver.current_activity == ACTIVITY.get('comment')
        print u'Step %s:左划进入评论页测试：OK' % (str(step))
        step+=1

    #excute TestCase
    def testBasic(self):
        self.common_check(NORMAL_ARTICLE)

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

