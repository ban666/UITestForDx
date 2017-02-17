# -*- coding: utf-8 -*-
__author__ = 'liaoben'

from appium import webdriver
import time,sys
from elements_id_plug import *

comment = 'com.cnhubei.dxxwhw:id/rl_comment'
digg_count = 'com.cnhubei.dxxwhw:id/tv_digg'
digg_button = 'com.cnhubei.dxxwhw:id/iv_common_zan'
loc_time = 'com.cnhubei.dxxwhw:id/tv_loc_time'
quote_comment = 'com.cnhubei.dxxwhw:id/ll_quote'
quote_name = 'com.cnhubei.dxxwhw:id/tv_quote_uname'
comment_icon = 'com.cnhubei.dxxwhw:id/civ_uicon'
comment_name = 'com.cnhubei.dxxwhw:id/tv_uname'
comment_text = 'com.cnhubei.dxxwhw:id/expandable_text'
comment_input = 'com.cnhubei.dxxwhw:id/comment_content_edt'
comment_sent_button = 'com.cnhubei.dxxwhw:id/comment_send_text'
comment_count = 'com.cnhubei.dxxwhw:id/comment_number_text'

support_button = 'com.cnhubei.dxxwhw:id/ll_pop_support'
reply_button = 'com.cnhubei.dxxwhw:id/ll_pop_reply'
copy_button = 'com.cnhubei.dxxwhw:id/ll_pop_copy'


class CommentHandler(object):

    def __init__(self,driver,mode):
        self.driver = driver
        self.mode = mode
def check_comment(driver,mode,comment):
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