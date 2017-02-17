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
from adb import *

class VideoPushTest(unittest.TestCase):

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

    #excute TestCase
    def testLive(self):
        # go_to_settings(self.driver)
        # print get_version_code(self.driver)
        # #self.driver.quit()
        # update_info = self.db.get_update_info_by_db()
        # self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        # sleep(WAIT_TIME)
        update_info = self.db.get_update_info_by_db()
        print update_info


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

