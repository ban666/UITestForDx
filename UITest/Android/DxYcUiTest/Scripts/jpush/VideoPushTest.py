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

class VideoPushTest(unittest.TestCase):

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

    def live_video_check(self,article):
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
        #sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',LIVE_VIDEO_BAR) == True
        assert self.driver.current_activity == ACTIVITY.get(article)
        print u'Step %s:推送直播类型视频，客户端以直播类型播放测试：OK' % (str(step))
        step+=1

        return True

    def video_check(self,article):
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
        #sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',LIVE_VIDEO_BAR) == False
        assert self.driver.current_activity == ACTIVITY.get(article)
        print u'Step %s:推送非直播类型视频，客户端以非直播类型播放测试：OK' % (str(step))
        step+=1

        return True

    #excute TestCase
    def testLive(self):
        self.case_id = get_case(__file__)
        self.result = self.live_video_check(LIVE_VIDEO_ARTICLE)

    def testVideo(self):
        self.case_id = get_case(__file__)
        self.result = self.video_check(VIDEO_ARTICLE)
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

