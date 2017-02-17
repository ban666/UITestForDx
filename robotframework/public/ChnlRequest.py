# -*- coding: utf-8 -*-
__author__ = 'liaoben'

from RequestForDx import RequestForDx
import re
import chardet
from common import unicode_to_str
from random import randint
from DbLib import DbLib
import requests
import json


class ChnlRequest(RequestForDx):

    def __init__(self,mode,ec='420000000010000',cc='420106',p='a',v='3.1.2',ak='1',dc = '1,0,0,suiZBeeEhYc391o8NI6samFpGXp8kd8L0ALLxd7Tt5Q=#af65396ebb49846daf9d98343c34f184',tid='a_imei865479020303095',pid = '100d855909470b42cd9',loc = '',chnl_para='cnhubei',secret="yJfRVvn6u9yCpn"):
        super(ChnlRequest,self).__init__(ec,cc,p,v,ak,dc,tid,pid,loc,chnl_para,secret)
        self.mode = mode
        self.dx_mode = 'mcp/dx'
        self.dx_plug_mode = 'mcp/plug/app'
        self.param_list = {
            self.dx_mode:{
                'rech_id':'rechid',
                'sp_id':'id',
                'article_id':'id',
                'ph_id':'id',
                'com_id':'id',
                'ret_focus':['data','focus']
            },
            self.dx_plug_mode:{
                'rech_id':'chnlid',
                'sp_id':'spid',
                'article_id':'infoid',
                'ph_id':'phid',
                'com_id':'comid',
                'ret_focus':['data','list']
            }
        }

    def chnl(self,*args):
        data = [self.mode+u'/1/news/chnl']
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        if self.mode != self.dx_mode:
            assert not result['data'].has_key('sub')
            result['data']['sub'] = result['data']['list']
        return result['data']

    def get_list(self,rechid='',id='',cmd='nearer',psize='20',*args):
        data = [self.mode+u'/1/news/list', self.param_list[self.mode]['rech_id']+'='+str(rechid),self.param_list[self.mode]['article_id']+'='+str(id),'cmd='+cmd,'psize='+str(psize)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        print result
        assert result['code']=='0'
        return result['data']['list']


    #2:普通文字新闻
    #3:组图
    #4:专栏
    #5:专题
    #13:视频
    #17:直播视频
    #22:音频
    def get_article(self, article, id='', cmd='nearer', psize='20',*args):
        if self.mode == self.dx_plug_mode:
            article['id'] = article['infoid']
        para_rechid = {
            self.dx_mode:'rechid',
            self.dx_plug_mode:'chnlid'
        }
        para_spid = {
            self.dx_mode:'id',
            self.dx_plug_mode:'spid'
        }
        para_id = {
            self.dx_mode:'id',
            self.dx_plug_mode:'infoid'
        }
        para_phid = {
            self.dx_mode:'id',
            self.dx_plug_mode:'phid'
        }
        dx_method = {
            '5':[self.mode+u'/1/news/list',para_rechid[self.mode]+'='+str(article['rechid']),para_id[self.mode]+'='+str(id),'cmd='+cmd,'psize='+str(psize)],
            '4':[self.mode+u'/1/news/sp',para_spid[self.mode]+'='+str(article['id'])],
            '2':[self.mode+u'/2/news/getarticle',para_id[self.mode]+'='+str(article['id'])],
            '3':[self.mode+u'/1/news/ph',para_id[self.mode]+'='+str(article['id'])],
            '13':[self.mode+u'/1/news/getvideo',para_id[self.mode]+'='+str(article['id'])],
            '17':[self.mode+u'/2/news/getarticle',para_id[self.mode]+'='+str(article['id'])],
            '25':[self.mode+u'/3/news/audio','infoid='+str(article['id'])]
        }

        if self.mode == self.dx_plug_mode:
            dx_method['25'] = [self.mode+u'/1/news/audio',para_id[self.mode]+'='+str(article['infoid'])]
            dx_method['17'] = [self.mode+u'/1/news/getarticle',para_id[self.mode]+'='+str(article['id'])]
            dx_method['13'] = [self.mode+u'/1/news/video',para_id[self.mode]+'='+str(article['infoid'])]
            dx_method['3'] = [self.mode+u'/1/news/photos',para_phid[self.mode]+'='+str(article['infoid'])]
            dx_method['2'] = [self.mode+u'/1/news/getarticle',para_id[self.mode]+'='+str(article['id'])]
        if dx_method.has_key(str(article['model'])):
            data = dx_method[str(article['model'])]
        else:
            print '当前版本不支持此model'.decode('utf-8')
            return False
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        if article['model'] == '5':
            return result['data']['list']
        dx_ret = {
            '5':{self.dx_mode:['data', 'list'], self.dx_plug_mode:['data', 'list']},
            '4':{self.dx_mode:['data','data'],self.dx_plug_mode:['data','sp']},
            '2':{self.dx_mode:['data','data'],self.dx_plug_mode:['data','article']},
            '3':{self.dx_mode:['data','data'],self.dx_plug_mode:['data','photos']},
            '13':{self.dx_mode:['data','data'],self.dx_plug_mode:['data','video']},
            '17':{self.dx_mode:['data','data'],self.dx_plug_mode:['data','article']},
            '25':{self.dx_mode:['data','audio'],self.dx_plug_mode:['data','audio']}
        }
        print 'model',str(article['model'])
        print 'mode',self.mode
        ret = dx_ret[str(article['model'])][self.mode]
        return result[ret[0]][ret[1]]



    def get_head_list(self,cateid='1',id='',cmd='nearer',psize='20',*args):
        data = [self.mode+u'/1/head/list','cateid='+str(cateid),'id='+str(id),'cmd='+cmd,'psize='+str(psize)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['data']['list']

    def get_head(self,id,*args):
        data = [self.mode+u'/1/head/list','id='+str(id)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['data']['clue']

    def get_focus(self,rechid='',psize=10,*args):
        if self.mode == self.dx_mode:
            data = [self.mode+u'/1/news/focus','rechid='+str(rechid)]
        elif self.mode == self.dx_plug_mode:
            data = [self.mode+u'/1/news/focus','chnlid='+str(rechid),'psize='+str(psize)]
        else:
            return False
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        ret = self.param_list[self.mode]['ret_focus']
        return result[ret[0]][ret[1]]

    def get_comment(self,id,comid='',cmd='nearer',psize='20',*args):
        dx_method = {
            self.dx_mode:[self.mode+u'/1/comm/latest',self.param_list[self.mode]['com_id']+'='+str(comid),'id='+str(id),'cmd='+str(cmd),'psize='+str(psize)],
            self.dx_plug_mode:[self.mode+u'/1/comm/list','comid='+str(comid),'infoid='+str(id),'cmd='+str(cmd),'psize='+str(psize)]
        }
        data = dx_method[self.mode]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['data']['list']

    def get_top(self,id,psize='20'):
        id_args = 'id'
        if self.mode == self.dx_plug_mode:
            id_args = 'infoid'
        data = [self.mode+u'/1/comm/top',id_args+'='+str(id),'psize='+str(psize)]
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['data']['list']

    def send_comment(self,iid,coment,comid='',*args):
        try:
            coment = coment.encode('utf-8')
        except:
            pass
        para_id = 'iid'
        para_cid = 'cid'
        if self.mode != self.dx_mode:
            para_id = 'infoid'
            para_cid = 'comid'
        print chardet.detect(coment)
        data = [self.mode+u'/1/comm/reply',para_id+'='+str(iid),'content='+str(coment),para_cid+'='+str(comid)]
        print data
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        ret = {
            self.dx_mode:['comment','id'],
            self.dx_plug_mode:['comm','comid']
        }
        if result['code']=='0':
            comment_id = result['data'][ret[self.mode][0]][ret[self.mode][1]]
            return comment_id
        return result

    def digg(self,id,*args):
        data = [self.mode+u'/1/comm/digg',self.param_list[self.mode]['com_id']+'='+str(id)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result

    def get_hotwords(self,*args):
        data = [self.mode+u'/1/news/hot']
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result

    def search(self,keywords,id='', cmd='nearer', psize='20',*args):
        #print chardet.detect(keywords)
        try:
            keywords = keywords.encode('utf-8')
        except:
            pass
        data = [self.mode+u'/1/news/search','word='+keywords,'id='+str(id),'cmd='+cmd,'psize='+str(psize)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        if result['code']=='0':
            return result['data']['list']
        return result

     #1:like 0:unlike
    def digg_for_article(self,infoid,option,*args):
        data_dict = {
            self.dx_mode:[u'mcp/jsapi/digg','paras={\"id\":\"%s\",\"option\":\"%s\"}'%(str(infoid),str(option))],
            self.dx_plug_mode:[self.mode+u'/1/news/digg','infoid='+str(infoid),'option='+str(option)]
        }
        data = data_dict[self.mode]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return True



    def get_bullet(self,id,*args):
        data = [self.mode+u'/1/news/getbullet','id='+str(id)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['data']['list']

    def add_bullet(self,content,infoid,id,vtime,*args):
        try:
            content = content.encode('utf-8')
        except:
            pass
        data = [self.mode+u'/1/news/addbullet','infoid='+str(infoid),'id='+str(id),'vtime='+str(vtime),'content='+str(content)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return True

    def change_city_and_check_article(self,city_information_force,city_information,ec,cc):
        chnl_list=self.chnl('hd_ec='+ec,'hd_cc='+cc)
        if self.mode != self.dx_mode:
            chnl_list['sub'] = chnl_list['list']
        for chnl in chnl_list['sub']:
            if int(chnl['sortNum']) not in [10,20]:
                rechid = chnl['id']
                print chnl['title']
                break

        article_list = self.get_list(rechid,'','nearer','20','hd_ec='+ec,'hd_cc='+cc)
        info_list = city_information[0]
        if len(city_information_force)!=0:
            info_list = city_information_force[0]
        expect_info=article_list[5]
        compart_list = ['id','title']
        expect_info_list = []
        for key in compart_list:
            expect_info_list.append(expect_info.get(key))
        print info_list[1],expect_info_list[1]
        print info_list[0],expect_info_list[0]
        expect_info_list = [unicode_to_str(x) for x in expect_info_list]
        info_list = [unicode_to_str(x) for x in info_list]
        result =  tuple(info_list)==tuple(expect_info_list)
        print result
        return result

    def get_article_by_model(self,model,rechid='',id='',cmd='nearer',psize='20'):
        chnl_content = self.get_list(rechid,id,cmd,psize)
        article_list = chnl_content
        ret = []
        for article in article_list:
            if str(article['model']) == str(model):
                ret.append(article)
        return ret

    def get_article_by_id(self,infoid,rechid='',id='',cmd='nearer',psize='20'):
        chnl_content = self.get_list(rechid,id,cmd,psize)
        article_list = chnl_content

        for article in article_list:
            if str(article.get('id')) == str(infoid) or str(article.get('infoid')) == str(infoid):
                print article
                return article
        return False

    def get_first_article_for_comment(self,rechid='',id='',cmd='nearer',psize='20'):
        chnl_content = self.get_list(rechid,id,cmd,psize)
        article_list = chnl_content
        forbidden = ['1','4','5']
        if self.mode == self.dx_mode:
            forbidden.append('25')
        for article in article_list:
            if not str(article['model']) in forbidden and int(article['turnoff']) % 2 == 0 and article['targeturl'] == '':
                if self.mode != self.dx_mode:
                    return article['infoid']
                #print article['id'],article['title']
                return article['id']
        print 'There is no article for comment.'
        return False

    def get_first_chnl_article_for_comment(self,*args):
        if self.mode == self.dx_mode:
            chnl_id = self.chnl()['sub'][0]['id']
        elif self.mode == self.dx_plug_mode:
            chnl_id = self.chnl()['data']['list']['0']
        else:
            print 'mode is wrong!'
            return False
        print chnl_id
        ret = self.get_first_article_for_comment(chnl_id,*args)
        return ret

    def get_article_list_for_comment(self,rechid='',id='',cmd='nearer',psize='20'):
        article_list = self.get_list(rechid,id,cmd,psize)
        ret = []
        forbidden = ['1','4','5']
        if self.mode == self.dx_mode:
            forbidden.append('25')
        for article in article_list:
            if not str(article['model']) in forbidden and int(article['turnoff']) % 2 == 0 and article['targeturl'] == '':
                #print article['id'],article['title']
                ret.append(article)
        return ret

    def get_head_list_for_comment(self,cateid='1',id='',cmd='nearer',psize='20',*args):
        head_list = self.get_head_list(cateid,id,cmd,psize,*args)
        ret = []
        for head in head_list:
            if str(head['turnoff'])!='1':
                ret.append(head)
        return ret

    def get_first_comment_for_digg(self,rechid='',id='',cmd='nearer',psize='20'):
        article_list = self.get_article_list_for_comment(rechid,id,cmd,psize)
        #article_id_list = [x['id'] for x in article_list]
        para_id = {
            self.dx_mode:'id',
            self.dx_plug_mode:'infoid'
        }
        para_comid = {
            self.dx_mode:'id',
            self.dx_plug_mode:'comid'
        }
        for article_id in article_list:
            article_content = self.get_article(article_id)
            article_repcount = int(article_content['repcount'])
            if article_repcount>0:
                comment_id = self.get_comment(article_id[para_id[self.mode]])[0][para_comid[self.mode]]
                return article_id[para_id[self.mode]],comment_id
        return False

    def get_type_article_list(self,article_type,rechid='',id='',cmd='nearer',psize='20'):
        article_list = self.get_list(rechid,id,cmd,psize)
        ret = []
        for article in article_list:
            if str(article['model']) == str(article_type):
                ret.append(article)
        return ret

    '''
    index name model
    1	普通网页模块	1	外链新闻，没有底部工具栏
    2	新闻详情模块	2
    3	组图模块	3
    4	专题模块	4
    5	特色专栏模块	5
    6	活动模块	6
    7	原生新闻模块	7
    8	我的评论	8
    9	回复我的评论	9
    10	报料详情	10
    11	新闻评论列表	11
    12	报料列表	12
    13	视频新闻详情	13
    14	新闻列表	14
    15	地方新闻列表	15
    16	视频新闻列表	16
    17	视频直播详情	17
    18	特色专栏列表	18
    19	订阅新闻列表	19
    20	订阅视频新闻列表	20
    21	支付模块	21
    22	政情列表	22	用于显示省、市、区(县)的主政官信息列表
    23	政情详情页	23	用于显示主政官的相关政务信息
    24	外链新闻	24	用于打开外链新闻，有底部工具栏，二次加载
    25	音频详情	25
    '''
    def get_type_article_list_for_comment(self,article_type,rechid='',id='',cmd='nearer',psize='20'):
        article_list = self.get_type_article_list(article_type,rechid,id,cmd,psize)
        ret = []
        print len(article_list)
        for article in article_list:
            if str(article['model']) == str(article_type) and str(article['turnoff'])!='1':
                ret.append(article[self.param_list[self.mode]['article_id']])
        return ret

    def get_digg_count(self,article_id,comment_id):
         comment_list = self.get_comment(article_id)
         for comment in comment_list:
             if comment[self.param_list[self.mode]['com_id']] == comment_id:
                 return comment['digg']

    def get_latest_comment(self,id,comid='',cmd='nearer',psize='20'):
        ret = self.get_comment(id,comid,cmd,psize)
        return ret[0]

    def get_quote(self,quote):
        try:
            quote = quote[0].encode('utf-8')
        except:
            pass
        print 'quote,',quote
        print 'quote,', type(quote)
        cmid_pattern = r'\"comid\":([0-9]+),'
        content_pattern = r'\"content\":(\S+),'
        cmid = re.findall(cmid_pattern,quote)[0]
        content = re.findall(content_pattern,quote)[0].strip("\"")
        return long(cmid),content

    def get_my_comm(self,id='',cmd='nearer',psize='20',*args):
        data = [self.dx_mode+u'/1/user/comlist','id='+str(id),'cmd='+str(cmd),'psize='+str(psize)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['data']['list']

    def get_my_recomm(self,id='',cmd='nearer',psize='20',*args):
        data = [self.dx_mode+u'/1/user/recomlist','id='+str(id),'cmd='+str(cmd),'psize='+str(psize)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['data']['list']

    def get_bullet_by_article(self,article):
        id = re.findall(r'uricode=(\w+)',article['sourceurl'])
        if len(id)!=1:
            return False
        id = id[0]
        return self.get_bullet(id)

    def get_first_video_and_add_bullet(self,content,rechid='',id='',cmd='nearer',psize='20',*args):
        first_video = self.get_article_by_model('13',rechid,id,cmd,psize,*args)[0]
        info_id = first_video[self.param_list[self.mode]['article_id']]
        print first_video
        url_id = re.findall(r'uricode=(\w+)',first_video['sourceurl'])[0]
        vtime = randint(1,int(first_video['duration']))

        assert self.add_bullet(content,info_id,url_id,vtime,*args)
        return url_id,vtime

    def check_bullet_from_db_and_delete(self,urlid,vtime,content):
        db= DbLib()
        latest_danmu = db.get_latest_danmu_by_db()
        print  latest_danmu['content'] == content
        print  latest_danmu['timePoint'] == long(vtime)
        if latest_danmu['content'] == content and latest_danmu['timePoint'] == long(vtime) and \
            latest_danmu['uricode'] == urlid:
            db.del_latest_danmu_by_db(latest_danmu['dmkid'])
            return True
        return False

    def get_article_num(self,ak=1,cc=420100,version='dx'):
        db= DbLib()
        num_list = db.get_article_num_by_db(ak,cc,version)
        return num_list

    def get_rechid_by_limit(self,compare_num,num_list):
        for rechid,num in num_list.items():
            if int(num) > int(compare_num):
                return rechid,num

    def get_focus_num(self,ak=1,cc=420100,version='dx'):
        db= DbLib()
        num_list = db.get_focus_num_by_db(ak,cc,version)
        return num_list

    def get_digg_for_article(self,content):
        print content
        digg = content['data']['digg']
        like_pattern = r'</span> <span id=\"count_like_article\">([0-9]+)</span>'
        unlike_pattern = r'<span id=\"count_unlike_article\">([0-9]+)</span>'
        like_digg = re.findall(like_pattern,digg)[0]
        unlike_digg = re.findall(unlike_pattern,digg)[0]
        return int(like_digg),int(unlike_digg)

    def get_hotword_by_db_and_check_ret(self):
        db= DbLib()
        print self.ak
        db_ret = db.get_hotwords_by_db(self.ak)
        hotword_db_list = [x['word'].decode('utf-8') for x in db_ret]
        result = self.get_hotwords()['data']['list']
        for i in range(len(result)):
            print hotword_db_list[i],result[i]
        return result==hotword_db_list

    def get_comment_by_id(self,id,comment_id,comid='',cmd='nearer',psize='20',*args):
        comment_list = self.get_comment(id,comid,cmd,psize,*args)
        for comment in comment_list:
            if comment['id'] == comment_id:
                return comment
        return 0

    def rb(self,infoid,option,*args):
        data = [self.mode+u'/3/news/rb','infoid='+str(infoid),'option='+str(option)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return True

    def get_first_article_and_share(self,*args):
        chnl = self.chnl(*args)
        article_list = self.get_list(chnl['sub'][0])
        for article in article_list:
            if int(article['turnoff']) >=0 and int(article['turnoff']) <8:
                share_article = article
                share_ret = self.rb(share_article['id'],1,*args)
                assert share_ret
                return True
        return False

    def send_comment_by_proxy(self,coment,iid,proxy,comid=''):
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
        if self.mode != self.dx_mode:
            para_id = 'infoid'
            para_cid = 'comid'
        ret_str = {
            self.dx_mode:'comment',
            self.dx_plug_mode:'comm'
        }
        data = [self.mode+u'/1/comm/reply',para_id+'='+str(iid),'content='+str(coment),para_cid+'='+str(comid)]
        print data

        self.model_init()
        self.gen_payload(*data)
        req = self.domain+self.path
        print req
        try:
            res = requests.post(req,data=self.payload,proxies=proxy,timeout=10)
        except Exception,e:
            print e
            return False
        if res.status_code==200:
            print 'post success'
        ret = res.content
        try:
            j_dict = json.loads(ret)
            if j_dict['code'] == '0':
                return j_dict['data'][ret_str[self.mode]]
            print j_dict
            return False
        except Exception, e:
            print e.__repr__()
            return False

    def check_comment_location(self, coment, iid, proxy, location, comid=''):
        ret = self.send_comment_by_proxy(coment,iid,proxy,comid)
        try:
            location = location.decode('utf-8')
        except:
            pass
        print ret.get('loc')
        if ret.get('loc') == location:
            return  True
        return  False

    def add_chnl(self,chnlid,add=0,*args):
        data = [self.dx_mode+u'/1/news/subchnl','chnl='+str(chnlid),'add='+str(add)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['data']['channels']

    def chnl_pop_city(self,*args):
        chnl = self.chnl(*args)
        for i in chnl['sub']:
            if int(i.get('sortNum')) == 0:
                chnl['sub'].pop(chnl['sub'].index(i))
                break
        return chnl

    def sub_sta(self,chnlid,*args):
        data = [self.dx_mode+u'/1/news/substa','chnl='+str(chnlid)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['data']

    def unsub_chnl(self,chnlid,*args):
        data = [self.dx_mode+u'/1/news/unsubchnl','chnl='+str(chnlid)]
        for arg in args:
            data.append(arg)
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['data']

if __name__ == '__main__':
    api = ChnlRequest('mcp/dx',dc='1,0,0,jv5RDypcLOG1Ho6UTgf8NN5sUcLGl4Zvk2eH3fH3wEI=#5e9aa5554c03189c306b2ef944aa2334')
    db = DbLib()
    dc = api.dc
    ec= api.ec
    cc = 420106
    sub = db.get_sub_able_chnl(dc,ec,cc)
    old = db.get_subchnl_by_db(dc,ec,cc)
    add = api.add_chnl(sub[0],1)
    force = db.get_force_chnl(ec,cc)
    print force
    chnl = api.chnl()
    force.extend(old)
    force.append(sub[0])
    from common import get_all_id
    id_list = get_all_id(chnl['sub'])
    print sub[0]
    print id_list
    print force
    print id_list == force
    #api.add_chnl()
    # db = DbLib()
    # infoid = db.get_infoid_by_article_name('自动化评论测试')
    # print infoid
    # top = api.get_top(infoid)
    # print top[0]
    # print len(top)
    #top =  api.send_comment_by_proxy('a',infoid,proxy='202.171.253.72:80')
    #print api.check_comment_location('a',infoid,'202.171.253.72:80','澳门')
    # first_video = api.get_article_by_id(795444250253987840,750142796387848192)
    # print first_video
    # info_id = first_video[api.param_list[api.mode]['article_id']]
    # print info_id
    # print 1
    # print first_video
    # url_id = re.findall(r'uricode=(\w+)',first_video['sourceurl'])[0]
    # vtime = randint(1,int(first_video['duration']))
    # for i in range(30):
    #     content = 'test'+str(i)
    #     api.add_bullet(content,info_id,url_id,2)
    # t_str = 'jingcai pinglun '
    # infoid = '799416572975517696'
    # for i in range(5,12,1):
    #     print i
    #     content = t_str +str(i)
    #     t_id =  api.send_comment(infoid,content)
    #     zan = 34-i
    #     print content,zan
    #     db.set_digg_count_by_db(t_id,zan)
    '''
    chnl_list = api.chnl()['list'][0]
    a,b,c = api.get_first_video_and_add_bullet('啦啦啦',chnl_list['id'])
    print a,b,c
    print api.get_bullet(a)
    print api.check_bullet_from_db_and_delete(a,b,c)
        '''
    # r = api.get_first_article_and_share()
    # print r
    '''
    print len(chnl_list)
    art_list = api.get_article_by_model('2',chnl_list['id'])
    art_content = api.get_article(art_list[0])
    infoid = art_list[0]['infoid']
    ld,ud = api.get_digg_for_article(art_content)
    print ld,ud
    api.digg_for_article(infoid,0)
    art_content = api.get_article(art_list[0])
    ld,ud = api.get_digg_for_article(art_content)
    print ld,ud
    api.digg_for_article(infoid,1)
    art_content = api.get_article(art_list[0])
    ld,ud = api.get_digg_for_article(art_content)
    print ld,ud
    '''
    '''
    foc = api.get_focus(rid)
    print len(foc)
    '''