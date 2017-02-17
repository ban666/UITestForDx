# -*- coding: utf-8 -*-
__author__ = 'liaoben'

import redis
from mongo import  Mongo


class RedisHandler(object):

    def __init__(self,db=1):
        self._host='10.99.113.80'
        self._port=6379
        self._password='Hs1JlTXOGsDRtq8UH'
        self._db=db
        self.r = redis.Redis(host=self._host,port=self._port,db=self._db,password=self._password)

    def connect(self):
        self.r = redis.Redis(host=self._host,port=self._port,db=self._db,password=self._password)

    def get_vcode(self,mid,phone):
        return self.r.hget('H_VERIFYCODE:'+str(mid),phone)

    def get_vcode_count(self,tid):
        return self.r.get('VERIFYNCOUNT:'+str(tid))

    def clear_vcode_count(self,tid):
        return self.r.delete('VERIFYNCOUNT:'+str(tid))

    def get_vcode_by_dc(self, phone, dc,tid='a_imei000000000000000'):
         m = Mongo()
         vcode = False
         if dc.find('#')!=-1:
             dc = dc.split('#')[0]
         try:
             mid = m.get_mid(dc)
             vcode = self.get_vcode(str(mid),str(phone))
         except Exception as e:
             print e
         finally:
             self.clear_vcode_count(tid)
             return vcode

    def get_latest_vcode(self,phone):
        for i in self.r.keys():
            if i.find('H_VERIFYCODE')!=-1:
                ret = self.r.hget(i,phone)
                if ret:
                    return ret
        return False
if __name__ == '__main__':
    redis = RedisHandler()
    print redis.r.hget('H_VERIFYCODE:768351856484421632','13412341234')
    tid = 'a_imei000000000000000'
    print redis.get_vcode_count(tid)
    print redis.clear_vcode_count(tid)
    def get_vcode_by_redis(phone,dc,tid='a_imei000000000000000'):
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
             r.clear_vcode_count(tid)
             return vcode