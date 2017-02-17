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
from ui_comment import *
from elements_id import *
from ui_settings import *
from jpush_handler import JpushHandler
from ui_push import *
from configrw import get_case
from TestlinkHandler import TestlinkHandler

class ArticlePushTest(unittest.TestCase):

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

    def common_check(self,article):
        step = 1
        # sleep(WAIT_TIME)
        # go_to_settings(self.driver)
        # sleep(WAIT_TIME)
        # assert set_push_state(self.driver,'true')
        # clear_notification(self.driver)


        push_info = self.db.get_push_info_by_name(article)

        self.jpush.push_article(push_info['model'],push_info['infoid'])
        ret = confirm_push(self.driver,timeout=20)
        assert ret
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'class','UIAWebView')
        print u'Step %s:点击普通新闻推送跳转测试：OK' % (str(step))
        step+=1

        #验证工具栏存在
        elements_list = [FONT_BUTTON,COMMENT_INPUT_IN_ARTICLE,SHARE_BUTTON,COLLECT_BUTTON]
        for el in elements_list:
            print el
            assert element_exsist(self.driver,*el) == True
        print u'Step %s:正文页工具栏显示测试：OK' % (str(step))
        step+=1

        self.driver.find_element(*SHARE_BUTTON).click()
        for method in SHARE_METHOD.values():
            assert element_exsist(self.driver,*method)
        click_center(self.driver)
        print u'Step %s:正文页推送分享测试：OK' % (str(step))
        step+=1

        content = u'中文'+str(randint(1,100))
        send_comment(self.driver,content,COMMENT_INPUT_IN_ARTICLE)
        sleep(5)
        slide_left(self.driver)
        assert element_exsist(self.driver,*AMAZING_COMMENT_TIPS)
        print u'Step %s:左划进入评论页测试：OK' % (str(step))
        step+=1

        info = get_comment_info(self.driver,1)
        assert info['content'] == content
        print u'Step %s:正文页发表评论测试结果：OK' % (str(step))
        step+=1
        return True

    #excute TestCase
    def test(self):
        self.case_id = get_case(__file__)
        self.result = self.common_check(NORMAL_ARTICLE)

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

