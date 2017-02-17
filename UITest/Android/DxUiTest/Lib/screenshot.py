# -*- coding: utf-8 -*-
__author__ = 'liaoben'

import os
import tempfile
import shutil
import sys
from config import *

from PIL import Image

PATH = lambda p: os.path.abspath(p)
TEMP_FILE = PATH(tempfile.gettempdir() + "/temp_screen.png")

class Appium_Extend(object):
    def __init__(self, driver):
        self.driver = driver

    def get_screenshot_by_element(self, element):
        #先截取整个屏幕，存储至系统临时目录下
        self.driver.get_screenshot_as_file(TEMP_FILE)

        #获取元素bounds
        location = element.location
        size = element.size
        box = (location["x"], location["y"], location["x"] + size["width"], location["y"] + size["height"])

        #截取图片
        image = Image.open(TEMP_FILE)
        newImage = image.crop(box)
        newImage.save(TEMP_FILE)

        return self

    def get_screenshot_by_custom_size(self, start_x, start_y, end_x, end_y):
        #自定义截取范围
        self.driver.get_screenshot_as_file(TEMP_FILE)
        box = (start_x, start_y, end_x, end_y)

        image = Image.open(TEMP_FILE)
        newImage = image.crop(box)
        newImage.save(TEMP_FILE)

        return self

    def write_to_file( self, dirPath, imageName, form = "png"):
        #将截屏文件复制到指定目录下
        if not os.path.isdir(dirPath):
            os.makedirs(dirPath)
        shutil.copyfile(TEMP_FILE, PATH(dirPath + "/" + imageName + "." + form))

    def load_image(self, image_path):
        #加载目标图片供对比用
        if os.path.isfile(image_path):
            load = Image.open(image_path)
            return load
        else:
            raise Exception("%s is not exist" %image_path)

    #http://testerhome.com/topics/202
    def same_as(self, load_image, percent):
        #对比图片，percent值设为0，则100%相似时返回True，设置的值越大，相差越大
        import math
        import operator

        image1 = Image.open(TEMP_FILE)
        image2 = load_image

        histogram1 = image1.histogram()
        histogram2 = image2.histogram()

        differ = math.sqrt(reduce(operator.add, list(map(lambda a,b: (a-b)**2, \
                                                         histogram1, histogram2)))/len(histogram1))
        print differ
        if differ <= percent:
            return True
        else:
            return False



    def resize_same_as(self,expect_path,truth_path,percent):
        import math
        import operator
        image1 = Image.open(expect_path)
        image2 = Image.open(truth_path)
        (x,y) = image2.size
        image1 = image1.resize((x,y),Image.ANTIALIAS)
        image1.save(PIC_SAVE_PATH+'test.png')

        histogram1 = image1.histogram()
        histogram2 = image2.histogram()

        differ = math.sqrt(reduce(operator.add, list(map(lambda a,b: (a-b)**2, \
                                                         histogram1, histogram2)))/len(histogram1))
        print differ
        if differ <= percent:
            return True
        else:
            return False


    def image_in_files_same_as(self,element,file_path,percent):
        image_paths = os.listdir(file_path)
        IsSame = False
        for image in image_paths:
            image_path = file_path + '/'+image
            image = Image.open(image_path)
            result = self.get_screenshot_by_element(element).same_as(image,percent)
            if result:
                IsSame = True
                return IsSame
        return IsSame

    def same_as_rgb(self,img1,img2, percent,miss=10):
        #对比图片，percent值设为0，则100%相似时返回True，设置的值越大，相差越大


        image1 = Image.open(img1)
        image2 = Image.open(img2)
        rgb_im1 = image1.convert('RGB')
        rgb_im2 = image2.convert('RGB')

        count = 0

        if image1.size != image2.size:
            return False
        x,y = image1.size
        for width in range(x):
            for height in range(y):
                rgb1 = rgb_im1.getpixel((width, height))
                rgb2 = rgb_im2.getpixel((width, height))
                for j in range(len(rgb1)):
                    if abs(rgb1[j]-rgb2[j])>miss:
                        count+=1
                    break

        differ = count/float(x*y)
        print differ
        if differ <= percent:
            return True
        else:
            return False

# if __name__ == '__main__':
#     path = 'f:/pic/'
#     f1 = 'nine_clue_images.png'
#     f2 = 'DXclueimagecheck.png'
#     a = Appium_Extend(1)
#     print a.same_as_rgb(path+f1,path+f2,10,10)