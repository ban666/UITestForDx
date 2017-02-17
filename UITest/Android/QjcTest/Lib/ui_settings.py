# -*- coding: utf-8 -*-
__author__ = 'liaoben'


from appium import webdriver
import time,sys
from elements_id import *
from appium_lib import *
from common import exception_handler
import chardet
@exception_handler
def go_to_settings(driver):
    driver.find_element_by_id(MY_CONFIG).click()


@exception_handler
def get_push_state(driver):
    return driver.find_element_by_id(PUSH_OPTION).get_attribute('checked')


@exception_handler
def set_push_state(driver,state):
    if get_push_state(driver) != state:
        driver.find_element_by_id(PUSH_OPTION).click()
    return True


@exception_handler
def setting_to_index(driver):
    back(driver)
    sleep(WAIT_TIME)
    click_right_side(driver)
    return True


@exception_handler
def set_location(driver,location,retry=3,wait=3):
    try:
        location = location.decode('utf-8')
    except:
        pass
    if get_location(driver) == location:
        driver.find_element_by_id(LOCATION_SETIINGS).click()
        sleep(wait)
        back(driver)
        return True
    driver.find_element_by_id(LOCATION_SETIINGS).click()
    sleep(wait)
    count = 1

    while not element_exsist(driver,'uiselector','new UiSelector().text(\"'+location+'\")'):
        if count == retry:
            return False
        slide_up(driver,per=3)
        sleep(wait)
        count += 1
    driver.find_element_by_android_uiautomator('new UiSelector().text(\"'+location+'\")').click()
    sleep(wait)
    driver.find_element_by_id(LOCATION_SETIINGS).click()
    sleep(wait)
    back(driver)
    return True


@exception_handler
def get_location(driver):
    return driver.find_element_by_id(LOCATION_SETIINGS).text


@exception_handler
def get_version_code(driver):
    return driver.find_element_by_id(VERSION).text