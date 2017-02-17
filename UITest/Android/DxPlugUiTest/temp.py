# -*- coding: utf-8 -*-
__author__ = 'liaoben'
import os
import threading
import ctypes
import time
import requests
def pthread_level1(i):
    print "workor id :%s"%i
    #获取threading对象的标识ident
    print threading.currentThread()
    print threading.currentThread().ident
    print "threaing id: ",ctypes.CDLL('libc.so.6').syscall(186)
    d = requests.get("http://www.google.com")
    time.sleep(100)
    return

def test_a(fn):
    for i in range(10):
        with open(fn,'r+') as f:

            print str(os.getpid())+f.read()


if __name__ == "__main__":
    # l = []
    # for i in xrange(5):
    #     t = threading.Thread(target=pthread_level1,args=(i,))
    #     l.append(t)
    # for i in l:
    #     i.start()
    # #查看进程跟线程的关系
    # os.system("pstree -p " + str(os.getpid()))
    # for i in l:
    #     i.join()
    # print "Sub-process done."
    import multiprocessing
    fn = 'g:/1.txt'

    for i in range(5):
        t = multiprocessing.Process(target=test_a,args=(fn,))
        t.start()
