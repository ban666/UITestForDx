# -*- coding: utf-8 -*-
__author__ = 'liaoben'

from adb import get_android_version

class WebviewHandler:

    def __init__(self,driver):
        self.version = ''
        self.driver = driver
        #self.android_version = get_android_version()

    def switch_to_webview(self):
        self.driver.switch_to.context(self.driver.contexts[-1])

    def switch_to_native(self):
        self.driver.switch_to.context(self.driver.contexts[0])

    def get_content_in_webview_plan_b(self):
        try:
            self.switch_to_webview()
            text = self.driver.find_element_by_accessibility_id('content').text
            self.switch_to_native()
            return [text]
        except:
            return False

    def get_content_in_webview_plan_a(self):
        try:
            texts = self.driver.find_elements_by_class_name('android.view.View')
            #print texts
            texts = [x.get_attribute('name') for x in texts]
            return texts
        except:
            return False

    def get_content_in_webview(self):
        ret_a = self.get_content_in_webview_plan_a()
        if ret_a != False:
            return ret_a
        return  self.get_content_in_webview_plan_b()