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

if __name__ == '__main__':
    t = test_multy_suite(['comment','jpush','search','mycomment','update'])
    import HTMLTestRunner
    # t = unittest.TestSuite()
    # t.addTest(unittest.makeSuite(TestComment))
    #unittest.TextTestRunner.run(t)
    filename = 'F:\\report\\ios_yc_test'+str(get_time())+'.html'
    fp = file(filename,'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
            stream = fp,
            title ='Plug_Test',
            description = 'Report_discription')

    runner.run(t)
    fp.close()


