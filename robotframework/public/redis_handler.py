# -*- coding: utf-8 -*-
__author__ = 'liaoben'

import redis

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

    def clear_all_vcode_count(self):
        for vcode in self.r.keys():
            if vcode.find('VERIFYNCOUNT:a_imei')!=-1:
                self.r.delete(vcode)

if __name__ == '__main__':
    redis = RedisHandler()
    print redis.r.hget('H_VERIFYCODE:768351856484421632','13412341234')
    tid = 'a_imei000000000000000'
    print redis.get_vcode_count(tid)
    print redis.clear_vcode_count(tid)