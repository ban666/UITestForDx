# -*- coding: utf-8 -*-
__author__ = 'liaoben'

from RequestForDx import RequestForDx
from DbLib import DbLib
from mongo import Mongo
import back
import requests
import json
import os
from ChnlRequest import ChnlRequest
from config import *
#from common import gen_dc

class BaoliaoRequest(RequestForDx):

    def __init__(self,ec=str(EC),cc='420106',p='a',v='3.1.2',ak=str(AK),dc = '1,0,0,jv5RDypcLOG1Ho6UTgf8NN5sUcLGl4Zvk2eH3fH3wEI=#123',tid='a_imei865479020303095',pid = '100d855909470b42cd9',loc = '',chnl_para='cnhubei',secret="dJEeE#dIRq"):
        super(BaoliaoRequest,self).__init__(ec,cc,p,v,ak,dc,tid,pid,loc,chnl_para,secret)

    def get_clue_type(self,*args):
        data = [u'mcp/plug/app/1/clue/subtype']
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['data']['list']

    def get_clue_list(self,subtype,cid='',cmd='nearer',psize='20',*args):
        data = [u'mcp/plug/app/1/clue/list','subtype='+str(subtype),'cid='+str(cid),'cmd='+cmd,'psize='+str(psize)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['data']['list']



    def get_clue_info(self,cid,*args):
        data = [u'mcp/plug/app/1/clue/info','cid='+str(cid)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['data']

    def send_clue(self,content,subtype,anony = 0,pic_list=[],location='',*args):
        try:
            content=content.encode('utf-8')
        except:
            pass
        if type(pic_list) == unicode:
            pic_list = eval(pic_list)
        data=['plug/app/1/clue/reply','content='+str(content),'location='+location,'subtype='+str(subtype),'anony='+str(anony)]
        for arg in args:
            data.append(arg)
        self.model_init()
        self.gen_payload(*data)
        req=self.domain+self.path
        #pic_list = [os.path.split(x) for x in pic_list]
        #print pic_list
        for j,k in self.payload.items():
            self.payload[j]=(None,k)
        if len(pic_list)!= 0:
            for l in range(len(pic_list)):
                t_str='_pic'+str(l+1)
                self.payload[t_str]=(os.path.split(pic_list[l])[0],open(pic_list[l], 'rb'), 'image/jpg')
        #print self.payload
        res = requests.post(req,files=self.payload)
        # print 'post success'
        # print 'status_code:',res.status_code
        ret = res.content
        try:
            j_dict = json.loads(ret)
            #print j_dict
            if j_dict['code'] == '0':
                return True
            return False
        except Exception, e:
            print e.__repr__()
            return False

    def search_clue(self,word,cid='',cmd='nearer',psize='20',*args):
        data = [u'mcp/plug/app/1/clue/srh','word='+str(word),'id='+str(cid),'cmd='+cmd,'psize='+str(psize)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        #print result
        assert result['code']=='0'
        return result['data']['list']

    def get_dx_head_list(self,cateid):
        dc = self.dc
        ch = ChnlRequest('mcp/dx',ak='1',secret='yJfRVvn6u9yCpn',dc=dc,ec='420000000010000',cc='420106',v='3.2.1')
        head_list = ch.get_head_list(cateid=str(cateid),psize=1000)
        return head_list

    def get_all_dx_head_id(self):
        ret = []
        for i in range(1,4,1):
            ret.extend(self.get_dx_head_list(i))
        ret =[x['id'] for x in ret]
        #print ret
        return ret

    def get_all_yc_head_id(self):
        ret = []
        for i in range(4,8):
            ret.extend(self.get_clue_list(i,psize=1000))
        #print ret[0].keys()
        ret =[x['cid'] for x in ret]
        #print ret
        return ret

    def get_intersection_of_head_for_dx_yc(self):
        dx_head = self.get_all_dx_head_id()
        yc_head = self.get_all_yc_head_id()
        intersection = set(dx_head) & set(yc_head)
        return intersection

    # def get_all_id(self,content):
    #     content = [x.get('cid') for x in content]
    #     return  content

    def get_dx_my_clue_list(self):
        dc = gen_dc(self.dc)
        yc = BaoliaoRequest(ak='1',secret='yJfRVvn6u9yCpn',dc=dc,ec='420000000010000',cc='420106',v='3.2.1')
        head_list = yc.get_my_clue_list_for_yc(psize='1000')
        head_list = [x['id'] for x in head_list]
        return head_list

    def get_my_clue_list_for_yc(self,id='',cmd='nearer',psize='20',*args):
        data = [u'mcp/dx/1/user/tiplist','id='+str(id),'cmd='+str(cmd),'psize='+str(psize)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['data']['list']

    def get_yc_my_clue_list(self):
        head_list = self.get_my_clue_list_for_yc(psize=1000)
        head_list = [x['id'] for x in head_list]
        return head_list

    def get_intersection_of_my_clue_for_dx_yc(self):
        dx_head = self.get_dx_my_clue_list()
        yc_head = self.get_yc_my_clue_list()
        print dx_head
        print yc_head
        intersection = set(dx_head) & set(yc_head)
        return intersection

    def get_last_myhead_info(self,dc):
        db = DbLib()
        m = Mongo()
        if dc.find('#')!=-1:
            dc = dc.split('#')[0]
        mid = m.get_mid(dc)
        head_info = db.get_last_head_info_by_db(mid)
        return head_info

    def review_head(self,dc,result, remark='', extra_point=0, support_base=0,reply=''):
        head_info = self.get_last_myhead_info(dc)
        thumb = [dict(u=x['u'].replace('${userTipoffPath}', 'http://test.cnhubei.com/mcp/resource/tipoff/')) for x in eval(head_info['comThumb'])]
        infoid = head_info['infoid']
        #print infoid
        mid = head_info['mid']
        content = head_info['content']
        result = back.review_head_by_back(infoid,mid,thumb,result,content,extra_point,remark,support_base,reply)
        return result

    def send_clue_and_review(self,content,result,subtype=4,anony = 0,pic_list=[],location='', remark='', extra_point=0, support_base=0,reply='',*args):
        self.send_clue(content,subtype,anony,pic_list,location,*args)
        self.review_head(self.dc,result,remark,extra_point,support_base,reply)


if __name__ == '__main__':
    bl =  BaoliaoRequest(dc='1,0,0,jv5RDypcLOG1Ho6UTgf8NN5sUcLGl4Zvk2eH3fH3wEI=#c3b2f34fd50d4ab494847f7699970aee')
    # t = bl.get_clue_type()
    # bl.send_clue('123',t[0]['subtype'])
    # bl.review_head(bl.dc,1)
    #bl.send_clue_and_review('456',1)
    l = bl.get_clue_list(4)
    print l[0]['cid']
    mode = 'mcp/plug/app'
    ch = ChnlRequest(mode)
    for i in range(50):
        ch.send_comment(l[0]['cid'],'aaa')
    # path = []
    # # bl.send_clue('1234',4)
    # # yc =  bl.get_yc_my_clue_list()
    # # dx = bl.get_dx_my_clue_list()
    # # print len(yc)
    # # print yc==dx
    # # print yc[0]
    # # print dx[0]
    # # c = bl.get_intersection_of_my_clue_for_dx_yc()
    # # print len(c)
    # for i in range(1,10,1):
    #     path.append('g:/img/'+str(i)+'.jpg')
    # #print path
    # for j in range(10):
    #     for i in range(4,8,1):
    #         pass
    #         bl.send_clue('1234'+str(i),i,0,path,'','hd_dc=1,0,0,jv5RDypcLOG1Ho6UTgf8NN5sUcLGl4Zvk2eH3fH3wEI=#bb72796c971f782f4f4b989bdea6ba27')
    #         #bl.send_clue('123'+str(i),i)
    # print bl.get_clue_type()
    # info = bl.get_clue_list(4)[0]
    # for i,j in info.items():
    #     print i,j
    # info =  bl.get_clue_info(804237029423714304)
    # for i,j in info.items():
    #     print i,j
    #print bl.search_clue('123')[0]['cid']
    #dx_head = bl.get_all_dx_head_id()
    # print len(dx_head)
    # clue = bl.get_intersection_of_head_for_dx_yc()
    #print len(clue)