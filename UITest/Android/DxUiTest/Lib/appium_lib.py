#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: liaoben
# @Date:   2015-10-27 10:14:36
# @Last Modified by:   liaoben
# @Last Modified time: 2015-11-18 15:25:10

from appium import webdriver
from random import randint
import time,sys
from redis_handler import RedisHandler
from elements_id import *
from appium.common.exceptions import NoSuchContextException
from selenium.webdriver.common.by import By
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.connectiontype import ConnectionType
from common import exception_handler
from config import *
from time import sleep
from adb import *
import os
from DbLib import DbLib
from mongo import Mongo

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

def quit_app(driver,wait=3):
    back(driver)
    sleep(1)
    back(driver)
    sleep(wait)

def element_exsist_in_list(driver,by,elist):
    method = {
        'id':By.ID,
        'class':By.CLASS_NAME,
        'xpath':By.XPATH,
        'uiselector':MobileBy.ANDROID_UIAUTOMATOR,
        'name':By.NAME
    }
    if not method.has_key(by):
        print 'wrong location method!'
        return False

    for e in elist:
        try:
            el = driver.find_element(by= method.get(by),value=e)
            result = el
            break
        except NoSuchContextException:
            result = False
        except Exception:
            result = False
    return result



def element_exsist(driver,by,e,inclass = False,index = 0):
    method = {
        'id':By.ID,
        'class':By.CLASS_NAME,
        'xpath':By.XPATH,
        'uiselector':MobileBy.ANDROID_UIAUTOMATOR,
        'name':By.NAME
    }
    if not method.has_key(by):
        print 'wrong location method!'
        return False
    check_again = False
    if not inclass:
        try:
            driver.find_element(by= method.get(by),value=e)
            return True
        except NoSuchContextException:
            return False
        except Exception:
            return False
    else:
        classel =  driver.find_elements_by_class_name(inclass)[index]
        try:
            classel.find_element(by= method.get(by),value=e)
            check_again = True
        except NoSuchContextException:
            return False
        except Exception:
            return False
    if check_again:
        el = classel.find_element(by= method.get(by),value=e)
        return element2_in_element1(classel,el)


def get_element_postion(element):
    location = element.location
    size = element.size
    positonDic = {'start_x' : location["x"],'start_y':location["y"],'end_x':location["x"]+size["width"],'end_y':location["y"]+size["height"]}
    return positonDic

def element2_in_element1(el1,el2):
    el1_p_Dic = get_element_postion(el1)
    el2_p_Dic = get_element_postion(el2)
    x0 = el1_p_Dic['start_x']
    y0 = el1_p_Dic['start_y']
    x1 = el1_p_Dic['end_x']
    y1 = el1_p_Dic['end_y']
    a0 = el2_p_Dic['start_x']
    b0 = el2_p_Dic['start_y']
    a1 = el2_p_Dic['end_x']
    b1 = el2_p_Dic['end_y']
    if x0<=a0 and x1>=a1 and y0<=b0 and y1>=b1:
        return True
    else:
        return False

def element1_above_element2(el1,el2):
    el1_p_Dic = get_element_postion(el1)
    el2_p_Dic = get_element_postion(el2)
    if el1_p_Dic['end_y']<el2_p_Dic['start_y']:
        return True
    else:
        return False



def slide_up(driver,per=1,end = 3):
    """较大幅度全拼翻页可以使用per 6 end 2"""
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    start_y = y/10*(end+per)
    end_y = y/10*end
    # print start_y,end_y
    driver.swipe(x/2, start_y, x/2, end_y, 0)


def slide_down(driver,per=5,wait_time = 3):
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    driver.swipe(x/2, y/10*3, x/2, y/10*(3+per), 0)
    time.sleep(wait_time)


def slide_left(driver,startpoint = 3.8):
    """slide_left(driver,3.8)"""
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    driver.swipe(x/4*startpoint, y/2, x/4*0.5, y/2, 0)


def slide_right(driver):
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    driver.swipe(x/4*0.35, y/2, x/4*3.5, y/2, 0)


def press_back(driver):
    driver.press_keycode(4)

