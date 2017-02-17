# -*- coding: utf-8 -*-
__author__ = 'liaoben'

import requests
import re
import os
from datetime import datetime,timedelta
from random import randint

def checkip(ip):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(ip):
        return True
    else:
        return False


def unicode_to_str(content):
    try:
        content = content.encode('utf-8')
    except:
        pass
    return content


def get_id(content):
    if content.has_key('id'):
        return content['id']
    elif content.has_key('infoid'):
        return content['infoid']
    return False


def download_image(url,local_fname):
    import requests
    r = requests.get(url, stream=True) # here we need to set stream = True parameter
    with open(local_fname, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
        f.close()
    return True


def same_as(img1,img2, percent):
    from PIL import Image
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


def get_request(url):
    r = requests.get(url)
    return r.content

def get_abspath(path):
    return os.path.abspath(path)

def get_all_id(content,id_var='id'):
    content = [x.get(id_var) for x in content]
    return  content

def gen_dc(dc):
    from uuid import uuid4
    new = dc.split('#')
    new[1] = str(uuid4()).replace('-','')
    new = '#'.join(new)
    return new

def get_day(delta=0):
    now = datetime.now()
    ret = now - timedelta(days=int(delta))
    ret = ret.strftime('%Y%m%d')
    return ret

def gen_randint(start,end):
    return randint(int(start),int(end))

def list_pop_repeat(content):
    reverse = content[::]
    pop_list = []
    for i in range(len(content)-1,0,-1):
        #print i
        if content.count(content[i])>1:
            content.pop(i)
    return content

def replace_ad_url(mid,dc):
    url = 'http://test.cnhubei.com/mcp/targeturl?mid=%s&url=http://www.ifeng.com/&type=1&dc=%s'%(str(mid),str(dc))
    return url


if __name__ == '__main__':
    content = [725939445572046848L, 999999999999999999L, 725939934690807808L, 728550209583583232L, 725940038130733056L, 725940001229246464L, 736033829084729344L, 728550829115838464L, 750142796387848192L, 652011649053757440L, 999999999999999999L, 672678215181144064L, 652010928770125824L, 674060541555380224L, 743356491855302656L, 689294835831803904L, 750144053269762048L, 652012655305035776L, 652012711596789760L, 717550206480289792L, 672679394007060480L, 652012925422407680L, 807147090122903552L, 694069106466623488L, 652012785911468032L, 652012735433019392L, 674130675905073152L, 652012762117181440L]
    b = list_pop_repeat(content)
    print b
    for i in b:
        if b.count(i)>1:
            print i