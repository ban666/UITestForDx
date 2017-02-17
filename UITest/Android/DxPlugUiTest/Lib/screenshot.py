# -*- coding: utf-8 -*-
__author__ = 'liaoben'

import os
import platform
import tempfile
import shutil

from PIL import Image

PATH = lambda p: os.path.abspath(p)
TEMP_FILE = PATH(tempfile.gettempdir() + "/temp_screen.png")

class Appium_Extend(object):

    def __init__(self, driver):
        self.driver = driver

    def get_screenshot_by_element(self, element,fname=TEMP_FILE):
        #先截取整个屏幕，存储至系统临时目录下
        self.driver.get_screenshot_as_file(fname)

        #获取元素bounds
        location = element.location
        size = element.size
        box = (location["x"], location["y"], location["x"] + size["width"], location["y"] + size["height"])

        #截取图片
        image = Image.open(fname)
        newImage = image.crop(box)
        newImage.save(fname)

        return self

    def get_screenshot_by_custom_size(self, start_x, start_y, end_x, end_y, fname=TEMP_FILE):
        #自定义截取范围
        self.driver.get_screenshot_as_file(fname)
        box = (start_x, start_y, end_x, end_y)

        image = Image.open(fname)
        newImage = image.crop(box)
        newImage.save(fname)

        return self

    def write_to_file( self, dirPath, imageName, form = "png", fname=TEMP_FILE):
        #将截屏文件复制到指定目录下
        if not os.path.isdir(dirPath):
            os.makedirs(dirPath)
        shutil.copyfile(fname, PATH(dirPath + "/" + imageName + "." + form))

    def load_image(self, image_path):
        #加载目标图片供对比用
        if os.path.isfile(image_path):
            load = Image.open(image_path)
            return load
        else:
            raise Exception("%s is not exist" %image_path)

    #http://testerhome.com/topics/202
    def same_as(self, load_image, fname, percent=0):
        #对比图片，percent值设为0，则100%相似时返回True，设置的值越大，相差越大
        import math
        import operator

        image1 = Image.open(load_image)
        image2 = Image.open(fname)

        histogram1 = image1.histogram()
        histogram2 = image2.histogram()

        differ = math.sqrt(reduce(operator.add, list(map(lambda a,b: (a-b)**2, \
                                                         histogram1, histogram2)))/len(histogram1))
        if differ <= percent:
            return True
        else:
            return False

if __name__ == '__main__':
    def same_as(img1,img2, percent):
        #对比图片，percent值设为0，则100%相似时返回True，设置的值越大，相差越大
        import math
        import operator

        image1 = Image.open(img1)
        image2 = Image.open(img2)

        histogram1 = image1.histogram()
        histogram2 = image2.histogram()

        differ = math.sqrt(reduce(operator.add, list(map(lambda a,b: (a-b)**2, \
                                                         histogram1, histogram2)))/len(histogram1))
        print differ
        if differ <= percent:
            return True
        else:
            return False

    img1= 'G:\\workspace\\UITest\\DxPlugUiTest\\Images\\notification_pause.png'
    img2= 'G:\\workspace\\UITest\\DxPlugUiTest\\Images\\start20161128104912.png'
    print same_as(img1,img2,0)