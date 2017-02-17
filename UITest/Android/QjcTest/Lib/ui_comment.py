# -*- coding: utf-8 -*-
__author__ = 'liaoben'

from appium import webdriver
import time,sys
from elements_id_plug import *
from appium_lib import *

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


def check_copy_content(driver, content):
    input_id = COMMENT_INPUT
    driver.find_element_by_id(input_id).click()
    paste(driver)
    el = driver.find_element_by_id(COMMENT_INPUT)
    t = el.text
    el.clear()
    return t == content


def check_copy_content_by_reply(driver,content):
    driver.find_element_by_id(COMMENT).click()
    driver.find_element_by_id(REPLY_BUTTON).click()
    paste(driver)
    t = driver.find_element_by_id(COMMENT_EDIT_TEXT).text
    driver.find_element_by_id(COMMENT_SEND_CANCEL).click()
    return t == content


def send_comment(driver,content,in_page=True):
    result = -1
    try:
        content = content.decode('utf-8')
    except:
        pass
    try:
        #driver.find_element_by_id(COMMENT_INPUT).click()
        driver.find_element_by_id(COMMENT_INPUT).send_keys(content)
        driver.find_element_by_id(COMMENT_SENT_BUTTON).click()
        result = 1
    except Exception as e:
        print 'send_comment_error:',e
        result = 0
    finally:
        return result

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
        driver.press_keycode(84)
        driver.activate_ime_engine(input[-1])
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


def reply_comment(driver,comment,content):
    result = -1
    try:
        driver.find_element_by_id(comment).click()
        driver.find_element_by_id(REPLY_BUTTON).click()
        driver.find_element_by_id(COMMENT_INPUT).send_keys(content)
        driver.find_element_by_id(COMMENT_SENT_BUTTON).click()
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
        driver.find_element_by_id(SUPPORT_BUTTON).click()
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
        driver.find_element_by_id(COMMENT_INPUT).send_keys(content)
        driver.find_element_by_id(COMMENT_SENT_BUTTON).click()
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



def get_comment_info(driver,comment,option=0):
    """
    获取评论详情
    :param driver:
    :param comment:
    :return:[点赞次数，地理位置_时间，评论用户名，评论内容，引用用户名，引用评论详情]
    """
    result = -1
    elements = [DIGG_COUNT,LOC_TIME,COMMENT_NAME]
    ret = []
    try:
        for ele in elements:
            ret.append(comment.find_element_by_id(ele).text)
        texts = comment.find_elements_by_id(COMMENT_TEXT)
        if int(option) == 0:
            ret.extend([texts[0].text,'',''])
        elif int(option) == 1:
            quote_name = comment.find_element_by_id(QUOTE_NAME).text
            quote_text = texts[0].text
            comment_text = texts[1].text
            ret.extend([comment_text,quote_name,quote_text])
        else:
            raise
        result = ret
    except Exception as e:
        print 'check_comment_error:',e
        result = 0
    finally:
        return result


if __name__ == '__main__':
    pass