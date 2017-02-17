# -*- coding: utf-8 -*-
__author__ = 'liaoben'

from appium import webdriver
from time import sleep
import sys
sys.path.append('../../Lib')
from appium_lib import *
from config import *
success = True

desired_caps={
    'app': 'com.cnhubei.ycdx',
    'udid':'16f8e9bde0d805ab524a9db4d79fb63e79b26015',
    'platformName': 'iOS',
    'platformVersion': '8.3',
    'deviceName': 'iPhone 6',
    'appium-version':'1.0',
    'unicodeKeyboard':True,
    'resetKeyboard':True
}
driver =webdriver.Remote('http://10.99.13.46:4723/wd/hub',desired_caps)
driver.implicitly_wait(60)
#print driver.current_activity
# driver.find_element_by_id("ic sousuo white").click()
# #driver.open_notifications()
# driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIASearchBar[1]').send_keys(u'自动化音频新闻')
# sleep(5)
# driver.find_element_by_id(u"搜索").click()
# sleep(5)
#
# driver.find_element_by_id(u'自动化音频新闻').click()
# sleep(5)
#
# #jump to comment page
# driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIAButton[2]').click()
# sleep(5)
#
# #click comment input butoon
# driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIAButton[2]').click()
# sleep(5)
#
# #click comment input butoon
# driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIATextView[1]').send_keys(u'自动化音频新闻')
# sleep(5)
#
# driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIAButton[3]').click()
# sleep(5)

COMMENT_ENTRANCE = ('id','btn news coments visited1')
COMMENT_ENTRANCE_AUDIO = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIAButton[2]')
COMMENT_INPUT_BUTTON = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIAButton[2]')
COMMENT_INPUT_EDIT = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIATextView[1]')
COMMENT_SEND_CANCEL = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIAButton[2]')
COMMENT_SEND_OK = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIAButton[3]')
COMMENT_ITEM = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[%d]')
COMMENT_VIEW = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIATableView[1]')

COMMENT_DICT = {
    2:#嵌套评论
        {
            'content':('xpath','/UIAStaticText[3]'),
            'author':('xpath','/UIAStaticText[1]'),
            'loc_time':('xpath','/UIAStaticText[2]'),
            'digg_count':('xpath','/UIAStaticText[4]'),
            'quote_author_loc':('xpath','/UIAStaticText[5]'),
            'quote_content':('xpath','/UIAStaticText[6]'),
            'quote_button':('xpath','/UIAButton[1]'),
            'digg_button':('xpath','/UIAButton[2]'),

        },
    1:#非嵌套评论
        {
            'author':('xpath','/UIAStaticText[1]'),
            'loc_time':('xpath','/UIAStaticText[2]'),
            'content':('xpath','/UIAStaticText[3]'),
            'digg_count':('xpath','/UIAStaticText[4]'),
            'digg_button':('xpath','/UIAButton[1]'),
        }
}


def get_to_comment(driver,entrance=COMMENT_ENTRANCE):
    driver.find_element(*entrance).click()

def send_comment(driver,content,input_button=COMMENT_INPUT_BUTTON):
    try:
        content = content.decode('utf-8')
    except:
        pass
    driver.find_element(*input_button).click()
    driver.find_element(*COMMENT_INPUT_EDIT).send_keys(content)
    sleep(5)
    driver.find_element(*COMMENT_SEND_OK).click()
    sleep(5)
# sleep(5)

def get_click_location(cell,view,frame_size = (261,50)):
    windows_size = driver.get_window_size()
    cell_origin = cell.location
    cell_size = cell.size
    view_origin = view.location
    view_size = view.size
    print view_origin,cell_origin
    if cell_origin['y']-view_origin['y']>frame_size[1]:
        print 'above'
        frame_location = ((windows_size['width']-frame_size[0])/2,cell_origin['y']-frame_size[1])
        print frame_location
    else:
        print 'below'
        frame_location = ((windows_size['width']-frame_size[0])/2,cell_origin['y']+cell_size['height'])
    click = range(3)
    #support reply copy
    click[0] = (frame_location[0]+frame_size[0]*1/6,frame_location[1]+frame_size[1]/2)
    click[1] = (frame_location[0]+frame_size[0]*3/6,frame_location[1]+frame_size[1]/2)
    click[2] = (frame_location[0]+frame_size[0]*5/6,frame_location[1]+frame_size[1]/2)
    return click


