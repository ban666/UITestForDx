# -*- coding: utf-8 -*-
__author__ = 'ld'

import sys
from appium import webdriver
from time import sleep
import unittest
from random import randint
sys.path.append('../../Lib')
import time
import os
from adb import *
from appium_lib import *
from dx_action import *
from ui_comment import *
from DbLib import DbLib
from config import *
from ui_clue import *
from ui_search import *
from screenshot import Appium_Extend

from elements_id import *

class SendNineImagesClueTest(unittest.TestCase):
    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.mode = MODE
        self.db = DbLib()
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        self.extend = Appium_Extend(self.driver)
        start_to_index(self.driver,self.mode)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def testSend9ImagesClue(self):
        """测试点：报料图片保存，发布九张图报料，报料搜索列表检查，报料详情页报料内容检查，我的报料报料内容检查"""
        BeLogin(self.driver)
        clean_image_save_dir()
        image_path = search_cLue_and_save_images(self.driver,self.extend)
        username = get_user_name(self.driver)
        # image_path = 'f:/pic/nine_clue_images.png'
        go_to_clue(self.driver)
        current_time = time.strftime( ISOTIMEFORMAT, time.localtime() )
        # current_date = '02-14'
        current_date = time.strftime(ISODAYFORMAT,time.localtime())
        content = 'test for sending clue with nine images '+str(current_time)
        # content = 'test for sending clue with nine images 2017-02-14 08:21:51'
        loc = u'湖北省武汉市武昌区东湖路靠近湖北日报传媒集团'
        print u"===================测试点1：发布九张图报料====================="
        send_txt_clue_with_image(self.driver,content,1)
        self.db.review_clue_by_content(content)
        print u"===================测试点2：校验列表九张图报料================="
        cluetestDic = {
            'content':content,
            'time' : current_date,
            'username' : username,
            'image_path' : image_path,
            'loc': loc,
            'image_nums': 9
        }
        self.driver.find_element_by_name(NEWSTABTXT).click()
        assert check_clue(self.driver,self.extend,cluetestDic,1)
        print u"===================测试点3：校验详情页报料内容================="
        self.driver.find_element_by_id(HEAD_CONTENT).click()
        assert check_clue_without_type(self.driver,self.extend,cluetestDic)
        self.driver.press_keycode(4)
        sleep(1)
        self.driver.press_keycode(4)
        print u"===================测试点4：校验我的报料中显示================="
        go_to_myclue(self.driver)
        sleep(WAIT_TIME)
        assert check_my_clue(self.driver,self.extend,self.db,cluetestDic,30)