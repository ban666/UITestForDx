# -*- coding: utf-8 -*-
__author__ = 'liaoben'

import pcap
import dpkt
from datetime import datetime,timedelta
from Queue import Queue
from threading import Thread
from time import sleep
from urllib import unquote
import urllib
def capture(q,duration,expect_host):
    end_time = datetime.now()+timedelta(seconds=duration)
    pc = pcap.pcap()
    pc.setfilter('tcp port 80')

    for ptime,pdata in pc:
        if datetime.now() >= end_time:
            return
        p=dpkt.ethernet.Ethernet(pdata)
        if p.data.__class__.__name__=='IP':
            ip='%d.%d.%d.%d'%tuple(map(ord,list(p.data.dst)))
            if p.data.data.__class__.__name__=='TCP':
                if p.data.data.dport==80:
                   sStr1 = p.data.data.data
                   host = get_host(sStr1)
                   # #print type(sStr1)
                   # print sStr1
                   # sStr2 = 'Host: '
                   # sStr3 = 'Connection'
                   # sStr4 = 'GET /'
                   # sStr5 = ' HTTP/1.1'
                   # nPos = sStr1.find(sStr3)
                   # nPosa = sStr1.find(sStr5)
                   # if sStr1.find(sStr2) >= 0:
                   #     for n in range(sStr1.find(sStr2)+6,nPos-1):
                   #         host=sStr1[sStr1.find(sStr2)+6:n]
                   if host == expect_host:
                       q.put(analysis(sStr1))


def get_host(c):
    c= c.split('\n')
    for con in range(len(c)-1,0,-1):
        if c[con]=='':
            c.pop(con)
    for i in c:
        if i.find('Host')!=-1:
            return i.split(':')[-1].strip()


def analysis(c):
    c= c.split('\n')
    c=[x.strip() for x in c]
    for con in range(len(c)-1,0,-1):
        if c[con]=='':
            c.pop(con)
    path = c[0].split()[1]
    method = c[0].split()[0]
    if method == 'POST':
        payload = unquote(c[-1]).split('&')
        payload_dict = {}
        for pay in payload:
            #print pay.split('=')
            key,values = pay.split('=',1)
            payload_dict[key] = values
        return path,payload_dict
    elif method == 'GET':
        print c
        path = unquote(path)
        if path.find('?')!=-1:
            path,payload =path.split('?',1)
            payload = payload.split('&')
            payload_dict = {}
            for pay in payload:
                #print pay.split('=')
                key,values = pay.split('=',1)
                payload_dict[key] = values
            return path,payload_dict
        return path
    return False
# host='host'
# urlex='urlex'
# pc=pcap.pcap()
# pc.setfilter('tcp port 80')
#
# for ptime,pdata in pc:
#     host = ""
#     urlex = ""
#     p=dpkt.ethernet.Ethernet(pdata)
#     if p.data.__class__.__name__=='IP':
#         ip='%d.%d.%d.%d'%tuple(map(ord,list(p.data.dst)))
#         if p.data.data.__class__.__name__=='TCP':
#             if p.data.data.dport==80:
#                #print p.data.data.data
#                sStr1 = p.data.data.data
#                #print type(sStr1)
#                print sStr1
#                # print "==============data=================="
#                # print sStr1
#                # print "===================================="
#                sStr2 = 'Host: '
#                sStr3 = 'Connection'
#                sStr4 = 'GET /'
#                sStr5 = ' HTTP/1.1'
#                nPos = sStr1.find(sStr3)
#                nPosa = sStr1.find(sStr5)
#                if sStr1.find(sStr2) >= 0:
#                    for n in range(sStr1.find(sStr2)+6,nPos-1):
#                        host=sStr1[sStr1.find(sStr2)+6:n]
#                        # print "n:" + n.__str__() + " " + "host" + host
#                if (sStr1.find(sStr4) >= 0):
#                     for n in range(sStr1.find(sStr4)+4,nPosa+1):
#                         urlex=sStr1[sStr1.find(sStr4)+4:n]
#                          # print "n:" + n.__str__() + " " + "urlex" + urlex
#                print host
#                print urlex
#                result=host+urlex
#                if result.__len__() > 0:
#                    print "==============result=================="
#                    print ptime
#                    print result
#                    print "======================================"

if __name__ == '__main__':
    q = Queue()
    t = Thread(target=capture,args=(q,10,'test.cnhubei.com',))
    t.start()
    sleep(10)
    l = []
    print q.qsize()
    while not q.empty():
        l.append(q.get(timeout=0.1))
    print l
    print 2222222222222
#     c = '''POST /mcp/dx/1/govinfo/sublist HTTP/1.1
# Content-Type: application/x-www-form-urlencoded; charset=UTF-8
# Content-Length: 332
# Host: test.cnhubei.com
# Connection: Keep-Alive
# Accept-Encoding: gzip
# User-Agent: okhttp/2.2.0
#
# hd_v=3.2.1&cateid=750268095477846016&hd_pid=&cmd=nearer&hd_tid=a_imei000000000000000&hd_dc=1%2C0%2C0%2CX2TPW5OoM0.qHQvRFLnKdjOgjrOg0HjJ5uwBDTqXXC0%3D%23e8c9d9610284793952cd6745faec0db5&hd_cc=429005&hd_ec=420000000010000&hd_loc=&psize=20&hd_sign=0339000935d6d1c21f406a163e620fde&id=&hd_chnl=cnhubei&hd_p=a&hd_ts=1482824342721&hd_ak=1
# '''
#     c= c.split('\n')
#     for con in range(len(c)-1,0,-1):
#         if c[con]=='':
#             c.pop(con)
#     path = c[0].split()[1]
#     method = c[0].split()[0]
#     payload = unquote(c[-1]).split('&')
#     payload_dict = {}
#     for pay in payload:
#         print pay.split('=')
#         key,values = pay.split('=',1)
#         payload_dict[key] = values
#     print path
#     print method
#     print payload
#     print payload_dict