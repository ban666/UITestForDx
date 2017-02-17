# -*- coding: utf-8 -*-
__author__ = 'liaoben'

from appium import webdriver
import time,sys
from elements_id import *
from elements_id import COMMENT_ITEM
from appium_lib import *

def send_comment(driver,content,input_button=COMMENT_INPUT_BUTTON):
    try:
        content = content.decode('utf-8')
    except:
        pass

    input = driver.find_element(*input_button)
    position = get_el_center(input)
    driver.tap([position])
    sleep(3)
    driver.find_element(*COMMENT_INPUT_EDIT).send_keys(content)
    driver.find_element(*COMMENT_SEND_OK).click()
    sleep(5)


def get_click_location(driver,cell,view,frame_size = (261,50)):
    windows_size = driver.get_window_size()
    cell_origin = cell.location
    cell_size = cell.size
    view_origin = view.location
    view_size = view.size
    #print view_origin,cell_origin
    if cell_origin['y']-view_origin['y']>frame_size[1]:
        #print 'above'
        frame_location = ((windows_size['width']-frame_size[0])/2,cell_origin['y']-frame_size[1])
        #print frame_location
    else:
        #print 'below'
        frame_location = ((windows_size['width']-frame_size[0])/2,cell_origin['y']+cell_size['height'])
    click = range(3)
    #support reply copy
    click[0] = (frame_location[0]+frame_size[0]*1/6,frame_location[1]+frame_size[1]/2)
    click[1] = (frame_location[0]+frame_size[0]*3/6,frame_location[1]+frame_size[1]/2)
    click[2] = (frame_location[0]+frame_size[0]*5/6,frame_location[1]+frame_size[1]/2)
    return click


def judge_comment_type(comment):
    texts =  comment.find_elements_by_class_name('UIAStaticText')
    if len(texts) == 4:
        return 1
    elif len(texts) == 6:
        return 2


def comment_handle(driver,index,method,quote=False,content=''):
    comment = COMMENT_ITEM[1] % (index)
    cell = driver.find_element(COMMENT_ITEM[0],comment)
    comment_type = judge_comment_type(cell)
    view = driver.find_element(*COMMENT_VIEW)
    method_dict = {
        'support':0,
        'reply':1,
        'copy':2,
    }
    if method == 'digg':
        driver.find_element_by_xpath(comment+COMMENT_DICT[comment_type]['digg_button'][1]).click()
        return
    if quote:
        quote_item = driver.find_element_by_xpath(comment+COMMENT_DICT[comment_type]['quote_button'][1])
        driver.find_element_by_xpath(comment+COMMENT_DICT[comment_type]['quote_button'][1]).click()
        position = get_click_location(driver,quote_item,view)
        if method!='reply':
            driver.tap([position[method_dict[method]]])
        elif method == 'reply':
            driver.tap([position[method_dict[method]]])
            driver.find_element(*COMMENT_INPUT_EDIT).send_keys(content)
            driver.find_element(*COMMENT_SEND_OK).click()
            sleep(WAIT_TIME)
    else:
        driver.find_element_by_xpath(comment+COMMENT_DICT[comment_type]['content'][1]).click()
        position = get_click_location(driver,cell,view)
        if method!='reply':
            driver.tap([position[method_dict[method]]])
        elif method == 'reply':
            driver.tap([position[method_dict[method]]])
            sleep(3)
            driver.find_element(*COMMENT_INPUT_EDIT).send_keys(content)
            driver.find_element(*COMMENT_SEND_OK).click()
            sleep(WAIT_TIME)


def get_comment_info(driver,index,mycomment=False,reply=False):
    comm_item = COMMENT_ITEM
    comm_dict = COMMENT_DICT
    if mycomment:
        comm_item = MY_COMMENT_PUBLISH_ITEM
        comm_dict = MY_COMMENT_DICT
        if reply:
            comm_item = MY_COMMENT_REPLY_ITEM
    comment = comm_item[1] % (index)
    cell = driver.find_element(COMMENT_ITEM[0],comment)
    comment_type = judge_comment_type(cell)
    ret = {}
    if comment_type == 1:
        #'content''author''loc_time''digg_count'
        keys = comm_dict[comment_type].keys()
        keys.pop(keys.index('digg_button'))
        for key in keys:
            ret[key] = driver.find_element_by_xpath(comment+comm_dict[comment_type][key][1]).text
    if comment_type == 2:
        #'content''author''loc_time''digg_count''quote_author_loc''quote_content'
        keys = comm_dict[comment_type].keys()
        keys.pop(keys.index('digg_button'))
        keys.pop(keys.index('quote_button'))
        for key in keys:
            ret[key] = driver.find_element_by_xpath(comment+comm_dict[comment_type][key][1]).text
    return ret

