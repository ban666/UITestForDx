#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: liaoben
# @Date:   2015-10-27 10:14:36
# @Last Modified by:   liaoben
# @Last Modified time: 2015-11-18 15:25:10

from appium import webdriver
import time,sys
from redis_handler import RedisHandler
from elements_id import *
from appium.common.exceptions import NoSuchContextException
from selenium.webdriver.common.by import By
from appium.webdriver.common.mobileby import MobileBy
from common import exception_handler,get_now
from appium.webdriver.connectiontype import ConnectionType
from time import sleep
from screenshot import Appium_Extend
#from adb import check_login_status,get_product_name
from config import *


def paste(driver):
    driver.press_keycode(50,28672)

def back(driver,button = BACK_BUTTON):
    #driver.press_keycode(4)
    for back_el in BACK_BUTTON_LIST:
        if element_exsist(driver,*back_el):
            back_button = driver.find_element(*back_el)
            center = get_el_center(back_button)
            driver.tap([center])
            return True
    return False


def home(driver):
    driver.press_keycode(3)


def quit_app(driver,wait=1):
    back(driver)
    sleep(wait)
    back(driver)


def element_exsist(driver,by,e):
    method = {
        'id':By.ID,
        'class':By.CLASS_NAME,
        'xpath':By.XPATH,
        'uiselector':MobileBy.ANDROID_UIAUTOMATOR
    }
    if not method.has_key(by):
        print 'wrong location method!'
        return False
    try:
        driver.find_element(by= method.get(by),value=e)
        return True
    except NoSuchContextException:
        return False
    except Exception:
        return False


def slide_up(driver,per=1,duration=0):
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    #print x/2, y/10*(10-per), 0,y*9/10-per*y/10
    driver.swipe(x/2, y*9/10, 0, -per*y/10, duration)

def slide_custom(driver,start_x,start_y,end_x,end_y):
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    driver.swipe(start_x*x, start_y*y, end_x*x, end_y*y, 0)


def slide_down(driver,per=3,wait_time = 3):
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    #print x/2, y/10*2, x/2, y/10*(2+per)
    driver.swipe(x/2, y/10*2, 0, y/10*(2+per), 0)
    sleep(WAIT_TIME)


def slide_left(driver):
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    driver.swipe(x/4*3, y/2, -2*x/4, 0, 0)


def slide_right(driver,per=1):
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    #print x/4*0.5, y/2, x*(1+per)/4-1, y/2
    driver.swipe(x/4*0.5, y/2, x*(1+per)/4, 0, 0)




def click_center(driver):
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    driver.tap([(x/2, y/2)])

def clear_notification(driver,wait=3):
    open_notifications(driver)
    while element_exsist(driver,*NOTIFICATION_CLEAR_BUTTON):
        driver.find_element(*NOTIFICATION_CLEAR_BUTTON).click()
        sleep(2)
        driver.find_element(*NOTIFICATION_CLEAR_CONFIRM).click()
        sleep(2)
    close_notification(driver)

def press_back(driver):
    driver.press_keycode(4)


def get_el_center(el):
    size = el.size
    location = el.location
    center = (location['x']+size['width']/2,location['y']+size['height']/2)
    return center


@exception_handler
def swipe_el_to_right(driver,el):
    position = el.location
    size = el.size
    point ={
               'x':position['x'],
               'y':position['y']+size['height']/2,
               'length':size['width']
    }
    x = driver.get_window_size()['width']
    driver.swipe(point['x'],point['y'],x-2,point['y'],1000)
    return True


def start_to_index(driver,mode,method='normal',cancel=True):
    # if mode == 'mcp/plug/app':
    #     box = driver.find_elements_by_class_name('android.widget.CheckBox')
    #     if method == 'all':
    #         for i in box:
    #             i.click()
    #     driver.find_element_by_class_name('android.widget.Button').click()
    # elif mode == 'mcp/dx':
    #     sleep(4)
    sleep(5)
    driver.find_element(*START_BUTTON[method]).click()
    sleep(5)
    # if element_exsist(driver,*IGNORE_BUTTON) and cancel:
    #     print 'update exsist'
    #     driver.find_element(*IGNORE_BUTTON).click()
    #     sleep(3)


