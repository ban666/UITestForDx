# -*- coding: utf-8 -*-
__author__ = 'liaoben'

import os
import commands
import subprocess
from lxml import etree

def get_shell_config():
    cmd = 'adb shell cat /data/data/com.zc.hubei_news/shared_prefs/config.xml'
    p = subprocess.Popen(cmd, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    curline = p.stdout.readlines()
    #print curline
    return curline

def analysis_config(content):
    ret = {}
    t = etree.fromstringlist(content)
    t = etree.ElementTree(t)
    r = t.getroot()
    for i in r:
        key = i.values()[0]
        val = i.text
        print key,val
        ret[key] = val
    return ret

def get_config():
    c = get_shell_config()
    r = analysis_config(c)
    return r

print get_config()['uid']