def check_comment(driver,comment):
    result = -1
    elements = [DIGG_COUNT,DIGG_BUTTON,LOC_TIME,COMMENT_ICON,COMMENT_NAME,COMMENT_TEXT]
    try:
        for ele in elements:
            comment.find_element_by_id(ele)
        result = 1
    except Exception as e:
        print 'check_comment_error:',e
        result = 0
    finally:
        return result


def check_copy_content(driver, content, input_button=COMMENT_INPUT_BUTTON):
    try:
        content = content.decode('utf-8')
    except:
        pass
    input = driver.find_element(*input_button)
    position = get_el_center(input)
    driver.tap([position])
    sleep(3)
    input_edit = driver.find_element(*COMMENT_INPUT_EDIT)
    center = get_el_center(input_edit)
    driver.tap([center],3000)
    driver.find_element_by_id(u'粘贴').click()
    t = driver.find_element(*COMMENT_INPUT_EDIT).text
    driver.find_element(*COMMENT_SEND_CANCEL).click()
    return t == content


def check_copy_content_by_reply(driver,content):
    driver.find_element_by_id(COMMENT).click()
    driver.find_element_by_id(REPLY_BUTTON).click()
    paste(driver)
    t = driver.find_element_by_id(COMMENT_EDIT_TEXT).text
    driver.find_element_by_id(COMMENT_SEND_CANCEL).click()
    return t == content



def send_comment_with_input(driver,content):
    result = -1
    try:
        content = content.decode('utf-8')
    except:
        pass
    try:
        input = driver.available_ime_engines

        el = driver.find_element_by_id(COMMENT_INPUT)
        el.send_keys(content)
        driver.activate_ime_engine(input[0])
        el.click()
        driver.find_element_by_id(COMMENT_SENT_BUTTON).click()
        driver.activate_ime_engine(input[-1])
        result = 1
    except Exception as e:
        print 'send_comment_error:',e
        result = 0
    finally:
        return result

def reply_comment(driver,comment,content):
    result = -1
    try:
        driver.find_element_by_id(comment).click()
        driver.find_element_by_id(REPLY_BUTTON).click()
        if element_exsist(driver,'id',COMMENT_INPUT):
            pass
            driver.find_element_by_id(COMMENT_INPUT).send_keys(content)
            driver.find_element_by_id(COMMENT_SENT_BUTTON).click()
            result = 1
        elif element_exsist(driver,'id',COMMENT_EDIT_TEXT):
            driver.find_element_by_id(COMMENT_EDIT_TEXT).send_keys(content)
            driver.find_element_by_id(COMMENT_SEND_OK).click()
            result = 1
    except Exception as e:
        print 'send_comment_error:',e
        result = 0
    finally:
        return result

def find_first_comment_and_support(driver, option=0):
    result = -1
    try:
        driver.find_elements_by_id(COMMENT_TEXT)[int(option)].click()
        if element_exsist(driver,'id',SUPPORT_BUTTON):
            support = SUPPORT_BUTTON
        else:
            support = MY_COMM_SUPPORT_BUTTON
        driver.find_element_by_id(support).click()
        result = 1
    except Exception as e:
        print 'send_comment_error:',e
        result = 0
    finally:
        return result

def find_first_comment_and_reply(driver,content,option=0):
    result = -1
    try:
        content = content.decode('utf-8')
    except:
        pass
    try:
        driver.find_elements_by_id(COMMENT_TEXT)[int(option)].click()
        driver.find_element_by_id(REPLY_BUTTON).click()
        if element_exsist(driver,'id',COMMENT_INPUT):
            driver.find_element_by_id(COMMENT_INPUT).send_keys(content)
            driver.find_element_by_id(COMMENT_SENT_BUTTON).click()
            result = 1
        elif element_exsist(driver,'id',COMMENT_EDIT_TEXT):
            driver.find_element_by_id(COMMENT_EDIT_TEXT).send_keys(content)
            driver.find_element_by_id(COMMENT_SEND_OK).click()
            result = 1
    except Exception as e:
        print 'send_comment_error:',e
        result = 0
    finally:
        return result

def find_first_comment_and_copy(driver,option=0):
    result = -1
    try:
        driver.find_elements_by_id(COMMENT_TEXT)[int(option)].click()
        driver.find_element_by_id(COPY_BUTTON).click()
        result = 1
    except Exception as e:
        print 'send_comment_error:',e
        result = 0
    finally:
        return result


def check_reply_comment(driver, comment):
    result = -1
    elements = [DIGG_COUNT,DIGG_BUTTON,LOC_TIME,COMMENT_ICON,COMMENT_NAME,COMMENT_TEXT,QUOTE_COMMENT,QUOTE_NAME]
    try:
        for ele in elements:
            comment.find_element_by_id(ele)
        result = 1
    except Exception as e:
        print 'check_comment_error:',e
        result = 0
    finally:
        return result

