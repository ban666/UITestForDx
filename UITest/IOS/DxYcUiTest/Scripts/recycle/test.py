# -*- coding: utf-8 -*-
__author__ = 'liaoben'

from appium import webdriver
import time
import sys
sys.path.append('../../Lib')
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from config import *
from appium_lib import *
from elements_id import *

class ToastTests(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['automationName'] = 'Uiautomator2'
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '5.1.1'
        desired_caps['deviceName'] = 'Android Emulator'
        desired_caps['appPackage'] = 'com.cnhubei.ycdx'
        desired_caps['appActivity'] = 'com.cnhubei.home.module.splash.A_SplashActivity'
        desired_caps['resetKeyboard'] = 'true'
        desired_caps['unicodeKeyboard'] = 'true'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def tearDown(self):
        self.driver.quit()

    def _find_toast(self,message,timeout,poll_frequency,driver):
        message = '//*[@text=\'{}\']'.format(message)
        element = WebDriverWait(driver,timeout,poll_frequency).until(expected_conditions.presence_of_element_located((By.XPATH,message)))
        print element

    def test_toast(self):
        print self.driver.get_window_size()
        sleep(10)
        get_to_article_by_search(self.driver,NORMAL_ARTICLE,'')
        sleep(8)
        # time.sleep(2)
        print self.driver.page_source
        self._find_toast(u'小号自体',10,0.5,self.driver)
        time.sleep(10)
        self.driver.find_element_by_id('showToastButton').click()
        self._find_toast('Hello selendroid toast!',10,0.5,self.driver)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ToastTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