@exception_handler
def get_to_search(driver):
    #driver.find_element(*INFORMATION).click()
    driver.find_element(*SEARCH_BUTTON).click()
    return True



@exception_handler
def go_to_mycomm(driver,mode):
    driver.find_element(*MY_CONFIG).click()
    driver.find_element(*MY_COMM).click()
    return True


@exception_handler
def go_to_head(driver):
    driver.find_element(*HEAD).click()
    return True


@exception_handler
def go_to_comment_page(driver,entrance=COMMENT_ENTRANCE):
    driver.find_element(*entrance).click()


def seach_by_ui(driver,title):
    result = False
    try:
        el = driver.find_element(*SEARCH_EDITTEXT)
        el.send_keys(title)
        el.click()
        driver.find_element(*SEARCH_KEYBOARD).click()
        result = True
    except Exception,e:
        print e.__repr__()
        result = False
    finally:
        return result


def get_to_article_by_search(driver,title,mode=''):
    result = False
    try:
        title = title.decode('utf-8')
    except:
        pass
    try:
        assert get_to_search(driver)
        sleep(WAIT_TIME)
        seach_by_ui(driver,title)
        sleep(WAIT_TIME)
        driver.find_element_by_id(title).click()
        result = True
    except Exception,e:
        print sys._getframe().f_code.co_name
        print e.__repr__()
        result = False
    finally:
        return  result


def click_search_item(driver,index):
    driver.find_elements_by_class_name('android.widget.RelativeLayout')[index]\
            .find_element_by_class_name('android.widget.TextView').click()
    return True

def search_article_to_index(driver,wait=3):
    back(driver)
    sleep(wait)
    driver.find_element(*SEARCH_CANCEL).click()
    sleep(wait)


def refresh_article(driver,title,button = BACK_BUTTON):
    back(driver,button)
    sleep(WAIT_TIME)
    driver.find_element_by_id(title).click()
    return True


def login(driver,phone,in_page = False):
    try:
        r = RedisHandler()
        r.clear_all_vcode_count()
        if not in_page:
            driver.find_element(*MY_CONFIG).click()
            driver.find_element(*PHONE_LOGIN_ICON).click()
        driver.find_element(*PHONE_INPUT).send_keys(phone)
        sleep(3)
        driver.find_element(*GET_VCODE).click()
        sleep(3)
        vcode = r.get_latest_vcode(phone)
        print vcode
        driver.find_element(*VCODE_INPUT).send_keys(vcode)
        sleep(5)
        driver.find_element(*PHONE_LOGIN_BUTTON).click()
        return True
    except Exception,e:
        print sys._getframe().f_code.co_name
        print e.__repr__()
        return False



def login_to_index(driver,phone):
    try:
        assert login(driver,phone)
        sleep(3)
        retry = 0
        while element_exsist(driver,*MY_COMM):
            if retry >= 10:
                print 'Error!'
                return False
            driver.find_element_by_id('menu1 1').click()
            retry +=1
        return True
    except Exception,e:
        print sys._getframe().f_code.co_name
        print e.__repr__()
        return False

def logout(driver,mode):
    try:
        driver.find_element(*MY_CONFIG).click()
        driver.find_element(*USER_ICON).click()
        driver.find_element(*LOGOUT_BUTTON).click()
        #driver.find_element_by_android_uiautomator('new UiSelector().text(\"登出\")').click()
        return True
    except Exception,e:
        print sys._getframe().f_code.co_name
        print e.__repr__()
        return False


def logout_to_index(driver,mode,get_dc=True):
    try:
        assert logout(driver,mode)
        sleep(3)
        driver.find_element_by_id('menu1 1').click()
        sleep(3)
    except Exception,e:
        print e.__repr__()
        return False

