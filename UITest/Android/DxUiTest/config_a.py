#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: liaoben
__author__ = 'liaoben'

import os
import time

basdir = os.path.abspath(os.path.dirname(__file__))

class ConfigA(object):

    def __init__(self):
        self.log_file = basdir+'\\Log\\Log_'+time.strftime("%Y%m%d%H%M%S", time.localtime())+'.log'
        self.report_file =basdir+'\\Report\\Report.xlsx'
        self.test_level = ['level 1','level 2','level 3','level 4','level 5']
        self.username = 'zzh'
        self.password = '123456'
        self.sn = '01379426'
        self.desired_caps = {}
        self.desired_caps['platformName'] = 'Android'
        self.desired_caps['platformVersion'] = '4.4.2'
        self.desired_caps['deviceName'] = 'Nexus_7_2012_API_19'
        self.desired_caps['appPackage'] = 'com.cnhubei.dxxwhw'
        self.desired_caps['appActivity'] = '.MainActivity'
        PATH=lambda p:os.path.abspath(
        os.path.join(os.path.dirname(__file__),p)
        )
        #self.desired_caps['app'] = PATH('C:\\Users\\Administrator\\Desktop\\Janlinker.apk')#被测试的App在电脑上的位置

    def gen_file(self,fn):
        if not os.path.exists(fn):
            with open(fn,'w+') as f:
                pass

    def init_case(self):
        self.gen_file(self.log_file)
        self.gen_file(self.report_file)

