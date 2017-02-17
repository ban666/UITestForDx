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

class ClueDealWithImageTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.db = DbLib()
        self.mode = MODE
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        self.extend = Appium_Extend(self.driver)
        start_to_index(self.driver,self.mode)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def go_to_send_clue(self):
        go_to_clue(self.driver)
        self.driver.find_element_by_id(CLUE_PUBLISH).click()

    def delete_image_check(self):
        result = True
        images_0 = self.driver.find_element_by_id(CLUE_CONTENT_INPUT_BOX).find_elements_by_id(CLUE_SELECTED_IMAGES)
        images_0[0].click()
        delete_image_in_clue(self.driver)
        back(self.driver)
        sleep(2)
        images = self.driver.find_element_by_id(CLUE_CONTENT_INPUT_BOX).find_elements_by_id(CLUE_SELECTED_IMAGES)
        imagenum = len(images)-1
        if len(images) == len(images_0)-1:
            print u'删除1张图后发报料界面显示正确'
        else:
            print u'Fail!!!------------》删除1张图后发报料界面显示错误'
            result = False
        images[0].click()
        while imagenum > 0 :
            if self.driver.find_element_by_id(CLUE_IMAGE_TITLE).text != '1/'+str(imagenum):
                result = False
                print u'FAIL!!!-------------------》图片序列显示错误'
            delete_image_in_clue(self.driver)
            imagenum -= 1
            sleep(1)
        try:
            self.driver.find_element_by_id(CLUE_CONTENT_INPUT_BOX).find_element_by_id(CLUE_SELECTED_IMAGES)
            print u'FAIL!!!------------------------------->图片没有全部被删除'
            result = False
        except NoSuchContextException:
            print u'1图片全部被删除'
        except Exception:
            print u'2图片全部被删除'
        return result

    def slide_image_check(self):
        result = True
        images = self.driver.find_element_by_id(CLUE_CONTENT_INPUT_BOX).find_elements_by_id(CLUE_SELECTED_IMAGES)
        image_num = len(images)-1
        images[0].click()
        for i in range(1,len(images),1):
            if self.driver.find_element_by_id(CLUE_IMAGE_TITLE).text != str(i)+'/'+str(image_num):
                result = False
                print u'FAIL!!!---------------------------》左划后图片序列显示错误'
                print self.driver.find_element_by_id(CLUE_IMAGE_TITLE).text
                print str(i)+' / '+str(image_num)
                break
            if i < image_num:
                slide_left(self.driver,3.8)
        for j in range(image_num,0,-1):
            if self.driver.find_element_by_id(CLUE_IMAGE_TITLE).text != str(j)+'/'+str(image_num):
                result = False
                print u'FAIL!!!----------------------------》右划后图片序列显示错误'
                break
            if j > 1:
                slide_right(self.driver)
        if result:
            print u'图片左划右划测试通过'
        return result

    def is_image_show(self):
        if element_exsist(self.driver,'id',CLUE_IMAGE_TITLE) \
                and element_exsist(self.driver,'id',CLUE_IMAGE_DELETE) \
                and element_exsist(self.driver,'id',SEND_CLUE_IMAGE_VIEW_BACK):
            print u'图片其他元素都显示'
            return True
        else:
            if not element_exsist(self.driver,'id',CLUE_IMAGE_TITLE) \
                    and not element_exsist(self.driver,'id',CLUE_IMAGE_DELETE) \
                    and not element_exsist(self.driver,'id',SEND_CLUE_IMAGE_VIEW_BACK):
                print u"图片其他元素都不显示"
                return False

    def click_image_check(self):
        if self.is_image_show():
            tap_center(self.driver)
            sleep(3)
            if not self.is_image_show():
                return True
            else:
                return False
        else:
            tap_center(self.driver)
            sleep(3)
            if self.is_image_show():
                return True
            else:
                return False

    def check_image_back_button(self):
        is_show_back = element_exsist(self.driver,'id',SEND_CLUE_IMAGE_VIEW_BACK)
        if not is_show_back:
            tap_center(self.driver)
            sleep(3)
        self.driver.find_element_by_id(SEND_CLUE_IMAGE_VIEW_BACK).click()
        result =  element_exsist(self.driver,'id',PV_IMAGE)
        if not result:
            print u'点击返回测试通过'
            return True
        else:
            print u'FAIL!!!------------------------》点击返回测试失败'
            return False

    def go_to_send_image(self,image_num):
        BeLogin(self.driver)
        # search_cLue_and_save_images(self.driver,self.extend,image_num)
        self.go_to_send_clue()
        add_images_in_clue(self.driver,image_num)

    def testImageDeleteInSendPage(self):
        self.go_to_send_image(image_num = 4)
        assert self.delete_image_check()

    def testImageViewInSendPage(self):
        self.go_to_send_image(image_num = 4)
        result = True
        if not self.slide_image_check():
            result = False
        if not self.click_image_check():
            result = False
            print result
        if not self.check_image_back_button():
            result = False
        assert result