def exit_usercenter(driver):
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    position = [(x-10,y/2)]
    print position
    retry = 0
    while element_exsist(driver,'id',MY_COMM):
        if retry >= 10:
            print 'Error!'
            return False
        driver.tap(position)
        retry +=1
    return True


def start_to_index(driver,mode,method='all',first_start=False,cancel=True):
    if mode == 'mcp/plug/app':
        box = driver.find_elements_by_class_name('android.widget.CheckBox')
        if method == 'all':
            for i in box:
                i.click()
        driver.find_element_by_class_name('android.widget.Button').click()
    elif mode == 'mcp/dx':
        #print driver.current_activity
        sleep(10)
        if driver.current_activity == ACTIVITY.get('first_start'):
            for i in range(3):
                slide_left(driver)
                sleep(3)
            driver.find_element_by_id(WELCOME_START_BUTTON).click()
        if element_exsist(driver,'id',BUTTON_CANCEL) and cancel:
            print 'update exsist'
            driver.find_element_by_id(BUTTON_CANCEL).click()
            sleep(3)
        sleep(3)

def get_to_search(driver,mode):
    if mode == 'mcp/dx':
        slide_down(driver,5)
        for i in range(10):

            slide_down(driver, 1.0+0.3*i)
            time.sleep(1)
            try:
                driver.find_element_by_id('com.zc.hubei_news:id/ll_search').click()
                return True
            except Exception,e:
                pass
        return False
    if mode == 'mcp/plug/app':
        driver.find_element_by_id(SEARCH_BUTTON)

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

def seach_by_ui(driver,title,postion = search_postion):
    product = get_product_name()

    if postion.has_key(product):
        postion = postion.get(product)
    else:
        postion = postion.get('default')
    result = False
    try:
        el = driver.find_element_by_id('com.zc.hubei_news:id/et_search')
        el.send_keys(title)
        a = driver.available_ime_engines
        driver.activate_ime_engine(a[0])
        el.click()
        driver.tap([postion])
        driver.activate_ime_engine(a[-1])
        result = True
    except Exception,e:
        print e.__repr__()
        result = False
    finally:
        return result


def get_to_article_by_search(driver,title,mode,postion = search_postion):
    result = False
    try:
        title = title.decode('utf-8')
    except:
        pass
    try:
        assert get_to_search(driver,mode)
        seach_by_ui(driver,title,postion)
        driver.find_element_by_id('com.zc.hubei_news:id/item_layout').click()
        result = True
    except Exception,e:
        print sys._getframe().f_code.co_name
        print e.__repr__()
        result = False
    finally:
        return  result

def refresh_article(driver):
    back(driver)
    time.sleep(3)
    driver.find_element_by_id('com.zc.hubei_news:id/item_layout').click()



def login(driver,mode,package,phone,tid=DEVICE_TID,in_page = False):
    from adb import get_config_by_adb
    if not in_page:
        driver.find_element_by_id(MENU_ICON).click()
        driver.find_element_by_id(PHONE_LOGIN_ICON).click()
    driver.find_element_by_id(PHONE_INPUT).send_keys(phone)
    driver.find_element_by_id(GET_VCODE).click()
    time.sleep(5)
    r = RedisHandler()
    if is_root:
        dc = get_config_by_adb(package)['dc']
        vcode = r.get_vcode_by_dc(phone,dc,tid)
    else:
        vcode = r.get_latest_vcode(phone)
        print vcode
    if vcode:
        driver.find_element_by_id(VCODE_INPUT).send_keys(vcode)
        driver.find_element_by_id(PHONE_LOGIN_BUTTON).click()
        return True
    else:
        return False

def login_to_index(driver,mode,package,phone,tid=DEVICE_TID,in_page = False):
    assert login(driver,mode,package,phone,tid,in_page)
    time.sleep(2)
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    position = [(x-10,y/2)]
    print position
    retry = 0
    while element_exsist(driver,'id',MY_COMM):
        if retry >= 10:
            print 'Error!'
            return False
        driver.tap(position)
        retry +=1
    return True

def BeLogin(driver):
    login_state = is_login(driver)
    if not login_state:
        phone_number = '134'+str(randint(10000000,99999999))
        print phone_number
        loginresult = login_to_index(driver,MODE,desired_caps['appPackage'],phone_number,in_page = False)
        if loginresult:
            print u'登录成功!'
            return True
        else:
            print u'FAIL!!!------------->登录失败'
            return False
    else:
        return True

