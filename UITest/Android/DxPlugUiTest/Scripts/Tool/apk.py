# -*- coding: utf-8 -*-
__author__ = 'liaoben'

import subprocess
import os
import threading
import sys
from appium import webdriver
import time
sys.path.append('../../Lib')
from adb import start_appium,stop_appium
# print ’popen3:’
def external_cmd(cmd, msg_in=''):
    try:
        proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,)
        stdout_value, stderr_value = proc.communicate(msg_in)
        return stdout_value, stderr_value
    except ValueError, err:
        # log("IOError: %s" % err)
        return None, None

# cmd1 = 'adb push g:/doc/pic/10.2M.jpg /sdcard/Pictures/'
# cmd2 = 'adb shell ls /sdcard/Pictures/'
# cmd3 = 'adb shell rm -rf /sdcard/Pictures/10.2M.jpg'
# print external_cmd(cmd1)
# print external_cmd(cmd2)
# print external_cmd(cmd3)
# print external_cmd(cmd2)

class ApkHandler(object):

    def __init__(self,ip):
        self.ip = ip

    def connect_phone(self):
        cmd = 'adb connect '+str(self.ip)
        ret = external_cmd(cmd)
        print self.ip+':',str(ret)+'\n'
        return ret

    def unistall_apk(self,package):
        cmd = 'adb -s '+str(self.ip)+':5555 '+'uninstall '+package
        ret = external_cmd(cmd)
        print self.ip+':',str(ret)+'\n'
        return ret

    def install_apk(self,package_path):
        cmd = 'adb -s '+str(self.ip)+':5555 '+'install '+ package_path
        ret = external_cmd(cmd)
        print self.ip+':',str(ret)+'\n'
        return ret

    def package_reset(self,package,package_path,unistall=True):
        self.connect_phone()
        if unistall:
            self.unistall_apk(package)
        self.install_apk(package_path)

def apk_install(ip_list,old_package,package_path):
        t = []
        for ip in ip_list:
            thread= threading.Thread(target=ApkHandler(ip).package_reset,args=(old_package,package_path,))
            t.append(thread)
        for j in t:
            j.start()
            j.join()


class TestLogin(object):

    def __init__(self,url):
        self.url = url

    def setUp(self):
        #self.testcases = conf.readcfg(__file__)
        self.desired_caps = {}
        self.desired_caps['platformName'] = 'Android'
        self.desired_caps['platformVersion'] = '4.4.2'
        self.desired_caps['deviceName'] = 'Nexus_7_2012_API_19'
        self.desired_caps['appPackage'] = 'com.cnhubei.dxxwhw'
        self.desired_caps['appActivity'] = 'com.cnhubei.dxxwhw.MainActivity'
        self.driver = webdriver.Remote(self.url, self.desired_caps)


    def tearDown(self):
        print 'test end...'
        try:
            self.driver.quit()
        except Exception as e:
            print 'tearDown:',e

    #excute TestCase
    def testFunc1(self):
        print self.driver.current_activity
        time.sleep(5)
        print 'test start'
        print self.driver.current_activity
        #change_network(self.driver,'wifi')
        #self.driver.find_element_by_id('com.cnhubei.dxxwhw:id/share_sina').click()

        box = self.driver.find_elements_by_class_name('android.widget.CheckBox')
        for i in box:
            i.click()
        self.driver.find_element_by_class_name('android.widget.Button').click()

        # sleep(2)
        # self.driver.find_element_by_id('com.cnhubei.dxxwhw:id/tv_news_normal_title').click()
        # self.driver.find_element_by_id('com.cnhubei.dxxwhw:id/ic_share').click()
        #
        # share = self.driver.find_elements_by_id('com.cnhubei.dxxwhw:id/umeng_socialize_shareboard_pltform_name')
        #
        # for i in share:
        #     print i.text

    def excute(self):
        self.setUp()
        self.testFunc1()
        self.tearDown()

if __name__ == '__main__':
    ip_list = ['192.168.1.116','192.168.1.115']
    # t = []
    package = 'com.cnhubei.dxxwhw'
    package_path = 'g:/downloads/938.apk'
    # for ip in ip_list:
    #     thread= threading.Thread(target=ApkHandler(ip).package_reset,args=(package,package_path,))
    #     t.append(thread)
    #
    # for j in t:
    #     j.start()
    #     #j.join()

    #apk_install(ip_list,package,package_path)
    host = '127.0.0.1'
    port = 4723
    bootstrap_port = 4724
    log_path = 'e:/appium_log'
    device_uid=[x+':5555' for x in ip_list]
    url_list = []
    stop_appium()
    for i in range(0,4,2):
        t_port = port+i
        t_bootstrap_port = port+i+1
        #url = threading.Thread(target =start_appium,args=(host, t_port, t_bootstrap_port, log_path,device_uid[i],))
        url = start_appium(host, t_port, t_bootstrap_port, log_path,device_uid[i/2])
        print url
        url_list.append(url[1])
        time.sleep(5)
        #url.start()
    thread_list = []
    for urls in url_list:
        print urls
        t = threading.Thread(target=TestLogin(urls).excute,args=())
        t.start()
