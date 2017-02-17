# -*- coding: utf-8 -*-
__author__ = 'ld'

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
from DbLib import DbLib
from config import *
from ui_clue import *
from ui_search import *
from screenshot import Appium_Extend

from elements_id import *

class NotLoginSendClueTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.mode = MODE
        self.db = DbLib()
        #self.api = ChnlRequest(self.mode)
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        self.extend = Appium_Extend(self.driver)
        start_to_index(self.driver,self.mode)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def NotLoginSendClueLocation(self):
        sleep(WAIT_TIME)
        '''
        # step 1：登录状态判断，已登录则退出登录
        '''
        login_state = is_login(self.driver)
        count = 0
        while login_state and count < 5:
            logout_to_index(self.driver,self.mode)
            count += 1
            login_state = is_login(self.driver)
            self.assertFalse(login_state)
        go_to_clue(self.driver)
        self.driver.find_element_by_id(CLUE_PUBLISH).click()
        '''
        step 2：判断未登录时点击是否跳转登录界面
        '''
        top_bar = self.driver.find_element_by_id(TOP_BAR).get_attribute("text")
        if top_bar == LOGIN_TOP_TITLE:
            print u"SUCCESS!!!--------->跳转到登录界面"
        else:
            print u"FAIL!!!------->未跳转到登录界面"
            return False
        '''
        step 3：输入手机号进行登录
        '''

        phone_number = '134'+str(randint(10000000,99999999))
        print phone_number
        loginresult = login(self.driver,self.mode,self.desired_caps['appPackage'],phone_number,in_page = True)
        if loginresult:
            print u'SUCCESS!!!---------->登录成功'
        else:
            print u'FAIL!!!------------->登录失败'
            return False
        sleep(WAIT_TIME)
        '''
        step 4：跳转回报料界面
        '''
        locationresult = element_exsist(self.driver,'id',CLUE_PUBLISH)
        if locationresult:
            print u'SUCCESS!!!---------->登录后成功跳转到报料列表'
        else:
            print u'FAIL!!!------------》登录后跳转到报料列表失败'

    def SendTxtClue(self,subtype,location = False):
        '''
        step 1：发布纯文字报料默认地理位置并审核通过
        '''
        if subtype:
            type = ' woxiu'
        else:
            type = ' baoliao'
        current_time = time.strftime(ISOTIMEFORMAT, time.localtime())
        content = 'test for sending hubei news clue with nine images '+str(current_time)+type
        send_txt_clue(self.driver,content,subtype,location,in_page = False)
        self.db.review_clue_by_content(content)
        assert element_exsist(self.driver,'id',CLUE_PUBLISH)
        return content

    def testNotLoginSendClue(self):
        """未登录发布报料，跳转登录后，发布一个我秀，并搜索检查"""
        self.NotLoginSendClueLocation()
        current_date = time.strftime(ISODAYFORMAT,time.localtime())
        go_to_clue(self.driver)
        sendclueresult = self.SendTxtClue(subtype = 1,location = False)
        #sendclueresult = '15:31'
        self.driver.find_element_by_name(NEWSTABTXT).click()
        username = get_user_name(self.driver)
        cluetestDic = {
            'content' : sendclueresult,
            'loc' :  False,
            'image_path' : False,
            'time' : current_date,
            'username': username
        }
        if sendclueresult:
            return check_clue(self.driver,self.extend,cluetestDic,1)
        else:
            return False

    def testSendBaoliaoClue(self):
        """发布一个报料并修改地理位置"""
        BeLogin(self.driver)
        current_date = time.strftime(ISODAYFORMAT,time.localtime())
        go_to_clue(self.driver)
        sendclueresult = self.SendTxtClue(0,testloc)
        # sendclueresult = '16:56:40'
        self.driver.find_element_by_name(NEWSTABTXT).click()
        username = get_user_name(self.driver)
        cluetestDic = {
            'content' : sendclueresult,
            'loc' :  '湖北提包测试地理位置',
            'image_path' : False,
            'time' : current_date,
            'username' : username,
            'image_num' : 0
        }
        if sendclueresult:
            return check_clue(self.driver,self.extend,cluetestDic,0)
        else:
            return False
