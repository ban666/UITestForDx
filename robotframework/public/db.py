#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: liaoben

import MySQLdb

class DxDb:

    def init_cfg(self,db='mcp'):
        self.host = '10.99.113.80'
        self.user = 'root'
        self.passwd = 'AiWz2uMRwiCpkRqeHtrxv'
        self.db =db

    def connect(self,db='mcp'):
        self.init_cfg(db)
        self.conn = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd,db=self.db)
        self.cursor = self.conn.cursor (cursorclass = MySQLdb.cursors.DictCursor)

    def do(self,content):
        self.cursor.execute(content)
        results = self.cursor.fetchall()
        self.conn.commit()
        return results

    def disconn(self):
        self.conn.close()


if __name__ == '__main__':
    dbtest = DxDb()
    dbtest.conn()
    r = dbtest.do('SELECT domainCode as ec from domain,apps where apps.appid=1 and apps.domid=domain.domid;')
    print r[0]['ec']
    dbtest.disconn()