def logout(driver,mode):
    if mode == 'mcp/dx':
        try:
            driver.find_element_by_id(MENU_ICON).click()
            driver.find_element_by_id(USER_ICON).click()
            driver.find_element_by_id(LOGOUT_BUTTON).click()
            driver.find_element_by_android_uiautomator('new UiSelector().text(\"登出\")').click()
            return True
        except Exception,e:
            print sys._getframe().f_code.co_name
            print e.__repr__()
            return False


def logout_to_index(driver,mode):
    try:
        assert logout(driver,mode)
        time.sleep(2)
        x = driver.get_window_size()['width']
        y = driver.get_window_size()['height']
        position = [(x-10,y/2)]
        print position
        retry = 0
        while element_exsist(driver,'id',MY_COMM):
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
def seekbar_sendkey(driver,per):
    el = driver.find_element_by_id(AUDIO_PROGRESS)
    position = el.location
    size = el.size
    point ={
               'x':position['x'],
               'y':position['y']+size['height']/2,
               'length':size['width']
    }
    end_point =[(point['x']+per*point['length'],point['y'])]
    #拖动实现效果较差，改为点击
    #driver.swipe(point['x'],point['y'],point['x']+per*point['length'],point['y'],1000)
    driver.tap(end_point)
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
    pause_image = IMAGE_PATH + '\\'+IMAGES['notification_pause']
    start_image = IMAGE_PATH + '\\'+IMAGES['notification_start']
    status_dict = {
        'play': start_image,
        'pause': pause_image
    }
    scr = Appium_Extend(driver)
    el = driver.find_element_by_id(NOTIFICATION_AUDIO_PLAY)
    scr.get_screenshot_by_element(el,fname)
    return scr.same_as(fname,status_dict.get(status))

@exception_handler
def clear_notification(driver):
    open_notifications(driver)
    sleep(WAIT_TIME)
    try:
        driver.find_element_by_id(NOTIFICATION_CLEAR_BUTTON).click()
    except:
        print 'no el find'
    close_notification(driver)


def close_notification(driver):
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    driver.swipe(x/2, y*9/10,2/x,y/10)


def click_center(driver):
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    driver.tap([(x/2, y/2)])

def click_right_side(driver):
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    driver.tap([(x-2, y/2)])

def tap_center(driver):
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    driver.tap([(x/2, y/2)])

def is_login(driver):
    result = False
    if is_root == True:
        return check_login_status()
    elif is_root == False:
        driver.find_element_by_id(MENU_ICON).click()
        if element_exsist(driver,'id',PHONE_LOGIN_ICON):
            result = False
        elif element_exsist(driver,'id',PHONE_LOGIN_ICON) == False and element_exsist(driver,'id',USER_ICON):
            result = True
    click_right_side(driver)
    sleep(WAIT_TIME)
    return result

def open_notifications(driver,wait=2):
    driver.open_notifications()
    sleep(wait)
    if element_exsist(driver,'id',XIAOMI_SETTINGS):
        print 'notification'
        slide_right(driver)
        sleep(wait)

def find_element_by_name_like(driver,element,name):
    elements = driver.find_elements_by_id(element)
    for el in elements:
        txt = el.text
        if name in txt:
            return el
    return False

def get_user_name(driver):
    driver.find_element_by_name(NEWSTABTXT).click()
    driver.find_element_by_id(MENU_ICON).click()
    user_name = driver.find_element_by_id(USER_NAME).text
    click_right_side(driver)
    sleep(WAIT_TIME)
    return user_name

def clean_image_save_dir():
    image_save_path = 'sdcard/'+IMAGE_SAVE_DIR
    cmd = 'adb shell "rm ' + image_save_path+'/*"'
    os.popen(cmd)
    p = ls(image_save_path)
    count = p.count("\n")
    if count == 2:
        print u'SUCCESS!!!---------->清空图片下载文件夹图片存储目录成功'
        return True
    else:
        print u'FAIL!!!--------->清空图片下载文件夹图片存储目录失败'
        return False