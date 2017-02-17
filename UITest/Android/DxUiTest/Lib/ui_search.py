# -*- coding: utf-8 -*-
from appium import webdriver
from elements_id import *
from config import *
from appium_lib import *
__author__ = 'liaoben'


def search_clue(driver,content):
    # try:
    #     content = content.decode('utf-8')
    # except:
    #     pass
    if not element_exsist(driver,'id',SEARCH_EDITTEXT):
        get_to_search(driver,MODE)
    el = driver.find_element_by_id(SEARCH_EDITTEXT)
    el.send_keys(content)
    driver.press_keycode(66)
    driver.find_element_by_name(CLUESEARCHTABTXT).click()
    result = element_exsist(driver,'id',HEAD_CONTENT,)
    if result:
        return True
    else:
        return False