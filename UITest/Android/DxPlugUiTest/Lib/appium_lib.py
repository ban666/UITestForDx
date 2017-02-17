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
from config import *

'''
电话键

KEYCODE_CALL 拨号键 5
KEYCODE_ENDCALL 挂机键 6
KEYCODE_HOME 按键Home 3
KEYCODE_MENU 菜单键 82
KEYCODE_BACK 返回键 4
KEYCODE_SEARCH 搜索键 84
KEYCODE_CAMERA 拍照键 27
KEYCODE_FOCUS 拍照对焦键 80
KEYCODE_POWER 电源键 26
KEYCODE_NOTIFICATION 通知键 83
KEYCODE_MUTE 话筒静音键 91
KEYCODE_VOLUME_MUTE 扬声器静音键 164
KEYCODE_VOLUME_UP 音量增加键 24
KEYCODE_VOLUME_DOWN 音量减小键 25

控制键

KEYCODE_ENTER 回车键 66
KEYCODE_ESCAPE ESC键 111
KEYCODE_DPAD_CENTER 导航键 确定键 23
KEYCODE_DPAD_UP 导航键 向上 19
KEYCODE_DPAD_DOWN 导航键 向下 20
KEYCODE_DPAD_LEFT 导航键 向左 21
KEYCODE_DPAD_RIGHT 导航键 向右 22
KEYCODE_MOVE_HOME 光标移动到开始键 122
KEYCODE_MOVE_END 光标移动到末尾键 123
KEYCODE_PAGE_UP 向上翻页键 92
KEYCODE_PAGE_DOWN 向下翻页键 93
KEYCODE_DEL 退格键 67
KEYCODE_FORWARD_DEL 删除键 112
KEYCODE_INSERT 插入键 124
KEYCODE_TAB Tab键 61
KEYCODE_NUM_LOCK 小键盘锁 143
KEYCODE_CAPS_LOCK 大写锁定键 115
KEYCODE_BREAK Break/Pause键 121
KEYCODE_SCROLL_LOCK 滚动锁定键 116
KEYCODE_ZOOM_IN 放大键 168
KEYCODE_ZOOM_OUT 缩小键 169

组合键

KEYCODE_ALT_LEFT Alt+Left
KEYCODE_ALT_RIGHT Alt+Right
KEYCODE_CTRL_LEFT Control+Left
KEYCODE_CTRL_RIGHT Control+Right
KEYCODE_SHIFT_LEFT Shift+Left
KEYCODE_SHIFT_RIGHT Shift+Right

基本

KEYCODE_0 按键'0' 7
KEYCODE_1 按键'1' 8
KEYCODE_2 按键'2' 9
KEYCODE_3 按键'3' 10
KEYCODE_4 按键'4' 11
KEYCODE_5 按键'5' 12
KEYCODE_6 按键'6' 13
KEYCODE_7 按键'7' 14
KEYCODE_8 按键'8' 15
KEYCODE_9 按键'9' 16
KEYCODE_A 按键'A' 29
KEYCODE_B 按键'B' 30
KEYCODE_C 按键'C' 31
KEYCODE_D 按键'D' 32
KEYCODE_E 按键'E' 33
KEYCODE_F 按键'F' 34
KEYCODE_G 按键'G' 35
KEYCODE_H 按键'H' 36
KEYCODE_I 按键'I' 37
KEYCODE_J 按键'J' 38
KEYCODE_K 按键'K' 39
KEYCODE_L 按键'L' 40
KEYCODE_M 按键'M' 41
KEYCODE_N 按键'N' 42
KEYCODE_O 按键'O' 43
KEYCODE_P 按键'P' 44
KEYCODE_Q 按键'Q' 45
KEYCODE_R 按键'R' 46
KEYCODE_S 按键'S' 47
KEYCODE_T 按键'T' 48
KEYCODE_U 按键'U' 49
KEYCODE_V 按键'V' 50
KEYCODE_W 按键'W' 51
KEYCODE_X 按键'X' 52
KEYCODE_Y 按键'Y' 53
KEYCODE_Z 按键'Z' 54
'''


