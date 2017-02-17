# -*- coding: utf-8 -*-
__author__ = 'liaoben'

from db import DxDb
from datetime import datetime,timedelta

class DbLib(DxDb):

    def get_latest_danmu_by_db(self):
        self.connect()
        sql_str = 'select dmkid,uricode,timePoint,content,createTime from danmaku order by createTime desc limit 1'
        r = self.do(sql_str)
        self.disconn()
        return r[0]

    def del_latest_danmu_by_db(self,dmkid):
        self.connect()
        print dmkid
        sql_str = 'delete from danmaku where dmkid = %s '%(str(dmkid))
        r = self.do(sql_str)
        self.disconn()
        return True


    def get_chnl_by_db(self,ak,cc,version='dx'):
        self.connect()
        if cc=='' or isinstance(cc,type(None)):
            cc=420100
        domid = self.do('SELECT domainCode as ec from domain,apps where apps.appid=%s and apps.domid=domain.domid' % (ak))
        sql_str = {
            'dx':'select rechid,name,flag,model from domain_released_channel where z in (%s,%s) and state=30 and not drccid=0 and sortNum in \
                 (\'10\',\'20\',\'30\',\'40\') order by sortNum,sort3 desc' % (domid[0]['ec'],str(cc)),
            'plug':'select rechid,name,flag,model from domain_released_channel where z in (%s,%s) and \
                 state=30 and not drccid=0 and sortNum in (\'10\',\'20\',\'30\',\'40\',\'50\',\'60\') order by \
                   sortNum,sort3 desc' % (domid[0]['ec'],str(cc))
        }

        print sql_str[version]
        print version
        print sql_str.has_key(version)
        r = self.do(sql_str[version])
        self.disconn()
        return r


    def get_article_list_by_db(self,rechid):
        self.connect()
        column = '*'
        sql_str = 'select %s from information where cateid = (select cateid2 from released_channel where  \
                  rechid = %s) ORDER BY sort3 desc' % (column,str(rechid));
        r = self.do(sql_str)
        self.disconn()
        return r

    def get_article_num_by_db(self,ak,cc,version='dx'):
        chnl_list = [x['rechid'] for x in self.get_chnl_by_db(ak,cc,version)]
        ret = {}
        for chnl in chnl_list:
            ret[chnl] = len(self.get_article_list_by_db(chnl))
        return ret

    def get_focus_list_by_db(self,rechid,ak):
        self.connect()
        domid = self.do('SELECT domainCode as ec from domain,apps where apps.appid=%s and apps.domid=domain.domid' % (ak))
        column = '*'
        sql_str = 'select %s from information where cateid = (select cateid1 from released_channel where  \
                  rechid = %s ) and z=%s and state=30 ORDER BY sort3 desc' % (column,str(rechid),domid[0]['ec']);
        r = self.do(sql_str)
        self.disconn()
        return r

    def get_focus_num_by_db(self,ak,cc,version='dx'):
        chnl_list = [x['rechid'] for x in self.get_chnl_by_db(ak,cc,version)]
        ret = {}
        for chnl in chnl_list:
            ret[chnl] = len(self.get_focus_list_by_db(chnl,ak))
        return ret

    def change_comment_state_by_db(self,infoid,state):
        self.connect()
        sql_str = 'update source_data set commentSwitch=%s where infoid=(SELECT sourceid from \
    information where infoid=%s)'% (str(state),str(infoid))
        print sql_str
        r = self.do(sql_str)
        self.disconn()
        return r

    def get_hotwords_by_db(self,ak,limit=10):
        self.connect()
        ec = self.do('SELECT domainCode as ec from domain,apps where apps.appid=%s and apps.domid=domain.domid' % (str(ak)))
        z = ec[0]['ec']
        sql_str = 'select * from hotwords where z=%s and state=2 order by sort3 desc limit %d' % (str(z),int(limit))
        print sql_str
        r = self.do(sql_str)
        self.disconn()
        return r

    def search_by_db(self,word,ak,cc):
        self.connect()
        ec = self.do('SELECT domainCode as ec from domain,apps where apps.appid=%s and apps.domid=domain.domid' % (str(ak)))
        print ec
        z = ec[0]['ec']
        sql_str = 'select infoid,title,model from information where z in (%s,%s) and state=30 and title like \'' % (str(z),str(cc))
        sql_str = sql_str + '%'+str(word)+'%\' order by sort3 desc'

        print sql_str
        r = self.do(sql_str)
        self.disconn()
        return r

    def delete_user_by_db(self,value,way='mid'):
        self.connect()
        self.do('delete from member where %s = %s' % (str(way),str(value)))
        self.disconn()


    def get_inv_count_by_db(self,mid,ak='1'):
        self.connect()
        domain_code = self.do('select t1.domainCode from domain t1,apps t2 where t1.domid=t2.domid and '
                              't2.appid=%s' % (str(ak)))
        r = self.do('select invnum from member_inviter where mid = %s and domainCode=%s'
                    % (str(mid),str(domain_code[0]['domainCode'])))
        self.disconn()
        return r[0]['invnum']

    def get_inv_info_by_db(self,mid,ak='1'):
        self.connect()
        domain_code = self.do('select t1.domainCode from domain t1,apps t2 where t1.domid=t2.domid and '
                              't2.appid=%s' % (str(ak)))

        r = self.do('select inviter,rootinviter from member_inviter where mid = %s and domainCode=%s' % (str(mid),str(domain_code[0]['domainCode'])))
        self.disconn()
        return r[0]

    def get_inv_code_by_db(self,mid):
        self.connect()
        r = self.do('select invcode from member where mid = %s' % (str(mid)))
        self.disconn()
        print r
        return r[0]['invcode']

    def get_pic_addr_by_title_for_sjw(self,title):
        self.connect('sjw')
        sql_str = 'select comThumb as pic from information where title =\'%s\' order by createTime desc limit 1' % (str(title))
        print sql_str
        r = self.do(sql_str)
        self.disconn()
        return r[0]['pic']

    def get_last_head_info_by_db(self,mid):
        self.connect()
        sql_str = 'select t1.infoid,t2.mid,t1.comThumb,t2.content from information t1,clue t2 where t1.infoid=t2.infoid and t2.mid=%s ORDER BY t1.sort3 desc limit 1' % (str(mid))
        #print sql_str
        r = self.do(sql_str)
        self.disconn()
        return r[0]

    def change_article_state_by_db(self,infoid,state):
        self.connect()
        sql_str = 'update information set state= %s where infoid= %s' % (str(state),str(infoid))
        #print sql_str
        r = self.do(sql_str)
        self.disconn()
        return True

    def del_article_by_db(self,infoid):
        return self.change_article_state_by_db(infoid,1)

    def publish_del_article_by_db(self,infoid):
        return self.change_article_state_by_db(infoid,30)

    def get_infoid_by_article_name(self,name):
        self.connect()
        sql_str = 'select infoid from information where title = \'%s\'' % (str(name))
        #print sql_str
        r = self.do(sql_str)
        self.disconn()
        if len(r) == 0:
            return False
        return r[0]['infoid']

    def close_comment_by_name(self,name):
        infoid = self.get_infoid_by_article_name(name)
        return self.change_comment_state_by_db(infoid,1)

    def open_comment_by_name(self,name):
        infoid = self.get_infoid_by_article_name(name)
        return self.change_comment_state_by_db(infoid,0)

    def get_comment_count_by_name(self,name):
        try:
            name = name.encode('utf-8')
        except:
            pass
        self.connect()
        sql_str = 'select t2.replyCount from information as t1,source_data as t2 where ' \
                  't1.title=\'%s\' and t1.sourceid = t2.infoid;'% (str(name))
        #print sql_str
        r = self.do(sql_str)
        self.disconn()
        if len(r) == 0:
            return False
        return r[0]['replyCount']

    def change_comment_count_by_name(self,name,count):
        try:
            name = name.encode('utf-8')
        except:
            pass
        self.connect()
        sql_str = 'update information as t1,source_data as t2 set t2.replyCount= %d where ' \
                  't1.title=\'%s\' and t1.sourceid = t2.infoid;'% (int(count),str(name))
        #print sql_str
        r = self.do(sql_str)
        self.disconn()
        return True

    def get_comment_count_by_id(self,inofid):
        self.connect()
        sql_str = 'select t2.replyCount from information as t1,source_data as t2 where ' \
                  't1.infoid=\'%s\' and t1.sourceid = t2.infoid;'% (str(inofid))
        #print sql_str
        r = self.do(sql_str)
        self.disconn()
        if len(r) == 0:
            return False
        return r[0]['replyCount']

    def change_comment_count_by_id(self,infoid,count):
        self.connect()
        sql_str = 'update information as t1,source_data as t2 set t2.replyCount= %d where ' \
                  't1.infoid=\'%s\' and t1.sourceid = t2.infoid;'% (int(count),str(infoid))
        #print sql_str
        r = self.do(sql_str)
        self.disconn()
        return True

    def get_digg_count_by_db(self,comid):
        self.connect()
        sql_str = 'select digg,diggBase from comment where comid=%s'% (str(comid))
        #print sql_str
        r = self.do(sql_str)
        self.disconn()
        if r[0]['diggBase'] == 0:
            return r[0]['digg']
        return r[0]['digg'],r[0]['diggBase']

    def set_digg_count_by_db(self, comid, count, digg_base=0):
        self.connect()
        digg = count - digg_base
        sql_str = 'update comment set digg=%s,diggBase=%s where comid=%s'% (str(digg),str(digg_base),str(comid))
        #print sql_str
        r = self.do(sql_str)
        self.disconn()
        return True

    def get_support_count_by_db(self,infoid):
        self.connect()
        sql_str ='SELECT t2.supportBase,t2.supportCount from information t1,source_data t2 where t1.infoid = %s' \
        ' and t1.sourceid = t2.infoid'% (str(infoid))
        #print sql_str
        r = self.do(sql_str)
        self.disconn()
        if r[0]['supportBase'] == 0:
            return r[0]['supportCount']
        return r[0]['supportCount'],r[0]['supportBase']

    def set_support_count_by_db(self, comid, count, support_base=0):
        self.connect()
        support = int(count) - support_base
        sql_str = 'update information t1,source_data t2 set t2.supportBase = %s,t2.supportCount=%s where t1.infoid = %s' \
        ' and t1.sourceid = t2.infoid'% (str(support_base),str(support),str(comid))
        #print sql_str
        r = self.do(sql_str)
        self.disconn()
        return True

    def get_opposition_count_by_db(self,infoid):
        self.connect()
        sql_str ='SELECT t2.oppositionBase,t2.oppositionCount from information t1,source_data t2 where t1.infoid = %s' \
        ' and t1.sourceid = t2.infoid'% (str(infoid))
        #print sql_str
        r = self.do(sql_str)
        self.disconn()
        if r[0]['oppositionBase'] == 0:
            return r[0]['oppositionCount']
        return r[0]['oppositionCount'],r[0]['oppositionBase']

    def set_opposition_count_by_db(self, comid, count, opposition_base=0):
        self.connect()
        opposition = int(count) - opposition_base
        sql_str = 'update information t1,source_data t2 set t2.oppositionBase = %s,t2.oppositionCount=%s where t1.infoid = %s' \
        ' and t1.sourceid = t2.infoid'% (str(opposition_base),str(opposition),str(comid))
        #print sql_str
        r = self.do(sql_str)
        self.disconn()
        return True

    def get_head_id_by_db(self,subtype,limit=20):
        self.connect()
        sql_str = 'SELECT t1.infoid from information t1,clue t2,source_data t3,member t4 ' \
                  'where t1.infoid=t2.infoid and t1.state=30 and t2.subtype=%s  ' \
                  'and t1.sourceid=t3.infoid and t2.mid=t4.mid ORDER BY t1.createTime desc limit %s'% (str(subtype),str(limit))
        #print sql_str
        r = self.do(sql_str)
        r=[x['infoid'] for x in r]
        self.disconn()
        return r

    def get_head_datail_by_db(self,infoid):
        self.connect()
        sql_str = 'SELECT t3.supportBase,t3.supportCount,t3.replyCount from information t1,clue t2,source_data t3 ' \
                  'where t1.infoid=t2.infoid and t1.sourceid=t3.infoid ' \
                  'and t1.infoid=%s'% (str(infoid))
        #print sql_str
        r = self.do(sql_str)
        self.disconn()
        return r[0]

    def get_activity_info_by_db(self,infoid):
        self.connect()
        sql_str = 'select t1.* from activity t1,information t2  where t1.infoid=t2.infoid ' \
                  'and t2.infoid=%s ORDER BY t2.sort3 desc'% (str(infoid))
        #print sql_str
        r = self.do(sql_str)
        self.disconn()
        return r[0]

    def get_latest_clue(self,subtype):
        self.connect()
        sql_str = 'SELECT t2.* FROM information t1,clue t2 where t1.cateid=\'101\' ' \
                  'and t2.subtype=%s and t1.infoid=t2.infoid ORDER BY t1.createTime desc limit 1' % (str(subtype))
        r = self.do(sql_str)
        self.disconn()
        return r[0]

    def get_yc_clue_type_by_db(self):
        self.connect()
        sql_str = 'select name from cluecate order by clcaid'
        #print sql_str
        r = self.do(sql_str)
        ret = [x.get('name').decode('utf-8') for x in r]
        self.disconn()
        return ret

    def set_article_unpublished_by_db(self,infoid):
        return self.change_article_state_by_db(infoid,10)

    def set_article_faield_by_db(self,infoid):
        return self.change_article_state_by_db(infoid,3)

    def change_paper_state_by_db(self,spuid,state):
        self.connect()
        sql_str = 'update spu set saleOff=%s where spuid=%s' % (str(state),str(spuid))
        #print sql_str
        r = self.do(sql_str)
        self.disconn()
        return True

    def change_all_paper_state_by_db(self,state):
        self.connect()
        sql_str = 'update spu set saleOff=%s' % (str(state))
        #print sql_str
        r = self.do(sql_str)
        self.disconn()
        return True

    def set_all_paper_free(self):
        self.change_all_paper_state_by_db(1)

    def set_all_paper_charge(self):
        self.change_all_paper_state_by_db(0)

    def get_subchnl_by_db(self,dc,ec=420000000010000,cc=420100):
        from mongo import Mongo
        m = Mongo()
        if dc.find('#')!=-1:
            dc = dc.split('#')[0]
        mid = m.get_mid(dc)
        self.connect()
        #sql_str = 'select rechid FROM subscribed where mid=%s and z in (%s,%s)' % (str(mid),str(ec),str(cc))
        sql_str = 'select rechid FROM subscribed where mid=%s ' % (str(mid))
        r = self.do(sql_str)
        self.disconn()
        ret = [x.get('rechid') for x in r]
        return ret

    def get_force_chnl(self,ec=420000000010000,cc=420100):
        self.connect()
        sql_str = 'select rechid from domain_released_channel ' \
                  'where z in (\'420000000010000\',%s,%s) and state=30 and ' \
                  'sortNum in (\'10\',\'20\',\'30\',\'40\') order by ' \
                  'sortNum,sort1 desc,sort3 desc' % (str(ec),str(cc))
        r = self.do(sql_str)
        self.disconn()
        ret = [x.get('rechid') for x in r]
        return ret

    def get_all_chnl(self,ec=420000000010000,cc=420100):
        self.connect()
        sql_str = 'select rechid from domain_released_channel ' \
                  'where z in (\'420000000010000\',%s,%s) and state=30 ' \
                  'order by ' \
                  'sortNum,sort1 desc,sort3 desc' % (str(ec),str(cc))
        r = self.do(sql_str)
        self.disconn()
        ret = [x.get('rechid') for x in r]
        return ret

    def get_sub_able_chnl(self,dc,ec=420000000010000,cc=420100):
        all = self.get_all_chnl(ec,cc)
        my_chnl = self.get_subchnl_by_db(dc,ec,cc)
        force_chnl = self.get_force_chnl(ec,cc)
        subable = set(all)-set(my_chnl)-set(force_chnl)
        return list(subable)

    def set_user_paid_for_newspapar(self,dc,spuid,last=24):
        from mongo import Mongo
        m = Mongo()
        mid = m.get_mid(dc)
        creat_time = datetime.now() - timedelta(hours=1)
        end_time = datetime.now() + timedelta(hours=int(last))
        creat_time = creat_time.strftime('%Y-%m-%d %H:%M:%S')
        end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')
        print creat_time
        self.connect()
        sql_str = 'update timelimit set mid= %s,createTime=\'%s\',endTime=\'%s\',spuid=%s ' \
                  'limit 1' % (str(mid),str(creat_time),str(end_time),str(spuid))
        print sql_str
        r = self.do(sql_str)
        self.disconn()
        return True

    def set_user_charge_for_newspapar(self,dc,spuid,last=-1):
        from mongo import Mongo
        m = Mongo()
        mid = m.get_mid(dc)
        creat_time = datetime.now() - timedelta(days=1)
        end_time = datetime.now() + timedelta(hours=int(last))
        creat_time = creat_time.strftime('%Y-%m-%d %H:%M:%S')
        end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')
        print creat_time
        self.connect()
        sql_str = 'update timelimit set mid= %s,createTime=\'%s\',endTime=\'%s\',spuid=%s ' \
                  'limit 1' % (str(mid),str(creat_time),str(end_time),str(spuid))
        print sql_str
        r = self.do(sql_str)
        self.disconn()
        return True

    def get_user_paper_info(self,dc):
        from mongo import Mongo
        m = Mongo()
        mid = m.get_mid(dc)
        self.connect()
        sql_str = 'select telmid from timelimit where mid=%s order by telmid desc' % (str(mid))
        print sql_str
        r = self.do(sql_str)
        self.disconn()
        return r

    def set_paper_price(self,skuid,price):
        self.connect()
        sql_str = 'update sku set price=%s where skuid=%s' % (str(price),str(skuid))

        r = self.do(sql_str)
        print sql_str
        print r
        self.disconn()
        return True

    def get_secret_by_ak(self,ak):
        self.connect()
        sql_str = 'select clientSecret from apps where appid=%s' % (str(ak))
        r = self.do(sql_str)
        print r
        self.disconn()
        return r[0]['clientSecret']

    def get_suggest_by_db(self,content):
        try:
            content = content.encode('utf-8')
        except:
            pass
        self.connect()
        sql= 'select * from suggest where content = \'%s\'' % (content)
        print sql
        result=self.do(sql)
        self.disconn()
        if result:
            return True
        else:
            return False

