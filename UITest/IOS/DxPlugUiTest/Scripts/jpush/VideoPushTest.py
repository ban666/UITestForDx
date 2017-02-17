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

        push_info = self.db.get_push_info_by_name(article)

        self.jpush.push_article(push_info['model'],push_info['infoid'])
        ret = confirm_push(self.driver,timeout=20)
        assert ret
        for i in range(20):
            if not self.driver.find_element(*VIDEO_CLOSE).is_displayed():
                self.driver.find_element(*VIDEO_ITEM).click()
                sleep(1)
            if self.driver.find_element(*VIDEO_CLOSE).is_displayed() and not \
                self.driver.find_element(*VIDEO_PROGRESS).is_displayed():
                print u'Step %s:推送直播类型视频，客户端以直播类型播放测试：OK' % (str(step))
                step+=1
                return True
        return False

    def video_check(self,article):
        step = 1
        sleep(WAIT_TIME)

        push_info = self.db.get_push_info_by_name(article)

        self.jpush.push_article(push_info['model'],push_info['infoid'])
        ret = confirm_push(self.driver,timeout=20)
        assert ret
        for i in range(20):
            if not self.driver.find_element(*VIDEO_CLOSE).is_displayed():
                self.driver.find_element(*VIDEO_ITEM).click()
            if self.driver.find_element(*VIDEO_PROGRESS).is_displayed():
                print u'Step %s:推送非直播类型视频，客户端以非直播类型播放测试：OK' % (str(step))
                step+=1
                return True
        return False

    def play_video_check(self):
        step = 1
        sleep(WAIT_TIME)

        get_to_article_by_search(self.driver,VIDEO_ARTICLE,self.mode)

        push_info = self.db.get_push_info_by_name(VIDEO_ARTICLE_B)

        self.jpush.push_article(push_info['model'],push_info['infoid'])
        ret = confirm_push(self.driver,timeout=20)
        assert ret
        #print ret
        assert element_exsist(self.driver,*VIDEO_FULL_SCREEN) and self.driver.find_element(*VIDEO_TITLE_PLAYING).text == VIDEO_ARTICLE_B
        back(self.driver)
        sleep(WAIT_TIME)
        assert self.driver.find_element(*VIDEO_TITLE_PLAY_BEFORE).text == VIDEO_ARTICLE and element_exsist(self.driver,*VIDEO_FULL_SCREEN) == False
        print u'Step %s:播放视频详情页视频A时，收到其他视频详情页视频B推送，点击查看通知，视频A立刻停止、播放视频B，返回时视频A停止播放，但视频详情页显示正常：OK' % (str(step))
        step+=1

        search_article_to_index(self.driver)

        get_to_article_by_search(self.driver,NORMAL_VIDEO_ARTICLE,self.mode)
        sleep(WAIT_TIME)
        click_audio_in_webview(self.driver)
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,*VIDEO_FULL_SCREEN)

        push_info = self.db.get_push_info_by_name(VIDEO_ARTICLE_B)

        self.jpush.push_article(push_info['model'],push_info['infoid'])
        ret = confirm_push(self.driver,timeout=20)
        assert ret
        #print ret
        assert element_exsist(self.driver,*VIDEO_FULL_SCREEN) and self.driver.find_element(*VIDEO_TITLE_PLAYING).text == VIDEO_ARTICLE_B
        back(self.driver)
        assert element_exsist(self.driver,*VIDEO_FULL_SCREEN) == False and element_exsist(self.driver,'class','UIAWebView')
        print u'Step %s:播放文章页中的视频A时，收到其他视频详情页视频B推送，点击查看通知，视频A立刻停止、播放视频B，返回时文章页中的视频A播放器销毁，但文章页面正常显示。：OK' % (str(step))
        step+=1
        return True

    def play_article_check(self):
        step = 1
        sleep(WAIT_TIME)

        get_to_article_by_search(self.driver,VIDEO_ARTICLE,self.mode)

        push_info = self.db.get_push_info_by_name(NORMAL_VIDEO_ARTICLE_B)

        self.jpush.push_article(push_info['model'],push_info['infoid'])
        ret = confirm_push(self.driver,timeout=20)
        assert ret
        #print ret
        click_audio_in_webview(self.driver)
        assert element_exsist(self.driver,*VIDEO_FULL_SCREEN)

        back(self.driver)
        assert self.driver.find_element(*VIDEO_TITLE_PLAY_BEFORE).text == VIDEO_ARTICLE and element_exsist(self.driver,*VIDEO_FULL_SCREEN) == False
        play_video(self.driver)
        assert element_exsist(self.driver,*VIDEO_FULL_SCREEN)
        print u'Step %s:播放视频详情页视频A时，收到文章页中嵌入的视频B推送，点击查看通知时视频A停止播放，点击播放视频B，视频B正确播放，返回时视频A播放器销毁，视频详情页页面仍存在，手动点击可重新播放视频A：OK' % (str(step))
        step+=1

        search_article_to_index(self.driver)

        get_to_article_by_search(self.driver,NORMAL_VIDEO_ARTICLE,self.mode)
        sleep(WAIT_TIME)
        click_audio_in_webview(self.driver)
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,*VIDEO_FULL_SCREEN)

        push_info = self.db.get_push_info_by_name(NORMAL_VIDEO_ARTICLE_B)

        self.jpush.push_article(push_info['model'],push_info['infoid'])
        ret = confirm_push(self.driver,timeout=20)
        assert ret
        click_audio_in_webview(self.driver)
        #print ret
        assert element_exsist(self.driver,*VIDEO_FULL_SCREEN)
        back(self.driver)
        assert element_exsist(self.driver,*VIDEO_FULL_SCREEN) == False and element_exsist(self.driver,'class','UIAWebView')
        print u'Step %s:播放文章页中的视频A时，收到文章页中嵌入的视频B推送，点击查看通知时视频A停止播放，点击播放视频B，视频B正确播放，返回时文章页中的视频A播放器销毁，但文章页面正常显示：OK' % (str(step))
        step+=1
        return True

    def play_video_audio_check(self):
        step = 1
        sleep(WAIT_TIME)

        get_to_article_by_search(self.driver,VIDEO_ARTICLE,self.mode)

        push_info = self.db.get_push_info_by_name(AUDIO_ARTICLE)

        self.jpush.push_article(push_info['model'],push_info['infoid'])
        ret = confirm_push(self.driver,timeout=20)
        assert ret
        #print ret
        assert element_exsist(self.driver,*AUDIO_PAUSE) and self.driver.find_element(*AUDIO_TITLE).text == AUDIO_ARTICLE
        back(self.driver)
        sleep(WAIT_TIME)
        assert self.driver.find_element(*VIDEO_TITLE_PLAY_BEFORE).text == VIDEO_ARTICLE and element_exsist(self.driver,*VIDEO_FULL_SCREEN) == False
        assert self.driver.find_element(*TOP_NOTIFICATION).text == u'正在播放:'+AUDIO_ARTICLE
        play_video(self.driver)
        assert element_exsist(self.driver,*VIDEO_FULL_SCREEN)
        assert element_exsist(self.driver,*TOP_NOTIFICATION) == False
        print u'Step %s:播放视频详情页视频时，收到音频详情页音频推送，点击查看通知，视频立刻停止、播放音频，返回时视频播放器销毁，视频详情页面仍存在，可手动点击重新播放视频，此时音频播放器销毁：OK' % (str(step))
        step+=1

        search_article_to_index(self.driver)

        get_to_article_by_search(self.driver,NORMAL_VIDEO_ARTICLE,self.mode)
        sleep(WAIT_TIME)
        click_audio_in_webview(self.driver)
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,*VIDEO_FULL_SCREEN)

        push_info = self.db.get_push_info_by_name(AUDIO_ARTICLE)

        self.jpush.push_article(push_info['model'],push_info['infoid'])
        ret = confirm_push(self.driver,timeout=20)
        assert ret
        #print ret
        assert element_exsist(self.driver,*AUDIO_PAUSE) and self.driver.find_element(*AUDIO_TITLE).text == AUDIO_ARTICLE
        back(self.driver)
        assert element_exsist(self.driver,*VIDEO_FULL_SCREEN) == False and element_exsist(self.driver,'class','UIAWebView')
        print u'Step %s:播放文章页中的视频时，收到音频详情页音频推送，点击查看通知，视频立刻停止、播放音频，返回时文章页中的视频播放器销毁，但文章页面正常显示：OK' % (str(step))
        step+=1
        return True

    def play_video_audio_article_check(self):
        step = 1
        sleep(WAIT_TIME)

        get_to_article_by_search(self.driver,VIDEO_ARTICLE,self.mode)

        push_info = self.db.get_push_info_by_name(NORMAL_AUDIO_ARTICLE)

        self.jpush.push_article(push_info['model'],push_info['infoid'])
        ret = confirm_push(self.driver,timeout=20)
        assert ret
        #print ret
        click_audio_in_webview(self.driver)
        assert element_exsist(self.driver,*AUDIO_PAUSE_IN_ARTICLE)

        back(self.driver)
        assert self.driver.find_element(*VIDEO_TITLE_PLAY_BEFORE).text == VIDEO_ARTICLE and element_exsist(self.driver,*VIDEO_FULL_SCREEN) == False
        assert self.driver.find_element(*TOP_NOTIFICATION).text == u'正在播放:'+NORMAL_AUDIO_ARTICLE
        play_video(self.driver)
        assert element_exsist(self.driver,*VIDEO_FULL_SCREEN)
        assert element_exsist(self.driver,*TOP_NOTIFICATION) == False
        print u'Step %s:播放视频详情页视频时，收到文章页中嵌入的音频推送，点击查看通知时视频停止播放，点击播放音频，音频正确播放，返回时视频播放器销毁，视频详情页页面仍存在，手动点击可重新播放视频，音频播放器销毁A：OK' % (str(step))
        step+=1

        search_article_to_index(self.driver)

        get_to_article_by_search(self.driver,NORMAL_VIDEO_ARTICLE,self.mode)
        sleep(WAIT_TIME)
        click_audio_in_webview(self.driver)
        sleep(WAIT_TIME)
        assert element_exsist(self.driver,*VIDEO_FULL_SCREEN)

        push_info = self.db.get_push_info_by_name(NORMAL_AUDIO_ARTICLE)

        self.jpush.push_article(push_info['model'],push_info['infoid'])
        ret = confirm_push(self.driver,timeout=20)
        assert ret
        click_audio_in_webview(self.driver)
        #print ret
        assert element_exsist(self.driver,*AUDIO_PAUSE_IN_ARTICLE)
        back(self.driver)
        assert element_exsist(self.driver,*VIDEO_FULL_SCREEN) == False and element_exsist(self.driver,'class','UIAWebView')
        print u'Step %s:播放文章页中的视频时，收到文章页中嵌入的音频推送，点击查看通知时视频停止播放，点击播放音频，音频正确播放，返回时文章页中的视频播放器销毁，但文章页面正常显示：OK' % (str(step))
        step+=1
        return True

    #excute TestCase
    def testLive(self):
        self.case_id = get_case(__file__)
        self.result = self.live_video_check(LIVE_VIDEO_ARTICLE)

    def testVideo(self):
        self.case_id = get_case(__file__)
        self.result = self.video_check(VIDEO_ARTICLE)

    def testPlayVideo(self):
        #2-4059
        self.case_id = get_case(__file__)
        self.result = self.play_video_check()

    def testPlayVideoArticle(self):
        #2-4060
        self.case_id = get_case(__file__)
        self.result = self.play_article_check()

    def testPlayVideoWithAudioPush(self):
        #2-4061
        self.case_id = get_case(__file__)
        self.result = self.play_video_audio_check()

    def testPlayVideoWithAudioArticlePush(self):
        #2-4062
        self.case_id = get_case(__file__)
        self.result = self.play_video_audio_article_check()
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

