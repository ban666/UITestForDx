# -*- coding: utf-8 -*-
__author__ = 'liaoben'

from PIL import Image, ImageDraw,ImageFont

#center crop
def image_crop(fname,x,y,out,lashen = True):
    """

    :param fname:输入文件
    :param x:截取宽度
    :param y:截取高度
    :param out:输出文件名
    :param lashen:True：允许拉伸，False:禁止拉伸
    :return:
    """
    image = Image.open(fname)
    sx,sy = image.size
    startx = (sx-x)/2
    starty= (sy-y)/2
    if (x>sx or y>sy) and error:
        print '截取范围大于图片大小，且不允许拉伸，请重新设定截取范围'
        return
    box = [startx,starty,startx+x,starty+y]
    print box
    newImage = image.crop(box)
    newImage.save(out)

if __name__ == '__main__':
    f = 'g:/music/1.jpg'
    out = 'g:/music/2.jpg'
    image_crop(f,960,20000,out)

