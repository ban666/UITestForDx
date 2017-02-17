# -*- coding: utf-8 -*-
__author__ = 'liaoben'

import pcap
import dpkt
from datetime import datetime,timedelta
from Queue import Queue
from threading import Thread
from time import sleep
from urllib import unquote


def capture(q,duration,expect_host,option='all'):
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
                   #print sStr1
                   if host == expect_host:
                       q.put(analysis(sStr1,option))

def capture_test(q,duration,expect_host):
    end_time = datetime.now()+timedelta(seconds=duration)
    pc = pcap.pcap()
    pc.setfilter('tcp port 80')

    for ptime,pdata in pc:
        if datetime.now() >= end_time:
            return
        p=dpkt.ethernet.Ethernet(pdata)
        if p.data.__class__.__name__=='IP':
            ip='%d.%d.%d.%d'%tuple(map(ord,list(p.data.dst)))
            if p.data.data.__class__.__name__=='TCP' or p.data.data.__class__.__name__=='HTTP' :
                # if p.data.data.dport==80:
                #     s =  p.data.data
                #     sStr1 = s.data
                #     host = get_host(sStr1)
                #     print s.ack
                #     print sStr1
                #     if host == expect_host:
                #        q.put(analysis(sStr1))
                if p.data.data.sport==80:
                    t = p.data.data
                    #print dir(t)
                    #print t.ack
                    #print t.data
                    #print t.opts

def get_host(c):
    c= c.split('\n')
    for con in range(len(c)-1,0,-1):
        if c[con]=='':
            c.pop(con)
    for i in c:
        if i.find('Host')!=-1:
            return i.split(':')[-1].strip()




def analysis(c,option='all'):
    #print c
    c= c.split('\n')
    c=[x.strip() for x in c]
    for con in range(len(c)-1,0,-1):
        if c[con]=='':
            c.pop(con)
    path = c[0].split()[1]
    method = c[0].split()[0]
    #print method,path
    #print c
    if method == 'POST'and (option == 'all' or option == 'POST'):
        payload = unquote(c[-1])
        #print payload
        if payload.find('&') == -1 and payload.find('=') == -1:
            return False
        payload = payload.split('&')
        payload_dict = {}
        for pay in payload:
            try:
                key,values = pay.split('=',1)
                payload_dict[key] = values
            except:
                pass
        return path,payload_dict
    elif method == 'GET' and (option == 'all' or option == 'GET'):
        #print c
        path = unquote(path)
        #print path
        try:
            if path.find('?')!=-1:
                path,payload =path.split('?',1)
                payload = payload.split('&')
                payload_dict = {}
                for pay in payload:
                    #print pay.split('=')
                    key,values = pay.split('=',1)
                    payload_dict[key] = values
                return path,payload_dict
            return path,''
        except:
            return path,''
    return False,''

def get_result(q):
    l=[]
    while not q.empty():
        l.append(q.get(timeout=0.1))
    return l

def start_capture(q,duration,domain,option='all'):
    t = Thread(target=capture,args=(q,duration,domain,option,))
    t.start()

if __name__ == '__main__':
    q = Queue()
    start_capture(q,30,'test.cnhubei.com','GET')
    sleep(10)
    l = get_result(q)
    print l
    # capture_test(q,30,'test.cnhubei.com')
    # pc = pcap.pcap()
    # pc.setfilter('tcp port 80')
    # e_ip = '10.99.113.80'
    # pacage_list = []
    # for ptime,pdata in pc:
    #     p=dpkt.ethernet.Ethernet(pdata)
    #     if p.data.__class__.__name__=='IP':
    #         ip='%d.%d.%d.%d'%tuple(map(ord,list(p.data.dst)))
    #         if p.data.data.__class__.__name__=='TCP':
    #             if p.data.data.dport==80:
    #                 if '%d.%d.%d.%d' % tuple(map(ord, list(p.data.src))) == e_ip or '%d.%d.%d.%d' % tuple(map(ord, list(p.data.dst)))==e_ip\
    #                         and p.data.data.data.strip()!='':
    #                     s =  dpkt.http.Request(p.data.data.data)
    #                     print dir(s)
    #             if '%d.%d.%d.%d' % tuple(map(ord, list(p.data.src))) == e_ip\
    #                         and p.data.data.data.strip('')!='':
    #                     print p.data.data.data
    #                     s =  dpkt.http.Response(p.data.data.data)
    #                     print dir(s)
    #                     #s1 = p.data
                #     s2=p
                #     #print dir(s1)
                #     sStr1 = s.data
                #     print '==============='
                #     print sStr1
                #     #print s1.__dict__
                #     #print '%d.%d.%d.%d' % tuple(map(ord, list(s1.src)))
                #     #print dir(s2)
                #     print '=================='
                #     host = get_host(sStr1)
                # if p.data.data.sport==80:
                #     t = p.data.data
                #     #print dir(t)
                #     #print t.ack
                #     print '-----------------'
                #     print t.data
                #     #print dir(t)
                #     print t.seq
                #     print '-----------------'
                #     #print t.opts
