# -*- coding: utf-8 -*-
__author__ = 'liaoben'

import sys
from appium import webdriver
from time import sleep
import unittest
from random import randint
sys.path.append('../../Lib')
import time
import os
from appium_lib import *
from dx_action import *
from ui_comment import *
from ChnlRequest import ChnlRequest
from DbLib import DbLib
from config import *
from loglib import log
from elements_id import *
from configrw import get_case
from TestlinkHandler import TestlinkHandler
from ui_clue import *
from BaoliaoRequest import BaoliaoRequest

class SubTypeTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.result = 'f'
        self.msg = ''
        self.tsl = TestlinkHandler()
        self.mode = MODE
        self.db = DbLib()
        self.clue = BaoliaoRequest()
        st = self.clue.get_clue_type()[0]['subtype']
        self.clue.send_clue_and_review(u'报料测试'+str(randint(1,100)),1,st)
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        start_to_index(self.driver,self.mode)
        if is_login(self.desired_caps['appPackage']):
            logout_to_index(self.driver,self.mode)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.tsl.set_tc_status(self.case_id,self.result,self.msg)
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self):
        step = 1

        go_to_clue(self.driver)

        self.driver.find_element_by_id(SEND_CLUE_BUTTON).click()
        #print self.driver.current_activity
        assert self.driver.current_activity == ACTIVITY.get('login')
        print u'Step %s:未登录时发布报料能够跳转登录：OK' % (str(step))
        step+=1

        sleep(WAIT_TIME)
        login(self.driver,self.mode,self.desired_caps['appPackage'],TEST_PHONE,DEVICE_TID,True)
        sleep(WAIT_TIME)
        print self.driver.current_activity
        assert self.driver.current_activity == ACTIVITY.get('clue_reply')
        print u'Step %s:登录后能够跳转到发布报料界面：OK' % (str(step))
        step+=1
        return True

    def name_check(self):
        step = 1
        subtype_ret = self.db.get_subtype_by_db()
        subtype_ret = [x.get('name').decode('utf-8') for x in subtype_ret]
        go_to_clue(self.driver)

        self.driver.find_element_by_id(SEND_CLUE_BUTTON).click()
        sleep(WAIT_TIME)

        self.driver.find_element_by_id(SEND_CLUE_TYPE_CHOOSE).click()
        subtype_choose_list = self.driver.find_elements_by_id(SEND_CLUE_TYPE_TXT)
        for sub in range(len(subtype_choose_list)):
            assert subtype_choose_list[sub].text == subtype_ret[sub]
        print u'Step %s:发布报料界面栏目选择与服务器配置一致：OK' % (str(step))
        step+=1

        return True

    def comment_check(self):
        step = 1

        go_to_clue(self.driver)

        self.driver.find_element_by_id(CLUE_LIST_DESC).click()
        sleep(WAIT_TIME)

        #发表评论
        content = u'中文'+str(randint(1,100))
        #content = u'一'*140
        send_comment(self.driver,content)
        sleep(5)
        new_comment = self.driver.find_element_by_id(COMMENT)
        info = get_comment_info(self.driver,new_comment,0)
        check_reply_elements = check_comment(self.driver,new_comment)
        assert check_reply_elements == 1
        assert info[3] == content
        assert info[2].find(u'宜昌动向网友') !=-1
        print u'Step %s:未登录可发表评论测试结果：OK' % (str(step))
        step+=1

        return True

    #excute TestCase
    def test(self):
        self.case_id = get_case(__file__)
        self.result = self.common_check()

    def testSubTypeName(self):
        self.case_id = get_case(__file__)
        self.result = self.name_check()

    def testComment(self):
        self.case_id = get_case(__file__)
        self.result = self.comment_check()
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

