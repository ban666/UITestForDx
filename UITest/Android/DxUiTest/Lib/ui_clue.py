# -*- coding: utf-8 -*-
__author__ = 'ld'

from appium import webdriver
import sys
from elements_id import *
from appium_lib import *
from common import exception_handler
from time import sleep
from screenshot import Appium_Extend
import re
from ui_search import *
from elements_id import *
from config import *
import os



#进入报料界面
def go_to_clue(driver):
    driver.find_element_by_id(HEAD).click()
    sleep(WAIT_TIME)
    return True

def go_to_myclue(driver):
    not_in_page = element_exsist(driver,'id',MENU_ICON)
    if not_in_page:
        driver.find_element_by_id(MENU_ICON).click()
        sleep(1)
    driver.find_element_by_name('我的爆料').click()

def check_my_clue(driver,extend,db,cluetestDic,state):
    """state：30 审核通过，10 未审核，3 审核不通过"""
    false_count = 0
    if not element_exsist(driver,'name','评论') and not element_exsist(driver,'name','赞'):
        print u'没有显示评论和点赞按钮'
    else:
        false_count += 1
        print u'FAIL!!!------------------》显示了评论点赞按钮'
    content = cluetestDic.get('content')
    image_num = cluetestDic.get('image_num')
    username = cluetestDic.get('username')
    no_pass_reason = db.get_clue_with_content_by_db(content)['remark'].decode('utf-8')
    show_reason = element_exsist(driver,'id',CLUE_REASON_NOPASS,LISTLAYOUT,3)
    state_text = driver.find_elements_by_class_name(LISTLAYOUT)[3].find_element_by_id(CLUE_REVIEW_STATE).text
    if state == 30 :
        if not show_reason and state_text == u'审核通过':
            print u'审核结果校验正确'
        else:
            false_count += 1
            print u'FAIL!!!-------------------》审核结果校验失败!'
        driver.find_elements_by_class_name(LISTLAYOUT)[3].find_element_by_id(HEAD_CONTENT).click()
        sleep(WAIT_TIME)
        el_bar = driver.find_element_by_id(TOP_BAR)
        if el_bar.text==u"爆料正文":
            print u'审核通过爆料可点击进入报料详情页'
            driver.press_keycode(4)
            if el_bar.text!=u"我的爆料":
                print u'FAIL!!!-------------------》返回报料列表失败'
                false_count += 1
        else:
            print u'FAIL!!!-------------------》审核通过爆料点击进入报料详情失败'
            false_count += 1
    elif state == 10 :
        if not show_reason and state_text == u'未审核':
            print u'审核结果校验正确'
        else:
            false_count += 1
            print u'FAIL!!!-------------------》审核结果校验失败'
        driver.find_elements_by_class_name(LISTLAYOUT)[3].find_element_by_id(HEAD_CONTENT).click()
        sleep(WAIT_TIME)
        el_bar = driver.find_element_by_id(TOP_BAR)
        print el_bar.text
        if el_bar.text!=u'我的爆料':
            print u'FAIL!!!---------------------》未审核爆料不应该能够点击进入报料正文'
            false_count += 1
        else:
            print u'未审核报料无法点击进入详情正确'

    elif state == 3 :
        clue_reason_nopass_text = driver.find_elements_by_class_name(LISTLAYOUT)[3].find_element_by_id(CLUE_REASON_NOPASS).text
        expect_text =  u'未通过原因：' + no_pass_reason
        if clue_reason_nopass_text == expect_text and state_text == u'审核未通过':
            print u'审核结果校验正确'
        else:
            false_count += 1
            print u'FAIL!!!-------------------》审核结果校验失败'
        driver.find_elements_by_class_name(LISTLAYOUT)[3].find_element_by_id(HEAD_CONTENT).click()
        sleep(WAIT_TIME)
        el_bar = driver.find_element_by_id(TOP_BAR)
        if el_bar.text!=u"我的爆料":
            print u'FAIL!!!---------------------》审核不通过爆料不应该能够点击进入报料正文'
            false_count += 1
        else:
            print u'审核不通过报料无法点击进入详情正确'
    else:
        print u'ERROR!---------------------》state传值错误'
    if not check_clue_without_type(driver,extend,cluetestDic):
        print u'FAIL!!!-------------------》报料内容校验失败'
        false_count += 1
    if image_num:
        if not check_clue_images_view(driver,username,image_num):
            print u'FAIL!!!-------------------》报料图片浏览校验失败'
            false_count += 1
        else:
            print u'图片浏览校验成功'
    if not false_count:
        return True
    else:
        return False