def paste(driver):
    driver.press_keycode(50,28672)

def back(driver):
    driver.press_keycode(4)


def home(driver):
    driver.press_keycode(3)


def quit_app(driver,wait=3):
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


def slide_up(driver,per=1):
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    driver.swipe(x/2, y/10*(10-per), x/2, y/10*1, 0)

def slide_custom(driver,start_x,start_y,end_x,end_y):
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    driver.swipe(start_x*x, start_y*y, end_x*x, end_y*y, 0)



def slide_down(driver,per=3,wait_time = 3):
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    driver.swipe(x/2, y/10*1, x/2, y/10*(1+per), 0)
    sleep(WAIT_TIME)


def slide_left(driver):
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    driver.swipe(x/4*3, y/2, x/4*0.5, y/2, 0)


def slide_right(driver):
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    driver.swipe(x/4, y/2, x*3/4, y/2, 0)


def close_notification(driver):
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    driver.swipe(x/2, y*9/10,2/x,y/10)


def click_center(driver):
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    driver.tap([(x/2, y/2)])


def press_back(driver):
    driver.press_keycode(4)


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


def start_to_index(driver,mode,method=''):
    if mode == 'mcp/plug/app':
        box = driver.find_elements_by_class_name('android.widget.CheckBox')
        if method == 'all':
            for i in box:
                i.click()
        driver.find_element_by_class_name('android.widget.Button').click()
    elif mode == 'mcp/dx':
        sleep(4)

@exception_handler
def get_to_search(driver):
    driver.find_element_by_id(SEARCH_BUTTON).click()
    return True



@exception_handler
def go_to_mycomm(driver,mode):
    if mode == 'mcp/dx':
        driver.find_element_by_id(MENU_ICON).click()
        driver.find_element_by_id(MY_COMM).click()
        return True


@exception_handler
def go_to_head(driver):
    driver.find_element_by_id(HEAD).click()
    return True


@exception_handler
def go_to_comment_page(driver,is_photo = False):
    if is_photo:
        driver.find_element_by_id(COMMENT_PHOTO_ENTRANCE).click()
        return True
    driver.find_element_by_id(COMMENT_COUNT).click()
    return True


def seach_by_ui(driver,title):
    result = False
    try:
        el = driver.find_element_by_id(SEARCH_EDITTEXT)
        el.send_keys(title)
        #a = driver.available_ime_engines
        #driver.activate_ime_engine(a[0])
        #el.click()
        #driver.tap([postion])
        #driver.activate_ime_engine(a[-1])
        el.click()
        driver.press_keycode(66)
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
        el = driver.find_element_by_class_name('android.widget.RelativeLayout')\
            .find_element_by_class_name('android.widget.TextView').click()
        #print el.find_element_by_class_name('android.widget.RelativeLayout').find_element_by_class_name('android.widget.TextView').text
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
    back(driver)


def refresh_article(driver):
    back(driver)
    sleep(WAIT_TIME)
    driver.find_element_by_class_name('android.widget.RelativeLayout')\
            .find_element_by_class_name('android.widget.TextView').click()
    return True


def login(driver,mode,package,phone,tid='a_imei000000000000000'):
    if mode == 'mcp/dx':
        try:
            from adb import get_config_by_adb
            driver.find_element_by_id(elements_id.MENU_ICON).click()
            driver.find_element_by_id(elements_id.PHONE_LOGIN_ICON).click()
            driver.find_element_by_id(elements_id.PHONE_INPUT).send_keys(phone)
            driver.find_element_by_id(elements_id.GET_VCODE).click()
            sleep(5)
            dc = get_config_by_adb(package)['dc']
            r = RedisHandler()
            vcode = r.get_vcode_by_dc(phone,dc,tid)
            driver.find_element_by_id(elements_id.VCODE_INPUT).send_keys(vcode)
            driver.find_element_by_id(elements_id.PHONE_LOGIN_BUTTON).click()
            return True
        except Exception,e:
            print sys._getframe().f_code.co_name
            print e.__repr__()
            return False

