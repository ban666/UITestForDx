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
        subtype_id = self.clue.get_clue_type()[0]['subtype']
        self.clue.send_clue_and_review(u'报料测试'+str(randint(1,100)),1,subtype_id)
        self.api = ChnlRequest(MODE)
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        start_to_index(self.driver,self.mode)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.tsl.set_tc_status(self.case_id,self.result,self.msg)
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self):
        step = 1


        sleep(WAIT_TIME)
        go_to_clue(self.driver)
        #subtype_id = self.clue.get_clue_type()[0]['subtype'] #获取第一个栏目的报料类型ID
        # current_time = time.strftime( ISOTIMEFORMAT, time.localtime() )
        # clue_content = 'test for comment button '+str(current_time)
        # self.clue.send_clue(clue_content,subtype_id) #使用接口发送报料
        # clue_id = self.db.get_clueid_with_content_by_db(clue_content)


        comment_count = get_clue_comment_count(self.driver)
        assert int(comment_count) == 0
        #点击切换
        self.driver.find_element_by_id(CLUE_LIST_COMMENT_BUTTON).click()
        assert self.driver.current_activity == ACTIVITY.get('clue')
        assert  element_exsist(self.driver,'id',CLUE_LIST_DESC)
        print u'Step %s:报料无评论时，点击列表中评论按钮进入报料正文页：OK' % (str(step))
        step+=1


        return True

    def comment_jump_check(self):
        step = 1

        sleep(WAIT_TIME)
        subtype_id = self.clue.get_clue_type()[0]['subtype']
        clue_id = self.clue.get_clue_list(subtype_id)[0]['cid']
        for i in range(50):
            self.api.send_comment(clue_id,'test for comment anchor')
        go_to_clue(self.driver)
        slide_down(self.driver)
        comment_count = get_clue_comment_count(self.driver)
        assert int(comment_count) != 0
        #点击切换
        self.driver.find_element_by_id(CLUE_LIST_COMMENT_BUTTON).click()
        assert self.driver.current_activity == ACTIVITY.get('clue')
        assert  element_exsist(self.driver,'id',CLUE_LIST_DESC) == False
        print u'Step %s:报料有评论时，点击列表中报料的评论按钮，跳转到评论锚点：OK' % (str(step))
        step+=1

        return True

    #excute TestCase
    def test(self):
        self.case_id = get_case(__file__)
        self.result = self.common_check()

    def testCommentJump(self):
        self.case_id = get_case(__file__)
        self.result = self.comment_jump_check()
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