def check_clue_images_view(driver,username,image_num = 9,inclass = LISTLAYOUT):
    print 'testing for images view'
    false_count = 0
    page_contain_image = element_exsist(driver,'id',HEAD_PIC)
    if page_contain_image:
        pic_el = driver.find_element_by_id(HEAD_PIC)
        loc_el = driver.find_element_by_id(CLUE_TIME)
        is_contain_image = elment1_above_elment2(pic_el,loc_el)
    if not image_num:
        if is_contain_image:
            return False
    else:
        images_moudle = driver.find_element_by_class_name(inclass).find_element_by_id(HEAD_PIC)
        images =images_moudle.find_elements_by_class_name(IMAGEVIEW)
        num = len(images)
        if num!=image_num:
            false_count+=1
        images[0].click()
        if not element_exsist(driver,'id',PV_IMAGE):
            return False
        if driver.find_element_by_id(CLUE_IMAGE_NUM).text!='1/'+str(num) or driver.find_element_by_id(CLUE_IMAGE_TITLE).text != username:
            false_count += 1
        slide_left(driver,3.8)
        if driver.find_element_by_id(CLUE_IMAGE_NUM).text!='2/'+str(num) or driver.find_element_by_id(CLUE_IMAGE_TITLE).text != username:
            false_count += 1
        slide_right(driver)
        if driver.find_element_by_id(CLUE_IMAGE_NUM).text!='1/'+str(num) or driver.find_element_by_id(CLUE_IMAGE_TITLE).text != username:
            false_count += 1
        driver.find_element_by_id(PV_IMAGE).click()
        if element_exsist(driver,'id',CLUE_IMAGE_SAVE) or element_exsist(driver,'id',BUTTON_BACK):
            false_count += 1
        driver.find_element_by_id(PV_IMAGE).click()
        if not element_exsist(driver,'id',CLUE_IMAGE_SAVE) and not element_exsist(driver,'id',BUTTON_BACK):
            false_count += 1
        if not element_exsist(driver,'id',CLUE_IMAGE_SAVE):
            false_count += 1
        driver.find_element_by_id(BUTTON_BACK).click()
        if element_exsist(driver,'id',PV_IMAGE):
            false_count += 1
    if false_count:
        return False
    else:
        return True


def search_cLue_and_save_images(driver,extend,imagenum = 9,keyword = NINE_IMAGES_CLUE_KEYWORD):
    image_save_path = 'sdcard/'+IMAGE_SAVE_DIR+'/'
    get_to_search(driver,MODE)
    search_clue(driver,keyword)
    sleep(WAIT_TIME)
    clue_image_el = driver.find_element_by_id(HEAD_PIC)
    extend.get_screenshot_by_element(clue_image_el).write_to_file(PIC_SAVE_PATH, "templet_clue_images")
    image_path = PIC_SAVE_PATH+"/templet_images.png"
    imagepathcheck = os.path.isfile(PIC_SAVE_PATH+"/templet_clue_images.png")
    if imagepathcheck:
        print u'截图保存成功！！！'
    else:
        print u'FAIL!!!----------------》截图保存失败！！！'
    images = clue_image_el.find_elements_by_class_name(IMAGEVIEW)
    images[0].click()
    i = 0
    while i < imagenum:
        driver.find_element_by_id(CLUE_IMAGE_SAVE).click()
        if i < imagenum-1:
            slide_left(driver,3.8)
        i += 1
    driver.press_keycode(4)
    p = ls(image_save_path)
    count = p.count("\n")
    driver.press_keycode(4)
    if count >= imagenum+2:
        print u'下载图片成功!'
        return image_path
    else:
        print u'FAIL!!!--------->下载图片失败!!!'
        return False


#发布报料 subtype=0为发送报料，subtype=1为发送我秀
def send_txt_clue(driver,content,subtype = 0,loc = False,in_page = True):
    if not in_page:
        driver.find_element_by_id(CLUE_PUBLISH).click()
    if subtype:
        driver.find_element_by_id(SHOWMETAB).click()
    driver.find_element_by_id(CLUE_CONTENT_INPUT_BOX).send_keys(content)
    if loc:
        # driver.press_keycode(4)
        driver.find_element_by_id(CLUE_LOCATION).click()
        driver.find_element_by_id(ClUE_LOCATION_EDIT).send_keys(loc)
        driver.find_element_by_id(CLUE_LOCATION_EDIT_SUBMIT).click()
    driver.find_element_by_id(SEND_CLUE_BUTTON).click()
    sleep(WAIT_TIME)
    return True

def check_clue(driver,extend,cluetestDic,subtype = 0):
    content = cluetestDic.get('content')
    username = cluetestDic.get('username')
    base_path = os.path.abspath(os.path.dirname(__file__))
    file_path = base_path.replace('Lib','images\\')
    true_count = 0
    if username == '':
        print 'get user name'
        cluetestDic['username'] = get_user_name(driver)
    result = search_clue(driver,content)
    if result:
        print u'报料能够被搜索！'
        true_count += 1
    else:
        print u'FAIL!!!-----------》报料无法被搜索！'

    if subtype:
        type = 'woxiu'
    else:
        type = 'baoliao'

    subtypeicon_el = driver.find_element_by_id(CLUE_SUBTYPE_ICON)
    extend.get_screenshot_by_element(subtypeicon_el).write_to_file(PIC_SAVE_PATH, "cluesubtypetest")
    subcheck = extend.image_in_files_same_as(subtypeicon_el,file_path+type,0)
    if subcheck:
        print u'报料列表类型校验成功！'
        true_count += 1
    else:
        print u'FAIL!!!---------------》报料列表类型校验失败！'

    check_clue_without_type_result = check_clue_without_type(driver,extend,cluetestDic)
    if check_clue_without_type_result:
        true_count += 1

    if true_count == 3:
        return True
    else:
        return False