def login_to_index(driver,mode,package,phone,tid='a_imei000000000000000'):
    try:
        assert login(driver,mode,package,phone,tid)
        sleep(2)
        x = driver.get_window_size()['width']
        y = driver.get_window_size()['height']
        position = [(x-10,y/2)]
        print position
        retry = 0
        while element_exsist(driver,'id',elements_id.MY_COMM):
            if retry >= 10:
                print 'Error!'
                return False
            driver.tap(position)
            retry +=1
        return True
    except Exception,e:
        print sys._getframe().f_code.co_name
        print e.__repr__()
        return False

def logout(driver,mode):
    if mode == 'mcp/dx':
        try:
            driver.find_element_by_id(elements_id.MENU_ICON).click()
            driver.find_element_by_id(elements_id.USER_ICON).click()
            driver.find_element_by_id(elements_id.LOGOUT_BUTTON).click()
            driver.find_element_by_android_uiautomator('new UiSelector().text(\"登出\")').click()
            return True
        except Exception,e:
            print sys._getframe().f_code.co_name
            print e.__repr__()
            return False


def logout_to_index(driver,mode):
    try:
        assert logout(driver,mode)
        sleep(2)
        x = driver.get_window_size()['width']
        y = driver.get_window_size()['height']
        position = [(x-10,y/2)]
        print position
        retry = 0
        while element_exsist(driver,'id',elements_id.MY_COMM):
            if retry >= 10:
                print 'Error!'
                return False
            driver.tap(position)
            retry +=1
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
def seekbar_sendkey(driver,per,):
    el = driver.find_element_by_id(AUDIO_PROGRESS)
    position = el.location
    size = el.size
    point ={
               'x':position['x'],
               'y':position['y']+size['height']/2,
               'length':size['width']
    }
    end_point =[(point['x']+per*point['length'],point['y'])]
    from random import randint
    way= randint(0,1)

    if way == 0:
        print u'进度条调整方式：拖动'
        driver.swipe(point['x'],point['y'],point['x']+per*point['length'],point['y'],1000)
    elif way == 1:
        print u'进度条调整方式：点击'
        driver.tap(end_point)
    #
    #
    # #拖动实现效果较差，改为点击
    # driver.swipe(point['x'],point['y'],point['x']+per*point['length'],point['y'],1000)
    # driver.tap(end_point)
    #sleep(wait)
    return True


@exception_handler
def get_alltime(driver):
    return driver.find_element_by_id(AUDIO_ALL_TIME).text


@exception_handler
def get_played_time(driver):
    return driver.find_element_by_id(AUDIO_PLAY_TIME).text


@exception_handler
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
    el = driver.find_element_by_id(NOTIFICATION_AUDIO_PLAY)
    scr.get_screenshot_by_element(el,fname)
    result = False
    for pic in status_dict.get(status):
        if scr.same_as(fname,pic):
            result = True

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



@exception_handler
def clear_notification(driver):
    driver.open_notifications()
    if element_exsist(driver,'id',XIAOMI_SETTINGS):
        slide_right(driver)
    sleep(WAIT_TIME)
    try:
        driver.find_element_by_id(NOTIFICATION_CLEAR_BUTTON).click()
    except:
        print 'no el find'
    close_notification(driver)

def click_right_side(driver):
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    driver.tap([(x-2, y/2)])


def open_notifications(driver):
    driver.open_notifications()
    if element_exsist(driver,'id',XIAOMI_SETTINGS):
        slide_right(driver)


def get_appium_url_from_config(path=DISTRIBUTE_CONFIG_PATH):
    tid = os.getpid()
    print 'inside',tid
    if os.path.exists(path):
        with open(path,'r+') as f:
            content = f.read()
            for i in content.split('\n'):
                t = i.split(',')
                if len(t) == 2:
                    if t[1] ==str(tid):
                        c = t[0]
                        return c

if __name__ == '__main__':
    a = get_appium_url_from_config()
    print a