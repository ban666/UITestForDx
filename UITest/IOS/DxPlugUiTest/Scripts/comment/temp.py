# -*- coding: utf-8 -*-
__author__ = 'liaoben'

from pytesser import *
import os
with open('temp.txt','w+') as f:
    pass
threshold = 140
table = []

fn = 'g:/toast2.png'
out_fn = 'g:/temp.png'
from PIL import Image,ImageEnhance
t = Image.open(fn)
t = t.convert('L')
#t.show()
# out = t.point(table,'1')
# out.save(out_fn)
# enhancer = ImageEnhance.Contrast(t)
# image_enhancer = enhancer.enhance(4)
#txt = image_to_string(t)
txt = image_to_string(t,language='normal')
#print txt.decode('gbk').encode('gbk')
print txt
print txt.strip() == '网络不给力'