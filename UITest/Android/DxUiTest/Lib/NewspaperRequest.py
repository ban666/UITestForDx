# -*- coding: utf-8 -*-
__author__ = 'liaoben'

from RequestForDx import RequestForDx
from DbLib import DbLib
from mongo import Mongo
import requests
import json

class NewspaperRequest(RequestForDx):

    def __init__(self,mode,ec='420000000010000',cc='420106',p='a',v='3.1.2',ak='1',dc = '1,0,0,jv5RDypcLOG1Ho6UTgf8NN5sUcLGl4Zvk2eH3fH3wEI=#5942cf325a19a9d552f2ad6b617f235e',tid='a_imei865479020303095',pid = '100d855909470b42cd9',loc = '',chnl_para='cnhubei',secret="yJfRVvn6u9yCpn"):
        super(NewspaperRequest,self).__init__(ec,cc,p,v,ak,dc,tid,pid,loc,chnl_para)
        self.mode = mode
        self.dx_mode = 'mcp/dx'
        self.dx_plug_mode = 'mcp/plug/app'
        self.default_paper = [{
                "spuid": 1,
                "name": u"人民日报"
            }, {
                "spuid": 2,
                "name": u"湖北日报"
            }, {
                "spuid": 3,
                "name": u"楚天都市报"
            }, {
                "spuid": 4,
                "name": u"楚天金报"
            }, {
                "spuid": 6,
                "name": u"长江日报"
            }]

    def get_paper_list(self,date='',spuid='',*args):
        data = [self.mode+u'/1/pager/get','date='+str(date),'spuid='+str(spuid)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['data']

    def get_paper_type_list(self,*args):
        data = [self.mode+u'/1/pager/prolist']
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['data']['list']

    def get_paper_his(self,spuid,*args):
        data = [self.mode+u'/1/pager/his','spuid='+str(spuid)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['data']['list']

    def get_paper_content(self,date='',spuid='',*args):
        content = self.get_paper_list(date,spuid,*args)
        content = eval(content['data'])['data']
        ret = []
        for i in content:
            # print i.keys()
            # print i['contents']
            tmp_ret = {}
            tmp_ret['name'] = i['name']
            tmp_ret['contents'] = []
            for j in i['contents']:
                tmp_contens_ret = {
                    'name':j['name'],
                    'readnum':j['readnum'],
                    'id':j['id']
                    }
                tmp_ret['contents'].append(tmp_contens_ret)
            ret.append(tmp_ret)
        return ret

    def get_article_for_paper(self,infoid,*args):
        data = [self.mode+u'/2/news/getarticle','id='+str(infoid)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['data']['data']

    def get_article_for_paper_old_version(self,infoid,version=9,*args):
        path = self.mode+u'/1/news/getarticle'
        if version<'2.2.0':
            path = self.mode+u'/2/news/getarticle'
        data = [path,'id='+str(infoid),'v='+str(version)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx_old_version(*data)
        assert result['code']=='0'
        return result['data']['data']

    def get_article_for_paper_old_version1(self,infoid,version,*args):
        path = self.mode+u'/1/news/getarticle'
        if version<'2.2.0':
            path = 'mcp//dx'+u'/2/news/getarticle'
        data = [path,'id='+str(infoid),'v='+str(version)]
        for arg in args:
            data.append(arg)
        self.model_init_old_version()
        self.gen_payload_old_version(*data)
        req=self.domain+self.path
        for j,k in self.payload.items():
            self.payload[j]=(None,k)
        print self.payload
        res = requests.post(req,files=self.payload)
        print 'post success'
        print 'status_code:',res.status_code
        ret = res.content
        try:
            j_dict = json.loads(ret)
            print j_dict
            if j_dict['code'] == '0':
                return True
            return False
        except Exception, e:
            print e.__repr__()
            return False

    def get_product_info(self,skuid,*args):
        data = [self.mode+u'/1/product/getsku','skuid='+str(skuid)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['data']

    def paper_kind_check(self):
        paper_kind = self.get_paper_type_list()
        result = True
        for p in self.default_paper:
            if not p in paper_kind:
                result = False
        return result

    def get_all_infoid(self,spuid='',date='',*args):
        contents = self.get_paper_content(date,spuid,*args)
        ret = [x.get('contents') for x in contents]
        id_list = []
        for i in ret:
            for j in i:
                id_list.append(j.get('id'))
        return id_list

    def get_my_paper(self,cid='',cmd='nearer',psize='20',*args):
        data = [self.mode+u'/1/user/epaperlist','id='+str(cid),'cmd='+cmd,'psize='+str(psize)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['data']['myepaper']


if __name__ == '__main__':
    a=NewspaperRequest('mcp/dx')
    pay = '''ak	1
cc	4201
dc	1,0,0,ZRI86EokopFwTupgTtln.qpv7E30B_EgIJAQcGx2x2A=#d7d5068c729407fd97d5cf2342917f45
id	811707826992058368
p	i
pid	031cdd89258
sign	d7ec42410699ef3baa662e23c0e24583
tid	e10e15efed2a140f3e3321f2b4f65c66
ts	14823766718889
v	2.1.0'''
    b = pay.split('\n')
    b = [x.replace('\t','=') for x in b]
    for i in b:
        if i.find('sign')!=-1:
            b.pop(b.index(i))
            break

    print b
    dc = ''
    t_str ='dc=1,0,0,ZRI86EokopFwTupgTtln.qpv7E30B_EgIJAQcGx2x2A=#d7d5068c729407fd97d5cf2342917f45'

    a.get_article_for_paper(811707826681679872,'hd_v=2.1.0')
    #a.get_article_for_paper_old_version()
    # ret = a.get_paper_list()
    # ret_data = eval(ret['data'])
    # data = ret_data['data']
    # #print len(data)
    # for i in data:
    #     print len(i['contents'])
    #     for j in i['contents']:
    #         print j.keys()
    # #print type(ret_data)
    # from uuid import uuid4
    # d = a.dc
    # u = str(uuid4()).replace('-','')
    # print u,len(u)
    # d2 = d.split('#')
    # d2[1] = '123'
    # d2 = '#'.join(d2)
    # print d2
    # a.dc = d2
    # #print len(d.split('#')[1])
    # ret= a.get_product_info(5)
    # for i in  ret['skuinfos'][0]['list']:
    #     print i['v'],i['k']
    # print ret[0]['contents'][0]['id']
    # ret = a.get_all_infoid()
    # print len(ret)
    # ret = [x.get('contents') for x in ret]
    # print len(ret)
    # id_list = []
    # for i in ret:
    #     for j in i:
    #         id_list.append(j.get('id'))
    # print id_list
    # print len(id_list)
    #print a.paper_kind_check()