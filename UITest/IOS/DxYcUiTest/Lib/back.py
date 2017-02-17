# -*- coding: utf-8 -*-
__author__ = 'liaoben'

import requests
import time
class BackEnd(object):

    def __init__(self):
        self._cookies={
            'JSESSIONID':'0DD1898BE1AC63924C4A143F11E4D2E1',
            '__auc':'	2ed4374a155bf49842a15ba4b00',
            '_ga':	'GA1.2.625278778.1467793114',
            'pgv_pvi':'9115965140',
            'wdcid':'23c4bd3d202d8b1d',
            'wdlast':'1464773779',
            'sessionid':'4de920331408d86ecbf07771fab1e5d4'
            }
        self.baseurl ='http://test.cnhubei.com/mcp/con/partner/'


    def send_request(self,req,payload):
        res = requests.post(req,data=payload,cookies=self._cookies)
        ret = res.content
        return ret




def review_head_by_back(infoid,mid,thumb,result,content,extra_point=0,remark='',support_base=0,reply_txt=''):
        back = BackEnd()
        req = back.baseurl+'clue/audit?ts='+str(int(time.time()*1000))
        payload = {
            'clue.extraPoint':extra_point,
            'clue.supportBase':support_base,
            'clue.content':content,
            'clue.remark':remark,
            'clue.thumb':thumb,
            'clue.infoid':infoid,
            'clue.mid':mid,
            'clue.replytxt':reply_txt,
            'result':result
        }
        #print thumb
        if thumb == []:
            payload['clue.thumb'] = '[]'
        if int(extra_point) == 0:
            payload.pop('clue.extraPoint')
        #print payload
        ret =  back.send_request(req,payload)
        return ret


if __name__ == '__main__':
    # src= 'http://96.f.1ting.com/58199bf7/c66e2cd70de903e6943fd8145a6ecc71/zzzzzmp3/2013kNov/12W/12xuezhiqian/03.mp3'
    # data = '{"poster":"http://media.v.cnhubei.com:85/jcw/upload/Image/default/2016/11/02/08d39f313bf842d8b53d5f765ea7a827/5804a755-5379-491b-af4b-0bd4cfd91964.jpg","src":"%s","live":"0"}' % src
    #
    #
    # payload = {
    # 'article.title':'test_audio_article',
    # 'article.thumb':'\[\]',
    # 'article.pageViewBase':3625,
    # 'flag':0,
    # 'style':1,
    # 'article.releaseTime':'',
    # 'article.summary':'',
    # 'article.author':'',
    # 'article.content':'<p><div cnhubei_data_type="audio" data="%s" class="cnhubei_audio"><img parent="audio" src="http://media.v.cnhubei.com:85/jcw/upload/Image/default/2016/11/02/08d39f313bf842d8b53d5f765ea7a827/5804a755-5379-491b-af4b-0bd4cfd91964.jpg"><span></span></div><br></p>' % data,
    # 'article.insotxt':'',
    # 'article.oppositionBase':10,
    # 'article.supportBase':295,
    # 'article.targetUrl':'',
    # 'cateid':672678215164366848,
    # 'rechid':672678215181144064,
    # 'place':''
    # }
    # back = BackEnd()
    # req = 'http://test.cnhubei.com/mcp/con/dx/info/saveArticle?ts='+str(int(time.time()*1000))
    # ret =  back.send_request(req,payload)
    # print ret
    pass