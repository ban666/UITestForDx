# -*- coding: utf-8 -*-
__author__ = 'liaoben'

import requests
import json
import time
import hashlib
import chardet
import urllib

class RequestForDx(object):

    def __init__(self,ec='420000000010000',cc='420100',p='a',v='3.1.2',ak='1',dc = "1,0,0,93JhERG1UYLiW.p6UfdubuLUFveUZCjg6v.QMEkHKu8=#cc36a2ebfc32b210b90f91f8885de0bc",tid='a_imei865479020303095',pid = '100d855909470b42cd9',loc = 'abc',chnl_para='cnhubei'):
        self.secret = "yJfRVvn6u9yCpn"
        self.domain =  'http://test.cnhubei.com/'
        self.path = ''
        self.defaultec='420000000010000'
        self._dc = dc
        self.tid = tid
        self.ec = ec
        self.loc = loc
        self.ak = ak
        self.v = v
        self.p = p
        self.pid = pid
        self.cc = cc
        self.chnl_para= chnl_para
        self.defaultdc = "1,0,0,93JhERG1UYLiW.p6UfdubuLUFveUZCjg6v.QMEkHKu8=#cc36a2ebfc32b210b90f91f8885de0bc"
        '''
        self.dc = '1,0,0,suiZBeeEhYc391o8NI6samFpGXp8kd8L0ALLxd7Tt5Q=#af65396ebb49846daf9d98343c34f184'
        self.tid='a_imei865479020303095'
        self.ec='420000000010000'
        self.loc = ''
        self.ak='1'
        self.v='3.1.2'
        self.p='a'
        self.pid = '100d855909470b42cd9'
        self.cc='420106'
        self.chnl='cnhubei'
        '''

    @property
    def dc(self):
        return self._dc

    @dc.setter
    def dc(self, value):
        self._dc = value

    def model_init(self):
        self.payload = {
        'hd_dc':self._dc,
        'hd_ak':self.ak,
        'hd_v'	:self.v,
        'hd_ts':str(int(time.time()*1000)),
        'hd_p':self.p,
        'hd_loc':self.loc,
        'hd_pid':self.pid,
        'hd_tid':self.tid,
        'hd_chnl':self.chnl_para,
        'hd_ec':self.ec,
        'hd_cc':self.cc
        }


    def gen_payload(self,*args):
        test_data ={}
        self.path = args[0]
        for arg in args[1:]:
            temp = arg.split('=',1)
            test_data[str(temp[0])] = str(temp[1])
        self.payload.update(test_data)
        #print self.payload
        ret = []
        for key,val in self.payload.items():
            ret.append(key+val)
        try:
            ret=[unicode(x.decode('utf-8')) for x in ret]
        except:
            pass
        ret.sort()
        param_string = self.secret+"".join(ret)+self.secret
        self.payload['hd_sign'] = hashlib.md5(param_string.encode('utf-8')).hexdigest()
        #print self.payload['hd_sign']

    def send_request_for_dx(self,*args):
        self.model_init()
        self.gen_payload(*args)
        req = self.domain+self.path
        #print req
        res = requests.post(req,data=self.payload)
        if res.status_code==200:
            #print 'post success'
            pass
        ret = res.content
        try:
            j_dict = json.loads(ret)
            return j_dict
        except Exception, e:
            #print e
            return ret

    '''
    名称	值	说明
    dc	P1	用户证书
    lgd	P2	用户是否登录 0 未登录 1 登录
    tid	P3	终端标识符(用于标识终端的唯一性，不要求非常精准)
    cc	P4	用户所在城市的行政区划代码
    sid	P5	sessionid
    url	P6	目标实际地址
    '''
    def replace_args(self,url_str,dc='',lgd='1',):
        ret = url_str.replace('\$\{dc\}',self.dc)




if __name__ == '__main__':
    def gen_p(*args):
        secret = 'yJfRVvn6u9yCpn'
        test_data ={}
        for arg in args[1:]:
            temp = arg.split('=',1)
            print temp
            test_data[str(temp[0])] = str(temp[1])
        print test_data

        ret = []
        for key,val in test_data.items():
            ret.append(key+val)
        ret.sort()
        param_string = secret+"".join(ret)+secret
        r =  hashlib.md5(param_string).hexdigest()
        return r