if __name__ == '__main__':
    a = DbLib()
    # a.connect()
    # sql = 'select * from article where infoid=793737946078646272'
    # r = a.do(sql)
    # content = r[0]['content']
    # comp = r[0]['component']
    # print r[0]['content']
    # print r[0]['component']
    # a.disconn()
    dc='1,0,0,93JhERG1UYLiW.p6UfdubuLUFveUZCjg6v.QMEkHKu8=#05bd637abafa08464553157aa1428405'
    ec = 420000000010000
    print a.get_inv_info_by_db(813681064261455872)
    #print i
    '''
    r= a.get_chnl_by_db(1,420100,'plug')
    print r
    c = [x['rechid'] for x in r]
    for i in c:
        a_list = a.get_focus_list_by_db(i)
        #print i,len(a_list)
    print a.get_focus_num_by_db(1,420100)
        '''
    #b = a.change_article_state_by_db('781320267174776832',30)
    # b = a.get_last_head_info_by_db(630948137707769856)
    # print b
    # r= a.get_pic_addr_by_title_for_sjw('a')
    # print r
    #for i in r:
        #print i
    #b={'ownerPermiment_state_by_db(762484625116499968,1)ssion': 0L, 'supportCount': 0L, 'topTitle': '', 'nsort': 0L, 'pageViewBase': 474L, 'colid': 0L, 'rechid': 0L, 'oppositionCount': 0L, 'keywords': '', 'jbrowse': 0, 'style': 1, 'subTitle': '', 'oppositionBase': 832L, 'title': '\xe6\x96\x87\xe5\xad\x97\xe7\xa8\xbf\xe4\xbb\xb619', 'otherPermission': 0L, 'rootInfoid': 0L, 'owner': 0L, 'note': '', 'state': 30, 'replyCount': 0L, 'editor': '', 'targetUrl': '', 'insoid': 0L, 'type': 1, 'releaseTime': datetime.datetime(2016, 8, 8, 11, 4, 36), 'model': 2, 'pageView': 0L, 'groupPermission': 0L, 'supportBase': 489L, 'placeCode': 0L, 'sourceid': 762484625116499968L, 'listTitle': '', 'insn': 0L, 'y': 0L, 'flag': 0, 'link': 0, 'stick': 0, 'groups': 0L, 'parentid': 0L, 'listSummary': '', 'createTime': datetime.datetime(2016, 8, 8, 11, 4, 36), 'recommendChannel': 762483404200742912L, 'z': 420000000010000L, 'cateid': 762483404183965696L, 'author': '', 'infoid': 762484625116499968L, 'summary': '', 'comThumb': '[]', 'shareCount': 0L, 'sort1': 'fKtwdAm100', 'x': 2L, 'sort3': '0fKtwdAm100', 'sort2': ''}
