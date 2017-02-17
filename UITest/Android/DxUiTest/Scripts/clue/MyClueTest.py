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

class MyClueTest(unittest.TestCase):

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

    def testNoPassClue(self):
        BeLogin(self.driver)
        username = get_user_name(self.driver)
        image_num = 2
        search_cLue_and_save_images(self.driver,self.extend,image_num)
        go_to_clue(self.driver)
        # current_time = '2017-02-15 09:31:42'
        current_time = time.strftime( ISOTIMEFORMAT, time.localtime() )
        current_date = time.strftime(ISODAYFORMAT,time.localtime())
        content = 'test for my clue not review ,wulala,wulalalala '+str(current_time)
        cluetestDic = {
            'image_num' : image_num,
            'image_path' : False,
            'content' : content,
            'time' : current_date,
            'loc' : False,
            'username' : username
        }
        send_txt_clue_with_image(self.driver,content,1,False,image_num)
        self.driver.find_element_by_name(NEWSTABTXT).click()
        go_to_myclue(self.driver)
        assert check_my_clue(self.driver,self.extend,self.db,cluetestDic,10)


    def testPassedClue(self):
        BeLogin(self.driver)
        username = get_user_name(self.driver)
        image_num = 2
        search_cLue_and_save_images(self.driver,self.extend,image_num)
        go_to_clue(self.driver)
        # current_time = '2017-02-15 09:31:42'
        current_time = time.strftime( ISOTIMEFORMAT, time.localtime() )
        current_date = time.strftime(ISODAYFORMAT,time.localtime())
        content = 'test for my clue passed ,wulala,wulalalala '+str(current_time)
        cluetestDic = {
            'image_num' : image_num,
            'image_path' : False,
            'content' : content,
            'time' : current_date,
            'loc' : False,
            'username' : username
        }
        send_txt_clue_with_image(self.driver,content,1,False,image_num)
        self.driver.find_element_by_name(NEWSTABTXT).click()
        self.db.review_clue_by_content(content)
        go_to_myclue(self.driver)
        slide_down(self.driver)
        sleep(WAIT_TIME)
        assert check_my_clue(self.driver,self.extend,self.db,cluetestDic,30)

    def testRefusedClue(self):
        BeLogin(self.driver)
        username = get_user_name(self.driver)
        image_num = 2
        search_cLue_and_save_images(self.driver,self.extend,image_num)
        go_to_clue(self.driver)
        # current_time = '2017-02-14 17:07:19'
        current_time = time.strftime( ISOTIMEFORMAT, time.localtime() )
        # current_date = '02-14'
        current_date = time.strftime(ISODAYFORMAT,time.localtime())
        content = 'test for my clue refused ,wulala,wulalalala '+str(current_time)
        cluetestDic = {
            'image_num' : image_num,
            'image_path' : False,
            'content' : content,
            'time' : current_date,
            'loc' : False,
            'username' : username
        }
        send_txt_clue_with_image(self.driver,content,0,False,image_num)
        self.driver.find_element_by_name(NEWSTABTXT).click()
        self.db.refused_clue_by_content(content,'这个是测试审核不通过的爆料',3)
        go_to_myclue(self.driver)
        sleep(WAIT_TIME)
        assert check_my_clue(self.driver,self.extend,self.db,cluetestDic,3)



