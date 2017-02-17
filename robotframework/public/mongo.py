# -*- coding: utf-8 -*-
__author__ = 'liaoben'

import pymongo
'''
conn = pymongo.Connection("127.0.0.1",27017)
db = conn.tage #连接库
db.authenticate("tage","123")
'''
class Mongo:

    def __init__(self):
        self._host='10.99.113.80'
        self._port=27017
        self._dbname='mcp'
        self._username='mcp'
        self._passwd='95LGinxe4eKKneru8z24FpJno7sOw'

    def conn2db(self):
        self.c = pymongo.MongoClient(self._host,self._port)
        self.db = self.c.mcp
        status = self.db.authenticate(self._username,self._passwd)
        return status

    def get_mid(self,dc):
        if dc.find('#')!=-1:
            dc = dc.split('#')[0]
        status = self.conn2db()
        assert status
        col = self.db['logined_user_list']
        mid = col.find({'dc':dc})[0]['mid']
        print 'mid:',mid
        return mid


if __name__ == '__main__':
    dc='1,0,0,jv5RDypcLOG1Ho6UTgf8NN5sUcLGl4Zvk2eH3fH3wEI='
    m=Mongo()
    print m.get_mid(dc)
    m.conn2db()
    col = m.db['logined_user_list']
    print col.find()[0]
    #print col