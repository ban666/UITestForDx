# -*- coding: utf-8 -*-
__author__ = 'ld'

import sys
from appium import webdriver
from time import sleep
import unittest
sys.path.append('../../Lib')
from appium_lib import *
import time
import os
from adb import *
from dx_action import *
from ui_comment import *
from ChnlRequest import ChnlRequest
from DbLib import DbLib
from config import *
from elements_id import *
from configrw import get_case
from TestlinkHandler import TestlinkHandler
from ui_clue import *
from BaoliaoRequest import BaoliaoRequest
from random import randint

class NinePicsNoAddButtonaTest(unittest.TestCase):

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
        self.api = ChnlRequest(MODE)
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        self.extend = Appium_Extend(self.driver)
        start_to_index(self.driver,self.mode)

    def tearDown(self):
        print 'Test End...................................'
        try:
            #self.tsl.set_tc_status(self.case_id,self.result,self.msg)
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def AddNinePicsTest(self):
        sleep(WAIT_TIME)
        #步骤：删除图片下载目录内容
        step = 1
        cmd = 'adb shell "rm sdcard/cnhubei/*"'
        os.popen(cmd)
        p = ls('sdcard/cnhubei')
        count = p.count("\n")
        if count == 2:
            print u'step %s,SUCCES!!!---------->清空图片下载文件夹cnhubei目录成功' % (str(step))
        else:
            print u'step %s,FAIL!!!--------->清空图片下载文件夹cnhubei目录失败' % (str(step))
        step += 1
        #步骤：搜索9张图报料并进行下载
        go_to_clue(self.driver)
        self.driver.find_element_by_id(CLUE_SEARCH).click()
        self.driver.find_element_by_id(CLUE_SEARCH_EDIT).send_keys(CLUE_NINE_PIC)
        sleep(WAIT_TIME)
        self.driver.press_keycode(66)
        sleep(WAIT_TIME)
        # """
        # 将搜索的9张图图片列表进行保存，用于发布爆料后对比
        # """
        Image_element_1 = self.driver.find_element_by_id(CLUE_LIST_PIC)
        self.extend.get_screenshot_by_element(Image_element_1).write_to_file(PIC_SAVE_PATH, "send_9_images_test")
        self.assertTrue(os.path.isfile(PIC_SAVE_PATH+"/send_9_images_test.png"))
        for i in range (2,11,1):
            self.driver.find_elements_by_class_name(CLUE_LIST_PIC_CLASS)[i].click()
            self.driver.find_element_by_id(CLUE_IMAGE_DOWNLOAD_BUTTON).click()
            self.driver.press_keycode(4)
        self.driver.find_element_by_class_name(BACK_BUTTON_CLASS).click()
        self.driver.press_keycode(4)
        p = ls('sdcard/cnhubei')
        count = p.count("\n")
        if count == 11:
            print u'step %s,SUCCES!!!---------->下载九张图片成功' % (str(step))
        else:
            print u'step %s,FAIL!!!--------->下载九张图片失败' % (str(step))
            return False

        step += 1
        #步骤：进入发布报料界面添加9张图片并判断是否仍有图片添加按钮
        self.driver.find_element_by_id(SEND_CLUE_BUTTON).click()
        self.driver.find_elements_by_id(SEND_CLUE_PIC)[-1].click()
        self.driver.find_element_by_id(IMAGE_ALL).click()
        trynum = 0
        while trynum < 4:
            find_cnhubei = element_exsist(self.driver,'name',IMAGE_SAVE_DIR)
            if find_cnhubei:
                break
            else:
                slide_up(self.driver,5,2)
                trynum += 1
        self.driver.find_element_by_name(IMAGE_SAVE_DIR).click()
        for pic in range (8,-1,-1):
            self.driver.find_elements_by_id(SEND_CLUE_CHECK_MARK)[pic].click()
        self.driver.find_element_by_id(SEND_CLUE_PIC_CONFIRM).click()
        imageviews = self.driver.find_element_by_id(SEND_CLUE_IMAGE_LIST_VIEW).find_elements_by_id(SEND_CLUE_IMAGE_ADD)
        if len(imageviews) == 9:
            print u'step %s,SUCCES!!!---------->添加九张图片后不会再显示第十个图片添加按钮' % (str(step))
            self.tsl.set_tc_status(self.case_id[0],True,self.msg)
        else:
            print u'step %s,FAIL!!!---------->添加九张图片后图片添加按钮显示错误' % (str(step))
            self.tsl.set_tc_status(self.case_id[0],False,self.msg)
            return False
        # Image_element_1 = self.driver.find_element_by_id(SEND_CLUE_IMAGE)
        # self.extend.get_screenshot_by_element(Image_element_1).write_to_file(PIC_SAVE_PATH, "send_9_images_test")
        step+=1
        #loc = u'东湖路181'
        current_time = time.strftime( ISOTIMEFORMAT, time.localtime() )
        content = 'test for sending clue with nine images '+str(current_time)
        sleep(WAIT_TIME)
        send_txt_clue(self.driver,0,content)
        infoid = self.db.get_clueid_with_content_by_db(content)
        self.db.change_article_state_by_db(infoid,30)
        self.driver.find_element_by_id(SUBTYPE+str(0+1)).click()
        self.driver.find_element_by_id(CLUE_SEARCH).click()
        self.driver.find_element_by_id(CLUE_SEARCH_EDIT).send_keys(content)
        self.driver.press_keycode(66)
        sleep(WAIT_TIME)
        #发布报料是否成功
        image_element_2 = self.driver.find_element_by_id(CLUE_LIST_PIC)
        self.extend.get_screenshot_by_element(image_element_2).write_to_file(PIC_SAVE_PATH, "sended_9_images_test")
        #load = self.extend.load_image(PIC_SAVE_PATH+"\send_9_images_test.png")
        result = self.extend.same_as(PIC_SAVE_PATH+"/send_9_images_test.png",PIC_SAVE_PATH+"/sended_9_images_test.png",10)
        if result:
            print u'step %s,SUCCES!!!---------->发布九张图片成功，顺序正确' % (str(step))
            self.tsl.set_tc_status(self.case_id[1],result,self.msg)
            return result
        else:
            print u'step %s,FAIL!!!---------->发布九张图片后图片校验失败失败！' % (str(step))
            self.tsl.set_tc_status(self.case_id[1],result,self.msg)
            return result

    def testSendNinePics(self):
        self.case_id = get_case(__file__)
        if not is_login(self.driver):
            phone_number = '134'+str(randint(10000000,99999999))
            login_to_index(self.driver,MODE,desired_caps['appPackage'],phone_number)
        self.AddNinePicsTest()
