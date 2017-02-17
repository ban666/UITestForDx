# -*- coding: utf-8 -*-
__author__ = 'liaoben'

from RequestForDx import RequestForDx
from DbLib import DbLib
from mongo import Mongo
import back
import requests
import json

class AddressRequest(RequestForDx):

    def __init__(self,mode,ec='420000000010000',cc='420106',p='a',v='3.1.2',ak='1',dc = '1,0,0,jv5RDypcLOG1Ho6UTgf8NN5sUcLGl4Zvk2eH3fH3wEI=#5942cf325a19a9d552f2ad6b617f235e',tid='a_imei865479020303095',pid = '100d855909470b42cd9',loc = '',chnl_para='cnhubei',secret="yJfRVvn6u9yCpn"):
        super(AddressRequest,self).__init__(ec,cc,p,v,ak,dc,tid,pid,loc,chnl_para,secret)
        self.mode = mode
        self.dx_mode = 'mcp/dx'
        self.dx_plug_mode = 'mcp/plug/app'

    def get_address_list(self,id='',cmd='nearer',psize='20',*args):
        data = [self.mode+u'/1/user/addr/list','id='+str(id),'cmd='+cmd,'psize='+str(psize)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['data']['list']

    def save_address(self,name,phone,code,street,zip,infoid='',*args):
        try:
            name = name.encode('utf-8')
            street = street.encode('utf-8')
        except:
            pass
        data = [self.mode+u'/1/user/addr/save','id='+str(infoid),'name='+str(name),'street='+str(street),
                'code='+str(code),'zip='+str(zip),'phone='+str(phone)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        if result['code']=='0':
            return True
        return False

    def del_address(self,infoid,*args):
        data = [self.mode+u'/1/user/addr/del','id='+str(infoid)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        if result['code']=='0':
            return True
        return False

    def set_default(self,infoid,*args):
        data = [self.mode+u'/1/user/addr/default','id='+str(infoid)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        if result['code']=='0':
            return True
        return False

    def clear_address(self):
        address_list = self.get_address_list(psize=1000)
        address_list = [x.get('id') for x in address_list]
        for address in address_list:
            self.del_address(address)


if __name__ == '__main__':
    print 1111
    act = AddressRequest('mcp/dx')
    ad = act.get_address_list()
    from random import randint
    name= 'test'+str(randint(1,1000))
    phone = '1341234567'+str(randint(0,9))
    zip ='123456'
    loc = '420106'
    street = '123456'
    print act.save_address(name,phone,loc,street,zip)
    #print act.apply_activity(775964821224165376,'abc','13411111111',remark)