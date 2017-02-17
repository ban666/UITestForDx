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
from datetime import datetime,timedelta
from adb import *

class AricileCommentTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.mode = MODE
        self.db = DbLib()
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        start_to_index(self.driver,self.mode)
        if not is_login(self.driver):
            login_to_index(self.driver,TEST_PHONE)

    def tearDown(self):
        print 'Test End...................................'
        try:
             self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down'


    def common_check(self,article_name):
        step = 1

        #发布评论
        self.comid = self.db.get_latest_comid_by_article(article_name)
        #print self.comid
        #检测一分钟内逻辑
        go_to_mycomm(self.driver,self.mode)
        info = get_comment_info(self.driver,1,True)['loc_time']
        assert info.find(u'刚刚')!= -1
        print u'Step %s:一分钟内评论显示效果测试结果：OK' % (str(step))
        step+=1

        #修改时间为50分钟前并验证
        t = randint(1,59)
        #print t
        change_time = datetime.now()-timedelta(minutes=t)
        self.db.change_comment_time_by_id(self.comid,change_time)
        sleep(10)
        slide_down(self.driver)
        info = get_comment_info(self.driver,1,True)['loc_time']
        t_list = [-1,0,1]
        check_result = False
        for i in t_list:
            if info.find(str(t+i) + u'分钟前')!= -1:
                check_result = True
        assert check_result
        print u'Step %s:一小时内评论显示效果测试结果：OK' % (str(step))
        step+=1

        #修改时间为20小时前并验证
        t = randint(1,23)
        #print t
        change_time = datetime.now()-timedelta(hours=t)
        self.db.change_comment_time_by_id(self.comid,change_time)
        sleep(10)
        slide_down(self.driver)
        info = get_comment_info(self.driver,1,True)['loc_time']

        assert info.find(str(t) + u'小时前')!= -1
        print u'Step %s:一天内评论显示效果测试结果：OK' % (str(step))
        step+=1

        #修改时间为1天前并验证
        t = randint(1,10)
        change_time = datetime.now()-timedelta(t)
        self.db.change_comment_time_by_id(self.comid,change_time)
        slide_down(self.driver)
        info = get_comment_info(self.driver,1,True)['loc_time']
        assert info.find(change_time.strftime('%Y-%m-%d'))!= -1
        print u'Step %s:一天前评论显示效果测试结果：OK' % (str(step))
        step+=1

    #excute TestCase
    def testArticleComment(self):
        article = PHOTO_ARTICLE
        content = u'评论'+str(randint(1,1000))
        assert get_to_article_by_search(self.driver,article)
        go_to_comment_page(self.driver)
        send_comment(self.driver,content)
        back(self.driver)
        search_article_to_index(self.driver)
        self.common_check(article)



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