def judge_comment_type(comment):
    buttons =  comment.find_elements_by_class_name('UIAButton')
    return len(buttons)


def comment_handle(driver,index,method,quote=False,content=''):
    comment = COMMENT_ITEM[1] % (index)
    cell = driver.find_element(COMMENT_ITEM[0],comment)
    comment_type = judge_comment_type(cell)
    view = driver.find_element(*COMMENT_VIEW)
    method_dict = {
        'support':0,
        'reply':1,
        'copy':2
    }
    if quote:
        quote_item = driver.find_element_by_xpath(comment+COMMENT_DICT[comment_type]['quote_button'][1])
        driver.find_element_by_xpath(comment+COMMENT_DICT[comment_type]['quote_button'][1]).click()
        position = get_click_location(quote_item,view)
        if method!='reply':
            driver.tap([position[method_dict[method]]])
        elif method == 'reply':
            driver.tap([position[method_dict[method]]])
            driver.find_element(*COMMENT_INPUT_EDIT).send_keys(content)
            driver.find_element(*COMMENT_SEND_OK).click()
            sleep(WAIT_TIME)
    else:
        driver.find_element_by_xpath(comment+COMMENT_DICT[comment_type]['content'][1]).click()
        position = get_click_location(cell,view)
        if method!='reply':
            driver.tap([position[method_dict[method]]])
        elif method == 'reply':
            driver.tap([position[method_dict[method]]])
            driver.find_element(*COMMENT_INPUT_EDIT).send_keys(content)
            driver.find_element(*COMMENT_SEND_OK).click()
            sleep(WAIT_TIME)


def get_comment_info(driver,index):
    comment = COMMENT_ITEM[1] % (index)
    cell = driver.find_element(COMMENT_ITEM[0],comment)
    comment_type = judge_comment_type(cell)
    ret = {}
    if comment_type == 1:
        #'content''author''loc_time''digg_count'
        keys = COMMENT_DICT[comment_type].keys()
        keys.pop(keys.index('digg_button'))
        for key in keys:
            ret[key] = driver.find_element_by_xpath(comment+COMMENT_DICT[comment_type][key][1]).text
    if comment_type == 2:
        #'content''author''loc_time''digg_count''quote_author_loc''quote_content'
        keys = COMMENT_DICT[comment_type].keys()
        keys.pop(keys.index('digg_button'))
        keys.pop(keys.index('quote_button'))
        for key in keys:
            ret[key] = driver.find_element_by_xpath(comment+COMMENT_DICT[comment_type][key][1]).text
    return ret




get_to_article_by_search(driver,u'自动化状态测试')
#print driver.contexts
#driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIAButton[2]').click()
get_to_comment(driver)
sleep(5)
print get_comment_info(driver,1)
print get_comment_info(driver,2)
sleep(10)
#comment_handle(driver,1,'reply',content=u'中文',quote=False)
#driver.quit()
#send_comment(driver,'123')

# #wu qiantao
# cell = driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[1]')
# buttons =  cell.find_elements_by_class_name('UIAButton')
# print 'buttons,len',len(buttons)
# if len(buttons) == 2:
#     comment_type = 2
# else:
#     comment_type =1
# cell_origin = cell.location
# cell_size = cell.size
# view = driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIATableView[1]')
# view_origin = view.location
# view_size = view.size
# frame_size = (261,50)
# driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[1]/UIAStaticText[1]').click()



# #qiantao
#
# if view_origin['y']-cell_origin['y']>frame_size[1]:
#     click_l = get_click_location(cell,view,'above')
# else:
#     click_l =  get_click_location(cell,view,'below')
# click_l = get_click_location(cell,view)
# driver.tap([click_l[0]])
# sleep(5)
# driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[1]/UIAStaticText[1]').click()
# sleep(1)
# driver.tap([click_l[2]])
# driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[1]/UIAStaticText[1]').click()
# sleep(1)
# driver.tap([click_l[1]])
# sleep(5)

sleep(10)