def change_network(driver,state):
    state_dict = {
        'wifi':ConnectionType.WIFI_ONLY,
        'data':ConnectionType.DATA_ONLY,
        'airplane':ConnectionType.AIRPLANE_MODE,
        'none':ConnectionType.NO_CONNECTION,
        'all':ConnectionType.ALL_NETWORK_ON
    }
    if not state_dict.has_key(state):
        print 'Wrong state'
        return False
    try:
        driver.set_network_connection(state_dict[state])
        return True
    except Exception,e:
        print 'Exception',e
        return False

@exception_handler
# def seekbar_sendkey(driver,per):
#     el = driver.find_element(*AUDIO_PROGRESS)
#     position = el.location
#     size = el.size
#     point ={
#                'x':position['x'],
#                'y':position['y']+size['height']/2,
#                'length':size['width']
#     }
#     end_point =[(per*point['length'],0)]
#     #拖动实现效果较差，改为点击
#     #driver.swipe(point['x'],point['y'],point['x']+per*point['length'],point['y'],1000)
#     driver.tap(end_point)
#     #sleep(wait)
#     return True

def seekbar_sendkey(driver,per):
    el = driver.find_element(*AUDIO_PROGRESS)
    position = el.location
    size = el.size
    point ={
               'x':position['x'],
               'y':position['y']+size['height']/2,
               'length':size['width']
    }
    end_point =[(per*point['length'],0)]
    ball_position = driver.find_element(*AUDIO_PROGRESS).get_attribute('value')
    ball_position = int(ball_position.replace('%',''))*0.01
    start_x = position['x'] + point['length']*ball_position

    #拖动实现效果较差，改为点击
    driver.swipe(start_x,point['y'],(per-ball_position)*point['length'],0,1000)
    #driver.tap(end_point)
    #sleep(wait)
    return True


@exception_handler
def get_alltime(driver):
    return driver.find_element(*AUDIO_ALL_TIME).text


@exception_handler
def get_played_time(driver):
    return driver.find_element(*AUDIO_PLAY_TIME).text


# @exception_handler
# def notification_status_judge(driver,status):
#     """
#     check audio notification status by screenshot
#     :param driver:
#     :param status: 'play' or 'pause'
#     :return: Boolean
#     """
#     fname =PIC_SAVE_PATH+'\\'+get_now()+'.png'
#     pause_image = IMAGE_PATH + '\\'+IMAGES['notification_pause']
#     start_image = IMAGE_PATH + '\\'+IMAGES['notification_start']
#     status_dict = {
#         'play': start_image,
#         'pause': pause_image
#     }
#     scr = Appium_Extend(driver)
#     el = driver.find_element(*NOTIFICATION_AUDIO_PLAY)
#     scr.get_screenshot_by_element(el,fname)
#     return scr.same_as(fname,status_dict.get(status))

def notification_status_judge(driver,status):
    """
    check audio notification status by screenshot
    :param driver:
    :param status: 'play' or 'pause'
    :return: Boolean
    """
    fname =PIC_SAVE_PATH+'\\'+get_now()+'.png'
    pause_image = [IMAGE_PATH + '\\'+x for x in IMAGES['notification_pause']]
    start_image = [IMAGE_PATH + '\\'+x for x in IMAGES['notification_start']]
    status_dict = {
        'play': start_image,
        'pause': pause_image
    }
    scr = Appium_Extend(driver)
    el = driver.find_element(*NOTIFICATION_AUDIO_PLAY)
    scr.get_screenshot_by_element(el,fname)
    result = False
    for pic in status_dict.get(status):
        if scr.same_as(fname,pic):
            result = True

    return result



def click_right_side(driver):
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    driver.tap([(x-2, y/2)])


def open_notifications(driver,wait=3):
    slide_custom(driver,0.5,0,0,0.8)
    sleep(wait)
    driver.find_element(*NOTIFICATION_BUTTON).click()
    sleep(wait)

