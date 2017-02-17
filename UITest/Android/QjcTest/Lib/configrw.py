# -*- coding:utf-8 -*-
__author__ = 'Ban'

import ConfigParser
import os

def readcfg(cfg,opt='testcase'):
    list1=[]
    cfg=''.join([os.path.splitext(cfg)[0],'.cfg'])
    config=ConfigParser.ConfigParser()
    with open(cfg,"r") as cfgfile:
        config.readfp(cfgfile)
        op=config.options(opt)
    for i in op:
        list1.append(config.get(opt,i).split(','))
    return list1

def updateGlobal(vallist,cfg=''):
    config=ConfigParser.ConfigParser()
    config.read(cfg)
    for val in valist:
        config.set('Global',val[0],val[1])
    config.write( open(cfg, 'r+') )

