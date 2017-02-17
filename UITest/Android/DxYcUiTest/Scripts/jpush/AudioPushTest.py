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

class AudioPushTest(unittest.TestCase):

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

    def article_audio_check(self,article):
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


        click_audio_in_webview(self.driver)

        #切换回NATIVE并暂停播放
        self.driver.switch_to.context(self.driver.contexts[0])
        assert element_exsist(self.driver,'id',AUDIO_PAUSE)
        assert self.driver.current_activity == ACTIVITY.get(article)
        print u'Step %s:推送含音频的新闻详情页时，客户端能打开详情页并播放测试：OK' % (str(step))
        step+=1
        return True

    def audio_check(self,article):
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
        assert element_exsist(self.driver,'id',AUDIO_PAUSE)
        assert self.driver.current_activity == ACTIVITY.get(article)
        print u'Step %s:推送音频时，客户端进入音频详情页自动播放测试：OK' % (str(step))
        step+=1
        return True

    def play_audio_check(self):
        step = 1
        sleep(WAIT_TIME)
        go_to_settings(self.driver)
        sleep(WAIT_TIME)
        assert set_push_state(self.driver,'true')
        clear_notification(self.driver)

        self.driver.find_element_by_id(INFORMATION).click()

        get_to_article_by_search(self.driver,AUDIO_ARTICLE,self.mode)

        push_info = self.db.get_push_info_by_name(AUDIO_ARTICLE_B)

        self.jpush.push_article(push_info['model'],push_info['infoid'])
        ret = get_push_el(self.driver,timeout=20)
        assert len(ret)==1
        #print ret
        open_notifications(self.driver)
        ret[0].click()
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',AUDIO_PAUSE) and self.driver.find_element_by_id(AUDIO_TITLE).text == AUDIO_ARTICLE_B
        back(self.driver)
        assert self.driver.current_activity == ACTIVITY.get('search')
        open_notifications(self.driver)
        assert self.driver.find_element_by_id(NOTIFICATION_AUDIO_TITLE).text == AUDIO_ARTICLE_B
        close_notification(self.driver)
        print u'Step %s:播放音频详情页时，收到音频详情页B推送并点击时，音频A立刻停止播放详情页音频B，返回时音频A播放器销毁，直接回到音频A的上一页面：OK' % (str(step))
        step+=1

        back(self.driver)
        clear_notification(self.driver)

        get_to_article_by_search(self.driver,NORMAL_AUDIO_ARTICLE,self.mode)
        sleep(WAIT_TIME)
        click_audio_in_webview(self.driver)
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',AUDIO_PAUSE)

        push_info = self.db.get_push_info_by_name(AUDIO_ARTICLE_B)

        self.jpush.push_article(push_info['model'],push_info['infoid'])
        ret = get_push_el(self.driver,timeout=20)
        assert len(ret)==1
        #print ret
        open_notifications(self.driver)
        ret[0].click()
        sleep(WAIT_TIME)

        back(self.driver)
        assert element_exsist(self.driver,'id',AUDIO_PAUSE) == False
        assert self.driver.current_activity == ACTIVITY.get(NORMAL_AUDIO_ARTICLE)
        open_notifications(self.driver)
        assert self.driver.find_element_by_id(NOTIFICATION_AUDIO_TITLE).text == AUDIO_ARTICLE_B
        close_notification(self.driver)
        print u'Step %s:播放文章页中的音频A时，收到其他音频详情页音频B推送，点击查看通知，音频A立刻停止播放详情页音频B，返回时文章页中的音频A播放器销毁，但文章页面正常显示：OK' % (str(step))
        step+=1
        return True

    def play_article_check(self):
        step = 1
        sleep(WAIT_TIME)
        go_to_settings(self.driver)
        sleep(WAIT_TIME)
        assert set_push_state(self.driver,'true')
        clear_notification(self.driver)

        self.driver.find_element_by_id(INFORMATION).click()

        get_to_article_by_search(self.driver,AUDIO_ARTICLE,self.mode)

        push_info = self.db.get_push_info_by_name(NORMAL_AUDIO_ARTICLE_B)

        self.jpush.push_article(push_info['model'],push_info['infoid'])
        ret = get_push_el(self.driver,timeout=20)
        assert len(ret)==1
        #print ret
        open_notifications(self.driver)
        ret[0].click()
        sleep(WAIT_TIME)
        open_notifications(self.driver)
        assert self.driver.find_element_by_id(NOTIFICATION_AUDIO_TITLE).text == AUDIO_ARTICLE
        close_notification(self.driver)
        sleep(WAIT_TIME)
        click_audio_in_webview(self.driver)

        back(self.driver)
        assert self.driver.current_activity == ACTIVITY.get('search')
        open_notifications(self.driver)
        assert self.driver.find_element_by_id(NOTIFICATION_AUDIO_TITLE).text == NORMAL_AUDIO_ARTICLE_B
        close_notification(self.driver)
        print u'Step %s:播放音频详情页音频A时，收到文章页中嵌入的音频B推送，点击查看通知时，音频A继续播放，点击播放音频B，音频A停止、播放音频B，返回时音频A播放器销毁，直接回到音频A的上一页面：OK' % (str(step))
        step+=1

        back(self.driver)
        clear_notification(self.driver)

        get_to_article_by_search(self.driver,NORMAL_AUDIO_ARTICLE,self.mode)
        sleep(WAIT_TIME)
        click_audio_in_webview(self.driver)
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,'id',AUDIO_PAUSE)

        push_info = self.db.get_push_info_by_name(NORMAL_AUDIO_ARTICLE_B)

        self.jpush.push_article(push_info['model'],push_info['infoid'])
        ret = get_push_el(self.driver,timeout=20)
        assert len(ret)==1
        #print ret
        open_notifications(self.driver)
        ret[0].click()
        sleep(WAIT_TIME)
        open_notifications(self.driver)
        assert self.driver.find_element_by_id(NOTIFICATION_AUDIO_TITLE).text == NORMAL_AUDIO_ARTICLE
        close_notification(self.driver)
        sleep(WAIT_TIME)
        click_audio_in_webview(self.driver)

        back(self.driver)
        assert element_exsist(self.driver,'id',AUDIO_PAUSE) == False
        assert self.driver.current_activity == ACTIVITY.get(NORMAL_AUDIO_ARTICLE)
        open_notifications(self.driver)
        assert self.driver.find_element_by_id(NOTIFICATION_AUDIO_TITLE).text == NORMAL_AUDIO_ARTICLE_B
        close_notification(self.driver)
        print u'Step %s:播放文章页中的音频A时，收到文章页中嵌入的音频B推送，点击查看通知时，音频A继续播放，点击播放音频B，音频A停止、播放音频B，返回时文章页中的音频A播放器销毁，但文章页面正常显示：OK' % (str(step))
        step+=1
        return True

    #excute TestCase
    def testAudio(self):
        self.case_id = get_case(__file__)
        self.result = self.audio_check(AUDIO_ARTICLE)

    #excute TestCase
    def testArticleAudio(self):
        self.case_id = get_case(__file__)
        self.result = self.article_audio_check(NORMAL_AUDIO_ARTICLE)

    def testPlayAudio(self):
        self.case_id = get_case(__file__)
        self.result = self.play_audio_check()

    def testPlayAudioArticle(self):
        self.case_id = get_case(__file__)
        self.result = self.play_article_check()

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

