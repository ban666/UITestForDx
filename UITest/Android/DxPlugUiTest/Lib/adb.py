# -*- coding: utf-8 -*-
__author__ = 'liaoben'

import subprocess
import os
import socket
import threading
import time
from lxml import etree
from common import download_latest_apk
from config import *

def external_cmd(cmd, msg_in=''):
    try:
        proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,)
        stdout_value, stderr_value = proc.communicate(msg_in)
        return stdout_value, stderr_value
    except ValueError, err:
        # log("IOError: %s" % err)
        return None, None


def start_appium(host, port, bootstrap_port, appium_log_path,device_uid): #device_uid,
        #appium -p 4723 -bp 4724 -U 22238e79 --command-timeout 600
        errormsg = ""
        appium_server_url =""
        if not os.path.isdir(appium_log_path):
            os.mkdir(appium_log_path)
        log = appium_log_path+'/'+time.strftime("%Y%m%d%H%M%S", time.localtime())+'.txt'
        try:
            if not is_open(host,port):
                cmd ='start /b appium -a '+ host +' -p '+ str(port)+ ' --bootstrap-port '+ str(bootstrap_port) +  ' --session-override --log '+ '"'+log + '" --command-timeout 600' + ' -U '+ device_uid
                #print cmd
                #p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) #stdout=PIPE, stderr=PIPE)
                p = subprocess.call(cmd, shell=True,stdout=open('e:/log.log','w'),stderr=subprocess.STDOUT)
                #print p
                appium_server_url = 'http://' + host +':' + str(port) +'/wd/hub'
                print appium_server_url
            else:
                print "port:%d is used!"%(port)
        except Exception, msg:
            errormsg = str(msg)
            print errormsg
            return False,errormsg
        return True,appium_server_url

def stop_appium():
         #cmd = 'stop_appium.bat %s'%(self.get_port(Appium_url))
         cmd ='TASKKILL /F /IM cmd.exe /IM node.exe'
         print cmd
         #cmd=''
         p = os.popen(cmd)
         print p.read()

def is_open(ip,port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        s.connect((ip,int(port)))
        s.shutdown(2)
        #print '%d is open' % port
        return True
    except:
        #print '%d is down' % port
        return False

def change_danmu_state_by_adb(package_name,state=1):
    up_path = os.path.dirname(os.getcwd())
    fname_open = '/Tools/danmaku_open'
    fname_close = '/Tools/danmaku_close'
    result = False
    for i in range(10):
        if os.path.exists(up_path+fname_open):
            result = True
            break
        up_path = os.path.dirname(up_path)
    if not result:
        return result
    fn_open = up_path+fname_open
    fn_close = up_path+fname_close
    f = {
        '1':fn_open,
        '0':fn_close
    }
    cmd = 'adb push '+f[str(state)]+' /data/data/'+package_name+'/cache/List/danmaku.0'
    print cmd
    p = os.popen(cmd)
    print p.read()
    return True

def change_input_method_by_adb(method=3):
    command0 ='adb shell ime list -s'
    command1 ='adb shell settings get secure default_input_method'
    command2 ='adb shell ime set com.android.inputmethod.latin/.LatinIME'
    command3 ='adb shell ime set io.appium.android.ime/.UnicodeIME'
    way = {
        '0':command0,
        '1':command1,
        '2':command2,
        '3':command3
    }
    p = os.popen(way[str(method)])
    print p.read()

def get_config_by_adb(package):
    cmd = 'adb shell cat '+ '/data/data/'+package+'/shared_prefs/config.xml'
    print cmd
    p = os.popen(cmd)
    content = p.read()
    root = etree.XML(content)
    children = root.getchildren()
    ret_list = {}
    for i in children:
        #print dir(i)
        vals = i.values()
        if len(vals) == 2:
            ret_list[vals[0]] = vals[1]
        elif len(vals) == 1:
            ret_list[vals[0]] = i.text
    return ret_list

def is_login(package):
    content = get_config_by_adb(package)
    if content.get('uid'):
        return True
    return False


def install(apk):
    cmd = 'adb install '+ apk
    #print cmd
    p = os.popen(cmd)
    content = p.read()
    #print content
    if content.find('INSTALL_FAILED_ALREADY_EXISTS')!=-1:
        return False
    return True

def uninstall(package):
    cmd = 'adb uninstall  '+ package
    #print cmd
    p = os.popen(cmd)
    content = p.read()
    #print content
    return True

def download_and_install():
    apk = download_latest_apk()
    uninstall(desired_caps['appPackage'])
    if install(apk):
        return True
    return False


def get_product_name():
    cmd = 'adb shell cat /system/build.prop'
    p = os.popen(cmd)
    content = p.read()
    for con in content.split('\n'):
        if con.find('ro.product.model')!=-1:
            product = con.split('=')[1].replace('\r','')
            return product
    return False

if __name__ == '__main__':
    # host = '127.0.0.1'
    # port = 4723
    # bootstrap_port = 4724
    # log_path = 'e:/appium_log'
    # device_uid='192.168.1.112:5555'
    # for i in range(5):
    #     t_port = port+i
    #     t_bootstrap_port = port+i+2
    #     url = threading.Thread(target =start_appium,args=(host, t_port, t_bootstrap_port, log_path,device_uid,))
    #     url.start()
    #is_open('127.0.0.1',port)
    #stop_appium(port)
    #change_danmu_state_by_adb('com.cnhubei.dxxwhw',0)
    #change_input_method_by_adb(0)
    package = 'com.cnhubei.dxxwhw'
    ret =  get_product_name()
    print ret