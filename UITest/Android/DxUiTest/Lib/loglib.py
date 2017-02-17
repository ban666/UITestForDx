# -*- coding:utf-8 -*-
__author__ = 'Ban'


import logging,os,time

def WritetoLog(fname,msg):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(fname,encoding='utf-8')
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s: %(message)s \r\n')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.info(msg.decode('utf-8'))

    logger.removeHandler(fh)
    logger.removeHandler(ch)

def log(fname,msg):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(fname,encoding='utf-8')
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s: %(message)s \r\n')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.info(msg.decode('utf-8'))

    logger.removeHandler(fh)
    logger.removeHandler(ch)