def close_notification(driver,wait=3):
    slide_custom(driver,0.5,1,0,-0.5)
    sleep(wait)

def is_login(driver):
    result = False
    driver.find_element(*MY_CONFIG).click()
    if element_exsist(driver,*PHONE_LOGIN_ICON) == False:
        result = True
    driver.find_element(*('id','menu1 1')).click()
    sleep(WAIT_TIME)
    return result

def click_audio_in_webview(driver,click=(0.5,0.5),method='position'):
    if method == 'webview':
        driver.switch_to.context(driver.contexts[-1])
        driver.find_element_by_class_name('audio-start').click()
        sleep(WAIT_TIME)
        driver.switch_to.context(driver.contexts[0])
        return True
    else:
        x = driver.get_window_size()['width']
        y = driver.get_window_size()['height']
        tap_x = x*click[0]
        tap_y = y*click[1]
        print tap_x,tap_y
        driver.tap([(tap_x,tap_y)])
        sleep(WAIT_TIME)
        return True

def get_checked(el):
    checked = el.get_attribute('checked')
    if checked == 'true':
        return True
    return False


def play_video(driver):
    location = driver.find_element(*VIDEO_PLAY_IMAGE).location
    tap_location = (location['x'],location['y'])
    driver.tap([tap_location])


def judge_article_type(driver,article_type):
    type_dict = {
        'video':judge_video,
        'live_video':judge_live_video,
        'article':judge_article,
        'photo':judge_photo,
        'audio':judge_audio,
        'ext':judge_ext,
        'zhuanlan':judge_zhuanlan,
        'zhuanti':judge_zhuanti,
        'targeturl':judge_targeturl,
        'clue':judge_clue
    }
    return type_dict.get(article_type)(driver)


def judge_live_video(driver,count=20):
    for i in range(count):
        if not driver.find_element(*VIDEO_CLOSE).is_displayed():
            driver.find_element(*VIDEO_ITEM).click()
            sleep(1)
        if driver.find_element(*VIDEO_CLOSE).is_displayed() and not \
            driver.find_element(*VIDEO_PROGRESS).is_displayed():
            print 'type:live video'
            return True
    return False


def judge_video(driver,count=20):
    for i in range(count):
        if not driver.find_element(*VIDEO_CLOSE).is_displayed():
            driver.find_element(*VIDEO_ITEM).click()
        if driver.find_element(*VIDEO_PROGRESS).is_displayed():
            print 'type:video'
            return True
    return False


def judge_article(driver):
    return element_exsist(driver,'class','UIAWebView') and element_exsist(driver,*FONT_BUTTON)


def judge_photo(driver):
    return element_exsist(driver,*DOWNLOAD_BUTTON)


def judge_audio(driver):
    return element_exsist(driver,*AUDIO_PAUSE)


def judge_zhuanti(driver):
    return element_exsist(driver,*SHARE_BUTTON) and element_exsist(driver,*COLLECT_BUTTON) == False and \
        element_exsist(driver,*COLLECT_BUTTON_TYPE_B) == False


def judge_zhuanlan(driver):
    return element_exsist(driver,'class','UIAWebView') == False and element_exsist(driver,*FONT_BUTTON) == False and \
        element_exsist(driver,*SHARE_BUTTON) == False and element_exsist(driver,*COLLECT_BUTTON) == False

def judge_ext(driver):
    return element_exsist(driver,'class','UIAWebView') and driver.find_element(*FONT_BUTTON).is_displayed() == False and \
        driver.find_element(*SHARE_BUTTON).is_displayed() and driver.find_element(*COLLECT_BUTTON).is_displayed()

def judge_targeturl(driver):
    return element_exsist(driver,'class','UIAWebView') and driver.find_element(*FONT_BUTTON).is_displayed() == False and \
        driver.find_element(*SHARE_BUTTON).is_displayed() == False and driver.find_element(*COLLECT_BUTTON).is_displayed() == False

def judge_clue(driver):
    return driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIAStaticText[1]').text == u'报料详情'