def my_comment_handle(driver,index,method,quote=False,content='',reply=False):
    COMMENT_ITEM = MY_COMMENT_PUBLISH_ITEM
    if reply:
        COMMENT_ITEM = MY_COMMENT_REPLY_ITEM
    comment = COMMENT_ITEM[1] % (index)
    cell = driver.find_element('xpath',comment)
    comment_type = judge_comment_type(cell)
    view = driver.find_element(*MY_COMMENT_VIEW)
    method_dict = {
        'support':0,
        'reply':1,
        'copy':2,
    }
    if method == 'digg':
        driver.find_element_by_xpath(comment+MY_COMMENT_DICT[comment_type]['digg_button'][1]).click()
        return
    if quote:
        quote_content = driver.find_element_by_xpath(comment+MY_COMMENT_DICT[comment_type]['quote_content'][1])
        quote_loc_author = driver.find_element_by_xpath(comment+MY_COMMENT_DICT[comment_type]['quote_author_loc'][1])
        driver.find_element_by_xpath(comment+MY_COMMENT_DICT[comment_type]['quote_button'][1]).click()
        position = get_click_location_for_mycomm_quote(driver,quote_content,quote_loc_author,view)
        if method!='reply':
            driver.tap([position[method_dict[method]]])
        elif method == 'reply':
            driver.tap([position[method_dict[method]]])
            driver.find_element(*COMMENT_INPUT_EDIT).send_keys(content)
            driver.find_element(*COMMENT_SEND_OK).click()
            sleep(WAIT_TIME)
    else:
        driver.find_element_by_xpath(comment+MY_COMMENT_DICT[comment_type]['content'][1]).click()
        position = get_click_location(driver,cell,view)
        if method!='reply':
            driver.tap([position[method_dict[method]]])
        elif method == 'reply':
            driver.tap([position[method_dict[method]]])
            driver.find_element(*COMMENT_INPUT_EDIT).send_keys(content)
            driver.find_element(*COMMENT_SEND_OK).click()
            sleep(WAIT_TIME)

def check_copy_content_in_my_comm(driver,content,reply=False):
    COMMENT_ITEM = MY_COMMENT_PUBLISH_ITEM
    if reply:
        COMMENT_ITEM = MY_COMMENT_REPLY_ITEM
    comment = COMMENT_ITEM[1] % (1)
    cell = driver.find_element('xpath',comment)
    comment_type = judge_comment_type(cell)
    view = driver.find_element(*MY_COMMENT_VIEW)
    driver.find_element_by_xpath(comment+MY_COMMENT_DICT[comment_type]['content'][1]).click()
    position = get_click_location(driver,cell,view)
    driver.tap([position[1]])

    input_edit = driver.find_element(*COMMENT_INPUT_EDIT)
    center = get_el_center(input_edit)
    driver.tap([center],3000)
    driver.find_element_by_id(u'粘贴').click()
    t = driver.find_element(*COMMENT_INPUT_EDIT).text
    driver.find_element(*COMMENT_SEND_CANCEL).click()
    return t == content


def get_click_location_for_mycomm_quote(driver,content,author,view,frame_size = (261,50)):
    windows_size = driver.get_window_size()
    cell_origin = author.location
    view_origin = view.location
    view_size = view.size
    #print view_origin,cell_origin
    if cell_origin['y']-view_origin['y']>frame_size[1]:
        #print 'above'
        frame_location = ((windows_size['width']-frame_size[0])/2,cell_origin['y']-frame_size[1])
        #print frame_location
    else:
        #print 'below'
        frame_location = ((windows_size['width']-frame_size[0])/2,content.location['y']+content.size['height'])
    click = range(3)
    #support reply copy
    click[0] = (frame_location[0]+frame_size[0]*1/6,frame_location[1]+frame_size[1]/2)
    click[1] = (frame_location[0]+frame_size[0]*3/6,frame_location[1]+frame_size[1]/2)
    click[2] = (frame_location[0]+frame_size[0]*5/6,frame_location[1]+frame_size[1]/2)
    #print click
    return click


def click_comment_src(driver,index,reply=False):
    COMMENT_ITEM = MY_COMMENT_PUBLISH_ITEM
    if reply:
        COMMENT_ITEM = MY_COMMENT_REPLY_ITEM
    comment = COMMENT_ITEM[1] % (index)
    cell = driver.find_element('xpath',comment)
    comment_type = judge_comment_type(cell)
    driver.find_element_by_xpath(comment+MY_COMMENT_DICT[comment_type]['article_link'][1]).click()

if __name__ == '__main__':
    pass