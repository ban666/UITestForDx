# -*- coding: utf-8 -*-
__author__ = 'liaoben'

from ChnlRequest import ChnlRequest
import requests
import json

def send_comment_by_proxy(coment,iid,proxy,comid=''):
    mode = 'mcp/dx'
    api = ChnlRequest(mode)
    proxy = {
        'http': 'http://'+proxy,
        'https': 'http://'+proxy
    }
    try:
        coment = coment.encode('utf-8')
    except:
        pass
    para_id = 'iid'
    para_cid = 'cid'
    data = [mode+u'/1/comm/reply',para_id+'='+str(iid),'content='+str(coment),para_cid+'='+str(comid)]
    print data

    api.model_init()
    api.gen_payload(*data)
    req = api.domain+api.path
    print req
    try:
        res = requests.post(req,data=api.payload,proxies=proxy,timeout=10)
    except Exception,e:
        print e
        return False
    if res.status_code==200:
        print 'post success'
    ret = res.content
    try:
        j_dict = json.loads(ret)
        if j_dict['code'] == 0:
            return j_dict['data']['comment']
        return False
    except Exception, e:
        print e
        return False