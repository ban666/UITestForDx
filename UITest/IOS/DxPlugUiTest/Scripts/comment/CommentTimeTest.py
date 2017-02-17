# -*- coding: utf-8 -*-
__author__ = 'liaoben'

import sys
from appium import webdriver
from time import sleep
import unittest
from random import randint
sys.path.append('../../Lib')
import time
from appium_lib import *
from dx_action import *
from ui_comment import *
from ChnlRequest import ChnlRequest
from DbLib import DbLib
from config import *
from loglib import log
from elements_id import *
from common import exception_handler
from configrw import get_case
from TestlinkHandler import TestlinkHandler
from datetime import datetime,timedelta

class AricileCommentTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.result = 'f'
        self.msg = ''
        self.tsl = TestlinkHandler()
        self.mode = MODE
        self.db = DbLib()
        self.api = ChnlRequest(self.mode)
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        start_to_index(self.driver,self.mode)
        # if not is_login(self.desired_caps['appPackage']):
        #     login_to_index(self.driver,TEST_PHONE)

    def tearDown(self):
        print 'Test End...................................'
        try:
             self.tsl.set_tc_status(self.case_id,self.result,self.msg)
             self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e


    def common_check(self,article_name):
        step = 1

        #发布评论
        self.comid = self.api.send_comment_by_name(article_name,'comment time test')

        #检测一分钟内逻辑
        get_to_article_by_search(self.driver,article_name,self.mode)
        go_to_comment_page(self.driver)
        info = get_comment_info(self.driver,1)['loc_time'].split()[-1]
        print info
        assert info.find(u'刚刚')!= -1
        print u'Step %s:一分钟内评论显示效果测试结果：OK' % (str(step))
        step+=1

        #修改时间为50分钟前并验证
        t = randint(1,59)
        change_time = datetime.now()-timedelta(minutes=t)
        self.db.change_comment_time_by_id(self.comid,change_time)
        slide_down(self.driver)
        info = get_comment_info(self.driver,1)['loc_time'].split()[-1]
        print info,str(t)
        assert abs(int(info.replace(u'分钟前',''))-t)<=1
        print u'Step %s:一小时内评论显示效果测试结果：OK' % (str(step))
        step+=1

        #修改时间为20小时前并验证
        t = randint(1,23)
        change_time = datetime.now()-timedelta(hours=t)
        self.db.change_comment_time_by_id(self.comid,change_time)
        slide_down(self.driver)
        info = get_comment_info(self.driver,1)['loc_time'].split()[-1]
        print info,str(t)
        assert abs(int(info.replace(u'小时前',''))-t)<=1
        print u'Step %s:一天内评论显示效果测试结果：OK' % (str(step))
        step+=1

        #修改时间为1天前并验证
        t = randint(1,10)
        change_time = datetime.now()-timedelta(t)
        self.db.change_comment_time_by_id(self.comid,change_time)
        slide_down(self.driver)
        info = get_comment_info(self.driver,1)['loc_time'].split()[-1]
        print info,str(t)
        assert info.find(change_time.strftime('%Y-%m-%d'))!= -1
        print u'Step %s:一天前评论显示效果测试结果：OK' % (str(step))
        step+=1

        return True

    #excute TestCase
    def testArticleComment(self):
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

