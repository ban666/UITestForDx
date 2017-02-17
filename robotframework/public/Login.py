# -*- coding: utf-8 -*-
__author__ = 'liaoben'

from RequestForDx import RequestForDx
from mongo import Mongo
from redis_handler import RedisHandler
from time import sleep
from DbLib import DbLib
from conf import QQ_LOGIN_INFO,WECHAT_LOGIN_INFO,WEIBO_LOGIN_INFO
import requests
import json

class UserRequest(RequestForDx):


    def __init__(self,mode,ec='420000000010000',cc='420106',p='a',v='3.1.2',ak='1',dc = '',tid='a_imei000000000000000',pid = '',loc = '',chnl_para='cnhubei',secret="yJfRVvn6u9yCpn"):
        super(UserRequest,self).__init__(ec,cc,p,v,ak,dc,tid,pid,loc,chnl_para,secret)
        self.mode = mode
        self.dx_mode = 'mcp/dx'

    def vcode(self,phone,*args):
        r = RedisHandler()
        r.clear_all_vcode_count()
        data = [self.mode+u'/1/user/vcode','phone='+str(phone)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['dc']

    def get_vcode_by_redis(self,phone,dc):
         r = RedisHandler()
         m = Mongo()
         vcode = False
         if dc.find('#')!=-1:
             dc = dc.split('#')[0]
         try:
             mid = m.get_mid(dc)
             vcode = r.get_vcode(str(mid),str(phone))
         except Exception as e:
             print e
         finally:
             r.clear_vcode_count(self.tid)
             return vcode

    def login(self,phone,vcode,*args):
        data = [self.mode+u'/1/user/login','phone='+str(phone),'vcode='+str(vcode)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        return result

    def openid_login(self,platform,uid,screen_name,profile_image_url,*args):
        data = [self.mode+u'/1/user/openid_login','platform='+str(platform),'uid='+uid,'screen_name='+screen_name,'profile_image_url='+profile_image_url]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        return result

    @staticmethod
    def del_user(mid):
        db = DbLib()
        try:
            db.delete_user_by_db(mid)
            print 'del mid '+str(mid)+'success'
        except Exception as e:
            print e

    def set_icon(self,dc,fname='./resources/test.jpg'):
        data=[api.mode+'/1/user/seticon','hd_dc='+dc]
        api.model_init()
        api.gen_payload(*data)
        req=api.domain+api.path
        for j,k in api.payload.items():
            api.payload[j]=(None,k)
        api.payload['_icon']=(fname,open(fname, 'rb'), 'image/jpg')
        res = requests.post(req,files=api.payload)
        ret = res.content
        try:
            j_dict = json.loads(ret)
            return j_dict
        except Exception, e:
            print e
            return ret

    def set_phone(self,dc,phone,vcode,*args):
        data = [self.mode+u'/1/user/setphone','hd_dc='+dc,'phone='+str(phone),'vcode='+str(vcode)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        return result

    def set_scrname(self,dc,name,*args):
        data = [self.mode+u'/1/user/setscrname','hd_dc='+dc,'name='+name]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        return result

    def get_center(self,dc,*args):
        data = [self.mode+u'/1/user/center','hd_dc='+dc]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        return result

    def set_openuid(self,dc,platform,uid,screen_name,profile_image_url,*args):
        data = [self.mode+u'/1/user/setopenuid','hd_dc='+dc,'platform='+str(platform),'uid='+uid,'screen_name='+str(screen_name),'profile_image_url='+profile_image_url]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        return result

    def myinvite(self,dc,*args):
        data = [self.mode+u'/1/user/myinvite','hd_dc='+dc]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        return result['data']

    def invite(self,dc,vcode,*args):
        data = [self.mode+u'/1/user/invite','hd_dc='+dc,'vcode='+str(vcode)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        return result

    def get_my_comm(self,id='',cmd='nearer',psize='20',*args):
        data = [self.mode+u'/1/user/comlist','id='+str(id),'cmd='+str(cmd),'psize='+str(psize)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['data']['list']

    def get_my_recomm(self,id='',cmd='nearer',psize='20',*args):
        data = [self.mode+u'/1/user/recomlist','id='+str(id),'cmd='+str(cmd),'psize='+str(psize)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['data']['list']

    def invite_plus(self,userinfo,user_invite,*args):
        db = DbLib()
        vcode = db.get_inv_code_by_db(user_invite['data']['userinfo']['uid'])
        mid = userinfo['data']['userinfo']['uid']
        dc = userinfo['dc']
        return  self.invite(dc,mid,vcode,*args)

    def get_point_list(self,dc,id='',cmd='nearer',psize='20',*args):
        data = [self.mode+u'/1/user/pointlist','hd_dc='+str(dc),'id='+str(id),'cmd='+cmd,'psize='+str(psize)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code'] == '0'
        return result['data']

if __name__ == '__main__':
    api = UserRequest('mcp/dx')
    f = './resources/test.jpg'
    with open(f,'r') as fn:
        pass
    #
    # mid = 768362399840604160
    # api.del_user(mid)
    # phone = '13412341234'
    # dc_old = api.vcode('13412341234')
    # api.dc=dc_old
    # dc = dc_old.split('#')[0]
    # sleep(10)
    # vcode = api.get_vcode_by_redis(phone,dc)
    # print vcode
    # phone ='13333333333'
    # vcode = '1'
    #
    # userinfo = api.openid_login(QQ_LOGIN_INFO['platform'],QQ_LOGIN_INFO['uid'],QQ_LOGIN_INFO['screen_name'],QQ_LOGIN_INFO['profile_image_url'])
    # print userinfo
