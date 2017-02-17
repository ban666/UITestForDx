# -*- coding: utf-8 -*-
__author__ = 'liaoben'

from appium import webdriver
import time,sys
from elements_id import *
from appium_lib import *
from common import exception_handler
from time import sleep
from config import JPUSH_TIMEOUT,JPUSH_TITLE


def get_push_info(driver,timeout=JPUSH_TIMEOUT,title = JPUSH_TITLE):
    open_notifications(driver)
    ret = []
    for i in range(int(timeout)):
        try:
            notification_list = driver.find_elements_by_class_name('UIATableCell')

            for notification in notification_list:
                t = notification.text
                if t.split(',')[0] == title:
                    ret.append(t.split(',')[-1])
            if len(ret)!= 0:
                close_notification(driver)
                sleep(WAIT_TIME)
                return ret
        except:
            sleep(1)
    close_notification(driver)
    sleep(WAIT_TIME)
    return False

def confirm_push(driver,timeout=JPUSH_TIMEOUT):
    for i in range(int(timeout)):
        try:
            driver.find_element(*NOTIFICATION_OK).click()
            sleep(WAIT_TIME)
            return True
        except:
            sleep(1)
    return False


def get_push_el(driver,timeout=JPUSH_TIMEOUT,title = JPUSH_TITLE):
    open_notifications(driver)
    ret = []
    for i in range(int(timeout)):
        try:
            notification_list = driver.find_elements_by_class_name('UIATableCell')

            for notification in notification_list:
                t = notification.text
                if t.split(',')[0] == title:
                    print 'get'
                    ret.append(notification.find_elements_by_class_name('UIAStaticText')[-1])
            if len(ret)!= 0:
                close_notification(driver)
                sleep(WAIT_TIME)
                return ret
        except:
            sleep(1)
    close_notification(driver)
    sleep(WAIT_TIME)
    return False