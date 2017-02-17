# -*- coding: utf-8 -*-
__author__ = 'liaoben'

from ChnlRequest import ChnlRequest

class CommentRequest(ChnlRequest):

    def get_article(self,article_id):
        data = [u'mcp/dx/2/news/getarticle','id='+str(article_id)]
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['data']['data']

    def get_focus(self,rechid=''):
        data = [u'mcp/dx/1/news/focus','rechid='+rechid]
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['data']['focus']

    def get_comment(self,id,comid='',cmd='nearer',psize='20'):
        data = [u'mcp/dx/1/comm/latest','comid='+str(comid),'id='+str(id),'cmd='+str(cmd),'psize='+str(psize)]
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result['data']['list']

    def send_comment(self,iid,coment,comid='',):
        try:
            coment = coment.encode('utf-8')
        except:
            pass
        data = [u'mcp/dx/1/comm/reply','iid='+str(iid),'content='+str(coment),'cid='+str(comid)]
        result = self.send_request_for_dx(*data)
        if result['code']=='0':
            comment_id = result['data']['comment']['id']
            return comment_id
        return result

    def digg(self,id):
        data = [u'mcp/dx/1/comm/digg','id='+str(id)]
        result = self.send_request_for_dx(*data)
        assert result['code']=='0'
        return result

    def get_first_article_for_comment(self,rechid='',id='',cmd='nearer',psize='20'):
        chnl_content = self.get_list(rechid,id,cmd,psize)
        article_list = chnl_content
        for article in article_list:
            if str(article['model'])!='4' and str(article['model'])!='5' and str(article['turnoff'])!='1':
                #print article['id'],article['title']
                return article['id']
        print 'There is no article for comment.'
        return False

    def get_article_list_for_comment(self,rechid='',id='',cmd='nearer',psize='20'):
        article_list = self.get_list(rechid,id,cmd,psize)
        ret = []
        forbidden = ['1','4','5']
        for article in article_list:
            if not str(article['model']) in forbidden and str(article['turnoff'])!='1':
                #print article['id'],article['title']
                ret.append(article)
        return ret

    def get_first_comment_for_digg(self,rechid='',id='',cmd='nearer',psize='20'):
        article_list = self.get_article_list_for_comment(rechid,id,cmd,psize)
        article_id_list = [x['id'] for x in article_list]
        for article_id in article_id_list:
            article_repcount = int(self.get_article(article_id)['repcount'])
            if article_repcount>0:
                comment_id = self.get_comment(article_id)[0]['id']
                return article_id,comment_id
        return False

    def get_type_article_list(self,article_type,rechid='',id='',cmd='nearer',psize='20'):
        article_list = self.get_list(rechid,id,cmd,psize)
        ret = []
        for article in article_list:
            if article['model'] == str(article_type):
                ret.append(article)
        return ret

    '''
    article_type
    普通网页模块	1	一般用于打开外部链接
    新闻详情模块	2	通过webview控件加载新闻内容(V2.0)，V2.1中使用HTML模块方式渲染新闻内容
    组图模块	3	组图浏览模块
    专题模块	4
    特色专栏模块	5
    活动模块	6
    原生新闻模块	7
    我的评论	8
    回复我的评论	9
    报料详情	10
    新闻评论列表	11
    报料列表	12
    视频新闻详情	13
    新闻列表	14
    地方新闻列表	15
    视频新闻列表	16
    视频直播详情	17
    特色专栏列表	18	与model:5冲突，作废
    订阅新闻列表	19	订阅新闻列表与新闻列表的主要区别是，模块中有订阅频道与取消订阅频道的功能
    订阅视频新闻列表	20	订阅视频新闻列表与视频新闻列表的主要区别是，模块中有订阅频道与取消订阅频道的功能
    支付模块	21	打开支付模块
    政情列表	22	用于显示省、市、区(县)的主政官信息列表
    政情详情页	23	用于显示主政官的相关政务信息
    '''
    def get_type_article_list_for_comment(self,article_type,rechid='',id='',cmd='nearer',psize='20'):
        article_list = self.get_type_article_list(article_type,rechid,id,cmd,psize)
        ret = []
        for article in article_list:
            if article['model'] == str(article_type) and str(article['turnoff'])!='1':
                ret.append(article['id'])
        return ret

    def get_digg_count(self,article_id,comment_id):
         comment_list = self.get_comment(article_id)
         for comment in comment_list:
             if comment['id'] == comment_id:
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