def check_clue_without_type(driver,extend,cluetestDic):
    content = cluetestDic.get('content')
    username = cluetestDic.get('username')
    loc = cluetestDic.get('loc')
    time = cluetestDic.get('time')
    image_path = cluetestDic.get('image_path')
    image_num = cluetestDic.get('image_num')

    false_count = 0
    is_contain_images = element_exsist(driver,'id',HEAD_PIC)
    if not image_num:
        if not is_contain_images:
            print u'纯文本报料校验正确！'
        else:
            false_count += 1
            print u'FAIL!!!------------------》是否为纯文本报料校验失败！'
    elif image_path:
            # """截图检查"""
        element = driver.find_elements_by_class_name(LISTLAYOUT)[0].find_element_by_id(HEAD_PIC)
        extend.get_screenshot_by_element(element).write_to_file(PIC_SAVE_PATH, "DXclueimagecheck")
        if extend.same_as_rgb(image_path,PIC_SAVE_PATH+'testfordetail.png',0.1,10):
            print u'报料图片校验成功'
        else:
            false_count += 1
            print u'FAIL!!!--------------》报料图片校验失败'

    if driver.find_elements_by_class_name(LISTLAYOUT)[0].find_element_by_id(CLUE_USER_NAME).text == username:
        print u'用户名校验成功'
    else:
        false_count += 1
        print u'FAIL!!!--------------》用户名校验失败'

    if driver.find_elements_by_class_name(LISTLAYOUT)[0].find_element_by_id(HEAD_CONTENT).text == content:
        print u'报料内容校验成功'
    else:
        false_count += 1
        print u'FAIL!!!--------------》报料内容校验失败'

    # """地理位置检查"""
    loctrue = driver.find_elements_by_class_name(LISTLAYOUT)[0].find_element_by_id(CLUE_LOCATION).text
    if loc == loctrue:
        print u'地理位置定位正确！'
    elif loc==False:
        if  DEFAULT_LOC in loctrue:
            print u'地理位置定位正确！'
        else:
            false_count += 1
            print u'FAIL!!!----------》地理位置定位错误'
    else:
        false_count += 1
        print u'FAIL!!!--------------》地理位置校验失败'

    # """时间检查"""
    clue_time = driver.find_elements_by_class_name(LISTLAYOUT)[0].find_element_by_id(CLUE_TIME).text
    pattern = re.compile(r'^\d{2}-\d{2}\s\d{2}:\d{2}$')
    if len(pattern.findall(clue_time)) and (time in clue_time):
        print u'时间校验通过，日期正确，格式正确，时分未精确校验'
    else:
        false_count += 1
        print u'FAIL!!!--------------》时间校验失败'

    if not false_count:
        print u'报料内容模块校验成功!'
        return True
    else:
        return False

def add_images_in_clue(driver,image_num=9,image_dir = IMAGE_SAVE_DIR):
    sleep(2)
    driver.find_element_by_id(CLUE_ADD_IMAGE).click()
    trynum = 0
    while trynum < 4:
        el = find_element_by_name_like(driver,SELECT_IMAGES_DIR,image_dir)
        if el:
            break
        else:
            slide_up(driver,5,2)
            trynum += 1
    el.click()
    for pic in range (image_num-1,-1,-1):
        driver.find_elements_by_id(SELECT_IMAGE)[pic].click()
    driver.find_element_by_id(SEND_CLUE_BUTTON).click()
    imageviews = driver.find_element_by_id(CLUE_CONTENT_INPUT_BOX).find_elements_by_id(CLUE_SELECTED_IMAGES)
    if image_num == 9:
        if image_num == len(imageviews):
            driver.find_element_by_id(CLUE_ADD_IMAGE).click()
            driver.find_element_by_id(CLUE_ADD_PHOTO).click()
            assert element_exsist(driver,'id',CLUE_ADD_PHOTO)
    else:
        assert image_num == len(imageviews)-1

def send_txt_clue_with_image(driver,content,subtype=0,loc=False,image_num = 9,image_dir=IMAGE_SAVE_DIR,in_page = False):
    if not in_page:
        driver.find_element_by_id(CLUE_PUBLISH).click()
    add_images_in_clue(driver,image_num,image_dir)
    send_txt_clue(driver,content,subtype,loc,True)
    return True

def cluelist_to_myclue(driver):
    driver.find_element_by_name(NEWSTABTXT).click()
    go_to_myclue(driver)

def myclue_to_cluelist(driver):
    back(driver)
    exit_usercenter(driver)
    sleep(2)
    go_to_clue(driver)

def delete_image_in_clue(driver):
    driver.find_element_by_id(CLUE_IMAGE_DELETE).click()
    driver.find_element_by_name("确定").click()

if __name__ == '__main__':
    clue_time = '02-02 09:56'
    pattern = re.compile(r'^\d{2}-\d{2}\s\d{2}:\d{2}$')
    result = len(pattern.findall(clue_time))
    print result
