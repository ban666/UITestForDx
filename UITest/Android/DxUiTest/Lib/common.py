# -*- coding:utf-8 -*-
__author__ = 'Ban'

import os,time,sys,glob
from PIL import Image
import functools
import requests
from bs4 import BeautifulSoup
from config import APK_PATH
from urllib import unquote,urlretrieve
from datetime import datetime,timedelta

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

def judgeCaseLevel(case,level):
    caselevel=case[2]
    if caselevel in level:
        return 1
    else:
        return 0

def getTime_s():
    return time.strftime("%Y%m%d%H%M%S", time.localtime())

def printCaseStart(case):
    msg="TestcaseNo.:"+case[0]+' Start'
    msg+=' TestcaseName:'+case[1]+' TestcaseLevel:'+case[2]+""
    return msg

def printCaseEnd(case):
    msg="TestcaseNo.:"+case[0]+' End'
    return msg

def getLogfile(fname):
    Nowtime=time.strftime("%Y%m%d%H%M%S", time.localtime())
    Newname=''.join([os.path.split(fname)[0].replace('Scripts','Log'),'/','Log_',Nowtime,'.log'])
    return Newname

def getReportfile(fname):
    Nowtime=time.strftime("%Y%m%d%H%M%S", time.localtime())
    Newname=''.join([os.path.split(fname)[0].replace('Scripts','Log'),'/','Report_',Nowtime,'.log'])
    return Newname

def getAllPy(folder):
    tstr=folder+"\\*.py"
    delstr=folder+"\\__init__.py"
    fileList=glob.glob(tstr)
    try:
        fileList.remove(delstr)
    except Exception as e:
        pass
    return fileList

def updateGlobal(fname,LogFile='',ReportFile='',TestLevel=['level 1','level 2','level 3','level 4','level 5'],*args):
    with open(fname,'w+') as f:
        tstr='Logfile='+'\''+LogFile+'\''+'\n'        
        f.write(tstr)
        tstr='ReportFile='+'\''+ReportFile+'\''+'\n'           
        f.write(tstr)
        tlist='['
        for i in TestLevel:
            tlist+='\''+i+'\''+','
        tlist=tlist.rstrip(',')
        tlist+=']'
        tstr='TestLevel='+tlist+'\n'           
        f.write(tstr)
        for i in args:
            tstr=i[0]+'='+'\''+i[1]+'\''+'\n'   
            f.write(tstr)

def checkArgs(length,*args):
    if len(args) != length:
        print 'len args:',len(args)
        return 0
    return 1

def setTcStatus(tcno,status):
    if status==0:
        result='FAILED'
    elif status==1:
        result='PASS'
    else:
        result='BLOCK'
    msg="TestcaseNo.:"+tcno+' result:'+result+""
    return msg

def reportMsgGenerate(logf,runtime):
    pcount=0
    fcount=0
    bcount=0
    count=0
    msg=''
    with open(logf,'r+') as f:
        for i in f:
            if i.find('result:')!=-1:
                count+=1
                treslut=i[i.find('result:')+7:].strip()
                if treslut=='PASS':
                    pcount+=1
                elif treslut=='FAILED':
                    fcount+=1
                elif treslut=='BLOCK':
                    bcount+=1
                else:
                    bcount+=1
    rate="%.2f%%" % (float(pcount)/float(count)*100)
    rtime="%.2f" % runtime
    rtime=secondsToTime(float(rtime))
    msg='本轮测试共运行测试用例'+str(count)+'个,共计用时:'+str(rtime[0])+'时'+str(rtime[1])+'分'+str(rtime[2])+'秒,其中PASS:'+str(pcount)+'个,FAILED:'+str(fcount)+'个,BLOCK:'+str(bcount)+'个,通过率:'+str(rate)
    return msg

def secondsToTime(iItv):

    if type(iItv)==type(0.1):
        h=int(iItv/3600)
        sUp_h=int(iItv-3600*h)
        m=sUp_h/60
        sUp_m=iItv-3600*h-60*m
        s=sUp_m
        tlist=[str(h),str(m),str(s)]
        return tlist
    else:
        return "[InModuleError]:itv2time(iItv) invalid argument type"

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

def get_image_info(fname):
    m = Image.open(fname)
    h,w = m.height,m.width
    size = '{:.2f}'.format(os.path.getsize(fname)/1024/1024.0)
    return h,w,size


def exception_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        try:
            return func(*args, **kw)
        except Exception,e:
            print 'func_name:'+func.__name__,e.__repr__()
            return False
    return wrapper



def download_latest_apk(url= 'http://10.99.113.28/apk/'):
    r = requests.get(url)
    content = r.content
    soup = BeautifulSoup(content,'html')
    apk =  soup.find_all('a')[-1].text
    download_path = url+apk
    local_path = APK_PATH+apk
    urlretrieve (download_path, local_path)
    return local_path


def get_day(delta=0,strftime='%Y%m%d'):
    now = datetime.now()
    ret = now - timedelta(days=int(delta))
    ret = ret.strftime(strftime)
    return ret

if __name__ == '__main__':
    @exception_handler
    def suma(a,b):
        return a+b

    print suma(1,2)
    print suma('a',1)

