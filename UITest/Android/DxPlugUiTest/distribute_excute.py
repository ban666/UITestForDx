#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: liaoben
__author__ = 'liaoben'

import subprocess
import unittest
import os
import re
import sys
import time
from time import sleep
from Lib.config import *
from Lib.adb import *
import HTMLTestRunner
from Lib.appium_lib import get_appium_url_from_config
# print ’popen3:’
def make_test_suite(suite):
      base_path = os.path.abspath(os.path.dirname(sys.argv[0]))
      lib_path = base_path +'/Lib'
      path = base_path + '/Scripts/'+suite
      #print path
      sys.path.append(path)
      sys.path.append(lib_path)
      files = os.listdir(path)
      #print files
      test = re.compile('Test\.py$', re.IGNORECASE)
      files = filter(test.search, files)
      print files
      filenameToModuleName = lambda f: os.path.splitext(f)[0]
      moduleNames = map(filenameToModuleName, files)
      modules = map(__import__, moduleNames)
      load = unittest.defaultTestLoader.loadTestsFromModule
      return unittest.TestSuite(map(load, modules))

def test_multy_suite(suites):
        t = unittest.TestSuite()
        for suite in suites:
            t.addTest(make_test_suite(suite))
        return t

def get_time():
    return time.strftime("%Y%m%d%H%M%S", time.localtime())

def gen_config(url,config=DISTRIBUTE_CONFIG_PATH):
    from random import randint
    now =get_time()
    tid = os.getpid()
    print 'current',tid
    fname = now+str(randint(0,10000))+'.txt'
    fname = BASE_DIR+'/Config/'+fname
    with open(config,'a+') as f:
        f.write(url+','+str(tid)+'\n')
        f.flush()


class Distribute:

    def __init__(self,url,index,distribute_config=DISTRIBUTE_CONFIG_PATH):
        self.url = url
        self.config = distribute_config
        #gen_config(self.url)
        self.index = index


    def gen_cfg(self):
        from random import randint
        now =get_time()
        tid = sys._getframe().f_locals['self']
        print tid
        fname = now+str(randint(0,10000))+'.txt'
        fname = BASE_DIR+'/Config/'+fname
        with open(self.config,'a+') as f:
            f.write(fname+':'+str(tid)+'\n')
            f.flush()
        with open(fname,'w+') as f:
            f.write(self.url)
            f.flush()

    def run(self,url):
        gen_config(url)
        t = test_multy_suite(['distribution'])
        filename = 'F:\\report\\distribution'+str(get_time())+'.html'
        fp = file(filename,'wb')
        # t = unittest.TestSuite()
        # #t.addTest(unittest.makeSuite(t1))
        # unittest.TextTestRunner().run(t1)
        runner = HTMLTestRunner.HTMLTestRunner(
                stream = fp,
                title ='Distribute_Test',
                description = 'Report_discription')

        runner.run(t)
        fp.close()


def excute(ip_list):
    host = '127.0.0.1'
    port = 4723
    bootstrap_port = 4724
    log_path = 'e:/appium_log'
    device_uid=[x+':5555' for x in ip_list]
    url_list = []
    stop_appium()
    sleep(5)
    for i in range(0,len(device_uid)*2,2):
        t_port = port+i
        t_bootstrap_port = port+i+1
        #url = threading.Thread(target =start_appium,args=(host, t_port, t_bootstrap_port, log_path,device_uid[i],))
        url = start_appium(host, t_port, t_bootstrap_port, log_path,device_uid[i/2])
        print url
        url_list.append(url[1])
        time.sleep(5)
        #url.start()
    thread_list = []
    import multiprocessing
    t_list = []
    for urls in range(len(url_list)):
        print urls
        #gen_config(url_list[urls])
        t_list.append(Distribute(url_list[urls],urls))
        t = multiprocessing.Process(target=t_list[urls].run,args=(url_list[urls],))
        t.start()
        print t.pid
        sleep(5)

if __name__ == '__main__':
    # t = test_multy_suite(['search'])
    # import HTMLTestRunner
    # # t = unittest.TestSuite()
    # # t.addTest(unittest.makeSuite(TestComment))
    # #unittest.TextTestRunner.run(t)
    # filename = 'F:\\report\\plug_test_search'+str(get_time())+'.html'
    # fp = file(filename,'wb')
    # runner = HTMLTestRunner.HTMLTestRunner(
    #         stream = fp,
    #         title ='Plug_Test',
    #         description = 'Report_discription')
    #
    # runner.run(t)
    # fp.close()
    ip_list = ['192.168.1.112','192.168.1.115','192.168.1.110']
    # t = []
    package = 'com.cnhubei.dxxwhw'
    package_path = 'g:/downloads/938.apk'
    excute(ip_list)
