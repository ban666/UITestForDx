# -*- coding: utf-8 -*-
__author__ = 'liaoben'

from RequestForDx import RequestForDx
from DbLib import DbLib
from mongo import Mongo
import back
import requests
import json

class ActivityRequest(RequestForDx):

    def __init__(self,mode,ec='420000000010000',cc='420106',p='a',v='3.1.2',ak='1',dc = '1,0,0,jv5RDypcLOG1Ho6UTgf8NN5sUcLGl4Zvk2eH3fH3wEI=#5942cf325a19a9d552f2ad6b617f235e',tid='a_imei865479020303095',pid = '100d855909470b42cd9',loc = '',chnl_para='cnhubei',secret="yJfRVvn6u9yCpn"):
        super(ActivityRequest,self).__init__(ec,cc,p,v,ak,dc,tid,pid,loc,chnl_para,secret)
        self.mode = mode
        self.dx_mode = 'mcp/dx'
        self.dx_plug_mode = 'mcp/plug/app'

    def get_activity_list(self,id='',cmd='nearer',psize='20',*args):
        data = [self.mode+u'/1/act/list','id='+str(id),'cmd='+cmd,'psize='+str(psize)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['data']['list']

    def apply_activity(self,infoid,name,phone,remark='',*args):
        try:
            name = name.encode('utf-8')
            remark = remark.encode('utf-8')
        except:
            pass
        print remark
        data = [self.mode+u'/1/act/apply','id='+str(infoid),'name='+str(name),'phone='+str(phone),'remark='+str(remark)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        if result['code']=='0':
            return True
        return False

    def activity_detail(self,infoid,*args):
        data = [self.mode+u'/2/news/getactivity','id='+str(infoid)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['data']['data']

    def get_activity_by_state(self,state,id='',cmd='nearer',psize='20',*args):
        ret = self.get_activity_list(id,cmd,psize,*args)
        result = []
        for r in ret:
            if str(r['state']) == str(state):
                result.append(r)
        return result


if __name__ == '__main__':
    print 1111
    act = ActivityRequest('mcp/dx')
    remark= '一'*101
    print remark
    #print act.apply_activity(775964821224165376,'abc','13411111111',remark)