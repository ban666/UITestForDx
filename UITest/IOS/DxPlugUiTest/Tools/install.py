# -*- coding: utf-8 -*-
__author__ = 'liaoben'

import subprocess
import os
import requests
from bs4 import BeautifulSoup
from urllib import urlretrieve

URL = {
    'dx':'http://10.99.113.28/apk/',
    'yc':'http://10.99.113.28/ycdxapk/',
    'sdk':'http://10.99.113.28/pluginapk/',
    'qj':'http://10.99.113.28/qjapk/'
}

PACKAGE = {
     'dx':'com.zc.hubei_news',
    'yc':'com.cnhubei.ycdx',
    'sdk':'com.cnhubei.dxxwhw',
    'qj':'com.cnhubei.qjxw'
}

def external_cmd(cmd, msg_in=''):
    try:
        proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,)
        stdout_value, stderr_value = proc.communicate(msg_in)
        return stdout_value, stderr_value
    except ValueError, err:
        # log("IOError: %s" % err)
        return None, None


def install(apk):
    cmd = 'adb install '+ apk
    #print cmd
    p = os.popen(cmd)
    content = p.read()
    print content
    if content.find('INSTALL_FAILED_ALREADY_EXISTS')!=-1:
        return False
    return True

def uninstall(package):
    cmd = 'adb uninstall  '+ package
    #print cmd
    p = os.popen(cmd)
    content = p.read()
    print content
    return True


def download_latest_apk(url,path):
    r = requests.get(url)
    content = r.content
    soup = BeautifulSoup(content,'html')
    apk =  soup.find_all('a')[-1].text
    print apk
    download_path = url+apk
    local_path = path+apk
    urlretrieve (download_path, local_path)
    return local_path

#apktype: dx,yc,sdk,qj
def download_and_install(apk_type,path = ''):
    url = URL.get(apk_type)
    package = PACKAGE.get(apk_type)
    apk = download_latest_apk(url,path)
    uninstall(package)
    if install(apk):
        return True
    return False


if __name__ == '__main__':
    path = 'g:/apk/'
    ret =  download_and_install('dx',path)
    print ret