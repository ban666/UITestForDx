# -*- coding: utf-8 -*-
__author__ = 'liaoben'

from RequestForDx import RequestForDx
from DbLib import DbLib
from mongo import Mongo
import back
import requests
import json

class GovRequest(RequestForDx):

    def __init__(self,mode,ec='420000000010000',cc='420106',p='a',v='3.1.2',ak='1',dc = '1,0,0,jv5RDypcLOG1Ho6UTgf8NN5sUcLGl4Zvk2eH3fH3wEI=#5942cf325a19a9d552f2ad6b617f235e',tid='a_imei865479020303095',pid = '100d855909470b42cd9',loc = '',chnl_para='cnhubei',secret="yJfRVvn6u9yCpn"):
        super(GovRequest,self).__init__(ec,cc,p,v,ak,dc,tid,pid,loc,chnl_para,secret)
        self.mode = mode
        self.dx_mode = 'mcp/dx'
        self.dx_plug_mode = 'mcp/plug/app'

    def get_gov_list(self,code='42',id='',cmd='nearer',psize='20',*args):
        data = [self.mode+u'/1/govinfo/list','code='+str(code),'id='+str(id),'cmd='+cmd,'psize='+str(psize)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['data']['list']

    def get_gov_detail(self,infoid,*args):
        data = [self.mode+u'/1/govinfo/get','id='+str(infoid)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['data']['data']

    def get_gov_sublist(self,cateid,id='',cmd='nearer',psize='20',*args):
        data = [self.mode+u'/1/govinfo/sublist','cateid='+str(cateid),'id='+str(id),'cmd='+cmd,'psize='+str(psize)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['data']['list']



if __name__ == '__main__':
    print 1111
    act = GovRequest('mcp/dx')
    remark= '一'*100
    gov_list = act.get_gov_list()
    gov_detail = act.get_gov_detail(gov_list[0]['id'])
    sublist = act.get_gov_sublist(gov_detail['cate1'])
    print sublist