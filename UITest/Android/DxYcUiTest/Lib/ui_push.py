# -*- coding: utf-8 -*-
__author__ = 'liaoben'

from appium import webdriver
import time,sys
from elements_id import *
from appium_lib import *
from common import exception_handler
from time import sleep
from config import JPUSH_TIMEOUT,JPUSH_TITLE
from adb import get_product_name

@exception_handler
def get_push_info(driver,timeout=JPUSH_TIMEOUT,title = JPUSH_TITLE):
    open_notifications(driver)
    sleep(10)
    ret = []
    notification_el = NOTIFICATION_ITEM.get('default') if not NOTIFICATION_ITEM.has_key(get_product_name()) \
        else NOTIFICATION_ITEM.get(get_product_name())
    for i in range(int(timeout)):
        try:
            notification_list = driver.find_elements_by_id(notification_el)
            for notification in notification_list:
                t = notification.find_element_by_id(NOTIFICATION_TITLE).text
                #print t
                if t == title:
                    ret.append(notification.find_element_by_id(NOTIFICATION_TEXT).text)
            if len(ret)!= 0:
                close_notification(driver)
                sleep(WAIT_TIME)
                return  ret
        except:
            sleep(1)
    close_notification(driver)
    sleep(WAIT_TIME)
    return False


@exception_handler
def get_push_el(driver,timeout=JPUSH_TIMEOUT,title = JPUSH_TITLE):
    open_notifications(driver)
    ret = []
    notification_el = NOTIFICATION_ITEM.get('default') if not NOTIFICATION_ITEM.has_key(get_product_name()) \
        else NOTIFICATION_ITEM.get(get_product_name())
    print notification_el
    for i in range(int(timeout)):
        try:
            notification_list = driver.find_elements_by_id(notification_el)

            for notification in notification_list:
                t = notification.find_element_by_id(NOTIFICATION_TITLE).text
                #print t
                if t == title:
                    print 'get'
                    ret.append(notification.find_element_by_id(NOTIFICATION_TEXT))
            if len(ret)!= 0:
                close_notification(driver)
                sleep(WAIT_TIME)
                return ret
        except:
            sleep(1)
    close_notification(driver)
    sleep(WAIT_TIME)
    return False