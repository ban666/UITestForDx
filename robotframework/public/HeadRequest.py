# -*- coding: utf-8 -*-
__author__ = 'liaoben'

'''
 * ClassName: KeyboardVoiceActivity.java
 * Company: syt
 * @author lanhm
 * @date 2015-6-19上午11:15:43
 * @version 1.0
 * Description:键盘音效
 *
 * ......................我佛慈悲......................
 *                       _oo0oo_
 *                      o8888888o
 *                      88" . "88
 *                      (| -_- |)
 *                      0\  =  /0
 *                    ___/`---'\___
 *                  .' \\|     |// '.
 *                 / \\|||  :  |||// \
 *                / _||||| -卍-|||||- \
 *               |   | \\\  -  /// |   |
 *               | \_|  ''\---/''  |_/ |
 *               \  .-\__  '-'  ___/-. /
 *             ___'. .'  /--.--\  `. .'___
 *          ."" '<  `.___\_<|>_/___.' >' "".
 *         | | :  `- \`.;`\ _ /`;.`/ - ` : | |
 *         \  \ `_.   \_ __\ /__ _/   .-` /  /
 *     =====`-.____`.___ \_____/___.-`___.-'=====
 *                       `=---='
 *
 *..................佛祖开光 ,永无BUG...................
 *
'''
from RequestForDx import RequestForDx
from DbLib import DbLib
from mongo import Mongo
import back
import requests
import json
import os


class HeadRequest(RequestForDx):

    def __init__(self,mode,ec='420000000010000',cc='420106',p='a',v='3.1.2',ak='1',dc = '1,0,0,jv5RDypcLOG1Ho6UTgf8NN5sUcLGl4Zvk2eH3fH3wEI=#5942cf325a19a9d552f2ad6b617f235e',tid='a_imei865479020303095',pid = '100d855909470b42cd9',loc = '',chnl_para='cnhubei'):
        super(HeadRequest,self).__init__(ec,cc,p,v,ak,dc,tid,pid,loc,chnl_para)
        self.mode = mode
        self.dx_mode = 'mcp/dx'
        self.dx_plug_mode = 'mcp/plug/app'

    def send_head(self,content,head_type,location,*args):
        try:
            content=content.encode('utf-8')
        except:
            pass
        data = [self.mode+u'/1/head/tipoff','content='+content,'type='+str(head_type),'location='+str(location)]
        for arg in args:
            data.append(arg)

        self.model_init()
        self.gen_payload(*data)
        req=self.domain+self.path
        for j,k in self.payload.items():
            self.payload[j]=(None,k)
        res = requests.post(req,files=self.payload)
        print 'post success'
        print 'status_code:',res.status_code
        ret = res.content
        try:
            j_dict = json.loads(ret)
            return j_dict,res.status_code
        except Exception, e:
            print e
            return ret,res.status_code

    def send_clue(self,content,subtype,pic_list=[],location='',*args):
        try:
            content=content.decode('utf-8')
            location = location.encode('utf-8')
        except:
            pass
        if type(pic_list) == unicode:
            pic_list = eval(pic_list)
        #pic_list = [os.path.abspath(x) for x in pic_list]
        #print location
        data=[self.mode+u'/1/head/tipoff','content='+str(content),'location='+str(location),'type='+str(subtype)]
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
        #print self.payload['_pic1']
        res = requests.post(req,files=self.payload)
        print 'post success'
        print 'status_code:',res.status_code
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

    def get_last_myhead_info(self,dc):
        db = DbLib()
        m = Mongo()
        if dc.find('#')!=-1:
            dc = dc.split('#')[0]
        mid = m.get_mid(dc)
        head_info = db.get_last_head_info_by_db(mid)
        return head_info

    def get_head_detail(self,cid,*args):
        data = [self.mode+u'/1/head/get','id='+str(cid)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['data']

    def get_myhead_list(self,id='',cmd='nearer',psize='20',*args):
        data = [self.mode+u'/1/user/tiplist','id='+str(id),'cmd='+cmd,'psize='+str(psize)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['data']['list']

    def review_head(self,dc,result, remark='', extra_point=0, support_base=0):
        head_info = self.get_last_myhead_info(dc)
        thumb = [dict(u=x['u'].replace('${userTipoffPath}', 'http://test.cnhubei.com/mcp/resource/tipoff/')) for x in eval(head_info['comThumb'])]
        infoid = head_info['infoid']
        print infoid
        mid = head_info['mid']
        content = head_info['content']
        result = back.review_head_by_back(infoid,mid,thumb,result,content,extra_point,remark,support_base)
        return result

    def get_head_id(self,subtype,id='',cmd='nearer',psize='20',*args):
        from ChnlRequest import ChnlRequest
        ch = ChnlRequest(self.mode,dc=self.dc)
        head_list = ch.get_head_list(subtype,id,cmd,psize,*args)
        head_list = [x.get('id') for x in head_list]
        return head_list

    #1:like 0:unlike
    def digg_for_head(self,infoid,*args):
        data = [self.mode+u'/1/news/digg','id='+str(infoid),'option=1']
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return True

    def search_head(self,word,id='',cmd='nearer',psize='20',*args):
        data = [self.mode+u'/1/head/search','word='+str(word),'id='+str(id),'cmd='+cmd,'psize='+str(psize)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['data']['list']


if __name__ == '__main__':
    head = HeadRequest('mcp/dx')
    # dc = head.dc
    # content = 'aaaaabbbbb2'
    # pic_list=['./resources/test.jpg']
    # send_ret = head.send_clue(content,2,pic_list,123)
    # print send_ret
    # review_ret = head.review_head(dc,1,'abc',1)
    # print review_ret
    # print 'myhead',head.get_last_myhead_info(dc)
    # from ChnlRequest import ChnlRequest
    # ch = ChnlRequest('mcp/dx',dc=dc)
    # head_list = ch.get_head_list('2')
    # print 'headlist',head_list[0]['id']
    head_list = head.get_myhead_list()
    print head_list