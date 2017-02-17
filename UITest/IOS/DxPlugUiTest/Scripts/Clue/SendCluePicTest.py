# -*- coding: utf-8 -*-
__author__ = 'liaoben'

import sys
from appium import webdriver
from time import sleep
import unittest
from random import randint
sys.path.append('../../Lib')
import time
import os
from appium_lib import *
from dx_action import *
from ui_comment import *
from ChnlRequest import ChnlRequest
from DbLib import DbLib
from config import *
from loglib import log
from elements_id import *
from configrw import get_case
from TestlinkHandler import TestlinkHandler
from ui_clue import *
from adb import get_config_by_adb,download_and_install,push_picture
from BaoliaoRequest import BaoliaoRequest
from uuid import uuid4
from common import *

class SubTypeTest(unittest.TestCase):

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = desired_caps
        print 'Test Start...................................'
        self.result = 'f'
        self.msg = ''
        self.tsl = TestlinkHandler()
        self.mode = MODE
        self.clue = BaoliaoRequest()
        self.db = DbLib()
        download_and_install()
        self.driver = webdriver.Remote(APPIUM_URL, self.desired_caps)
        start_to_index(self.driver,self.mode)
        if not is_login(self.desired_caps['appPackage']):
            login_to_index(self.driver,TEST_PHONE)

    def tearDown(self):
        print 'Test End...................................'
        try:
            self.tsl.set_tc_status(self.case_id,self.result,self.msg)
            self.driver.quit()
        except Exception as e:
            print u'测试失败，失败环节:tear down',e

    def common_check(self,pic,expect,msg):
        step = 1
        #TODO
        #图片地址配置
        #服务器地址配置
        #图片下载配置
        path = '/sdcard/Pictures/1.jpg'
        push = IMAGE_PATH+'/'+IMAGES.get(pic)
        push_picture(push,path)
        h_old,w_old,size_old = get_image_info(push,'B')

        go_to_clue(self.driver)
        #dc = get_config_by_adb()['dc']
        self.driver.find_element_by_id(SEND_CLUE_BUTTON).click()
        content = pic+str(uuid4())
        assert send_txt_clue(self.driver,1,content,pic='true')
        assert element_exsist(self.driver,'id',CLUE_LIST_MY_CLUE_ENTRY)
        sleep(WAIT_TIME)

        pic_path = self.db.get_clue_pic_info_by_db(content)

        #download pic
        fname = IMAGE_PATH + '/'+'temp.jpg'
        download_image_by_ssh(pic_path,fname)
        #analysis pic
        h,w,size = get_image_info(fname,'B')
        print h_old,w_old,size_old
        print h,w,size
        os.remove(fname)
        assert w == expect[0] and h == expect[1] and eval(str(size)+expect[2]+str(size_old))
        print u'Step %s:%s：OK' % (str(step),msg)
        step+=1
        return True



    #excute TestCase
    def test(self):
        self.case_id = get_case(__file__)
        expect = [960,10000,'<']
        pic = '960_10000'
        msg = u'当图片长宽等于标准值时，质量压缩直接上传尺寸不变'
        self.result = self.common_check(pic,expect,msg)

    def test2(self):
        self.case_id = get_case(__file__)
        expect = [950,3953,'<']
        pic = '950_3953'
        msg = u'当图片长短边比r小于标准值R，并且短边小于MIN时'
        self.result = self.common_check(pic,expect,msg)

    def test3(self):
        self.case_id = get_case(__file__)
        expect = [2160,960,'<']
        pic = '10630_4724'
        msg = u'当图片长短边比r小于标准值R，并且短边大于MIN时'
        self.result = self.common_check(pic,expect,msg)

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

