# -*- coding: utf-8 -*-
__author__ = 'liaoben'

from db import DxDb
import os
from datetime import datetime

class DbLib(DxDb):

    def get_latest_danmu_by_db(self):
        self.connect()
        sql_str = 'select dmkid,uricode,timePoint,content,createTime from danmaku order by createTime desc limit 1'
        r = self.do(sql_str)
        self.disconn()
        return r[0]

    def del_latest_danmu_by_db(self,dmkid):
        self.connect()
        #print dmkid
        sql_str = 'delete from danmaku where dmkid = %s '%(str(dmkid))
        r = self.do(sql_str)
        self.disconn()
        return True


    def get_chnl_by_db(self,ak,cc,version='dx'):
        self.connect()
        if cc=='' or isinstance(cc,type(None)):
            cc=420100
        domid = self.do('SELECT domainCode as ec from domain,apps where apps.appid=%s and apps.appid=domain.domid' % (ak))
        sql_str = {
            'dx':'select rechid,name,flag,model from domain_released_channel where z in (%s,%s) and state=30 and not drccid=0 and sortNum in \
                 (\'10\',\'20\',\'30\',\'40\') order by sortNum,sort3 desc' % (domid[0]['ec'],str(cc)),
            'plug':'select rechid,name,flag,model from domain_released_channel where z in (%s,%s) and \
                 state=30 and not drccid=0 and sortNum in (\'10\',\'20\',\'30\',\'40\',\'50\',\'60\') order by \
                   sortNum,sort3 desc''' % (domid[0]['ec'],str(cc))
        }

        #print sql_str[version]
        #print version
        #print sql_str.has_key(version)
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
        domid = self.do('SELECT domainCode as ec from domain,apps where apps.appid=%s and apps.appid=domain.domid' % (ak))
        column = '*'
        sql_str = 'select %s from information where cateid = (select cateid1 from released_channel where  \
                  rechid = %s) and z=%s ORDER BY sort3 desc' % (column,str(rechid),domid[0]['ec']);
        r = self.do(sql_str)
        self.disconn()
        return r

    def get_focus_num_by_db(self,ak,cc,version='dx'):
        chnl_list = [x['rechid'] for x in self.get_chnl_by_db(ak,cc,version)]
        ret = {}
        for chnl in chnl_list:
            ret[chnl] = len(self.get_focus_list_by_db(chnl,ak))
        return ret

    # 0 0 0 0:四位分别为分享 收藏 弹幕 评论
    def change_comment_state_by_db(self,infoid,state):
        self.connect()
        sql_str = 'update source_data set commentSwitch=%s where infoid=(SELECT sourceid from \
    information where infoid=%s)'% (str(state),str(infoid))
        #print sql_str
        r = self.do(sql_str)
        self.disconn()
        return r

    def get_hotwords_by_db(self,ak,limit=10):
        self.connect()
        ec = self.do('SELECT domainCode as ec from domain,apps where apps.appid=%s and apps.appid=domain.domid' % (str(ak)))
        z = ec[0]['ec']
        sql_str = 'select * from hotwords where z=%s and state=2 order by sort3 desc limit %d' % (str(z),int(limit))
        print sql_str
        r = self.do(sql_str)
        self.disconn()
        return r

    def search_by_db(self,word,ak,cc):
        self.connect()
        ec = self.do('SELECT domainCode as ec from domain,apps where apps.appid=%s and apps.appid=domain.domid' % (str(ak)))
        #print ec
        z = ec[0]['ec']
        sql_str = 'select infoid,title,model from information where z in (%s,%s) and state=30 and title like \'' % (str(z),str(cc))
        sql_str = sql_str + '%'+str(word)+'%\' order by sort3 desc'

        #print sql_str
        r = self.do(sql_str)
        self.disconn()
        return r

    def delete_user_by_db(self,mid):
        self.connect()
        self.do('delete from member where mid = %s' % (str(mid)))
        self.disconn()

    def get_inv_count_by_db(self,mid):
        self.connect()
        r = self.do('select invnum from member where mid = %s' % (str(mid)))
        self.disconn()
        return r[0]['invnum']

    def get_inv_code_by_db(self,mid):
        self.connect()
        r = self.do('select invcode from member where mid = %s' % (str(mid)))
        self.disconn()
        return r[0]['invcode']

    def get_pic_addr_by_title_for_sjw(self,title):
        self.connect('sjw')
        sql_str = 'select comThumb as pic from information where title =\'%s\' order by createTime desc limit 1' % (str(title))
        #print sql_str
        r = self.do(sql_str)
        self.disconn()
        return r[0]['pic']

    def get_infoid_by_article_name(self,name):
        try:
            name = name.encode('utf-8')
        except:
            pass
        self.connect()
        sql_str = 'select infoid from information where title = \'%s\'' % (str(name))
        #print sql_str
        r = self.do(sql_str)
        self.disconn()
        if len(r) == 0:
            return False
        return r[0]['infoid']

    def get_clueid_with_content_by_db(self,content):
        # self.connect()
        # sql_str = 'select infoid from clue where content=\'%s\'' % (str(content))
        # r = self.do(sql_str)
        # self.disconn()
        # if len(r) == 0:
        #     return False
        # return r[0]['infoid']
        result = self.get_clue_with_content_by_db(content)
        return result['infoid']

    def get_clue_with_content_by_db(self,content):
        self.connect()
        sql_str = 'select * from clue where content=\'%s\'' % (str(content))
        r = self.do(sql_str)
        self.disconn()
        if len(r) == 0:
            return False
        return r[0]

    def review_clue_by_content(self,content,state=30):
        infoid = self.get_clueid_with_content_by_db(content)
        self.change_article_state_by_db(infoid,state)
        return True

    def refused_clue_by_content(self,content,reason,state = 3):
        infoid = self.get_clueid_with_content_by_db(content)
        self.connect()
        sql_str_set_remark = 'update clue SET remark = \'%s\' where content = \'%s\'' % (str(reason),str(content))
        sql_str_change_state = 'update information set state= %s where infoid = %s' % (str(state),str(infoid))
        self.do(sql_str_set_remark)
        self.do(sql_str_change_state)
        self.disconn()
        return True



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

    def clear_comment_by_name(self,name):
        try:
            name = name.encode('utf-8')
        except:
            pass
        self.connect()
        sql_str = 'delete comment from comment,information where information.title=\'%s\' and information.infoid = comment.infoid'% (name)
        r = self.do(sql_str)
        self.disconn()
        return True

    def change_comment_time_by_id(self,comid,create_time):
        self.connect()
        sql_str = 'UPDATE comment set createTime =\'%s\' where comid = %s'% (create_time,comid)
        r = self.do(sql_str)
        self.disconn()
        return True

    def get_comment_time_by_id(self,comid):
        self.connect()
        sql_str = 'select createTime from comment where comid=%s'% (str(comid))
        r = self.do(sql_str)
        self.disconn()
        print r
        return r[0]['createTime']

    def get_play_count_by_name(self,name):
        try:
            name = name.encode('utf-8')
        except:
            pass
        self.connect()
        sql_str = 'select t2.playCountBase,t2.playCount from information as t1,source_data as t2 where ' \
                  't1.title=\'%s\' and t1.sourceid = t2.infoid;'% (str(name))
        #print sql_str
        r = self.do(sql_str)
        self.disconn()
        if len(r) == 0:
            return False
        if r[0]['playCountBase'] == 0:
            return r[0]['playCount']
        return r[0]['playCount'],r[0]['playCountBase']

    def change_play_count_by_name(self,name,count,base =0):
        try:
            name = name.encode('utf-8')
        except:
            pass
        self.connect()
        count = count - base
        sql_str = 'update information as t1,source_data as t2 set t2.playCountBase= %d,t2.playCount= %d where ' \
                  't1.title=\'%s\' and t1.sourceid = t2.infoid;'% (int(base),int(count),str(name))
        #print sql_str
        r = self.do(sql_str)
        self.disconn()
        return True

    def get_push_info_by_name(self,name):
        try:
            name = name.encode('utf-8')
        except:
            pass
        self.connect()
        sql_str = 'select t1.infoid,t2.model from information t1,source_data t2 ' \
                  'where t1.sourceid = t2.infoid and t1.title = \'%s\'' % (str(name))
        r = self.do(sql_str)
        self.disconn()
        return r[0]

    def get_mid_by_phone(self,phone):
        self.connect()
        sql_str = 'SELECT mid from member where phone=%s' % (str(phone))
        r = self.do(sql_str)
        self.disconn()
        return r[0]['mid']

    def get_domaincode_by_name(self,name):
        try:
            name = name.encode('utf-8')
        except:
            pass
        self.connect()
        sql_str = 'select domainCode from domain where name= \'%s\'' % (str(name))
        r = self.do(sql_str)
        self.disconn()
        return r[0]['domainCode']

    #1：删除；2:正在审核中；3:审核未通过；10：新稿；20：已审；30：已发
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

    def set_article_unpublished_by_db(self,infoid):
        return self.change_article_state_by_db(infoid,10)

    def set_article_faield_by_db(self,infoid):
        return self.change_article_state_by_db(infoid,3)

    def get_first_clue(self,subtype):
        self.connect()
        sql_str = 'select t1.infoid from information t1,clue t2 where t1.state=30 ' \
                  'and t2.subtype = %s and t1.infoid=t2.infoid order by sort3 desc limit 1' % (str(subtype))
        #print sql_str
        r = self.do(sql_str)
        self.disconn()
        return r[0]['infoid']

    def set_article_time_by_db(self,release_time,condition):
        self.connect()
        try:
            condition = condition.encode('utf-8')
        except:
            pass
        sql_str = 'update information set releaseTime = \'%s\' where %s' % (str(release_time),str(condition))
        #print sql_str
        r = self.do(sql_str)
        self.disconn()
        return True

if __name__ == '__main__':
    a = DbLib()
    b = 'baoliao shenhebutongguo test 122'
    print a.refused_clue_by_content(b,'测试测试',3)
    # count =9999
    # print count
    # print a.get_clueid_with_content_by_db(b)
    print a.get_clue_with_content_by_db(b)['remark'].decode('utf-8')
    # print a.get_digg_count_by_db(b)
    # a.set_digg_count_by_db(b,count)
    # print a.get_digg_count_by_db(b)
    # '''
    # r= a.get_chnl_by_db(1,420100,'plug')
    # print r
    # c = [x['rechid'] for x in r]
    # for i in c:
    #     a_list = a.get_focus_list_by_db(i)
    #     #print i,len(a_list)
    # print a.get_focus_num_by_db(1,420100)
    #     '''
    # r= a.get_pic_addr_by_title_for_sjw('2')
    # img_path ='/wwwdata/sjw/resource/img/'
    # r=eval(r)
    # fpath = [x['u'].replace('${infoImgPath}',img_path).replace('_m','') for x in r]
    # print fpath
    # from scp_handler import SCPHandler
    # from Common import get_image_info
    #
    # s = SCPHandler()
    # for f in fpath:
    #     t = os.path.split(f)[1]
    #     pic = s.get_pic(f,t)
    #     print pic
    #     print get_image_info(pic)
    # def get_picinfo_by_title(title):
    #     db = DbLib()
    #     ret = []
    #     r= a.get_pic_addr_by_title_for_sjw(title)
    #     img_path ='/wwwdata/sjw/resource/img/'
    #     r=eval(r)
    #     fpath = [x['u'].replace('${infoImgPath}',img_path).replace('_m','') for x in r]
    #     from scp_handler import SCPHandler
    #     from Common import get_image_info
    #     s = SCPHandler()
    #     for f in fpath:
    #         t = os.path.split(f)[1]
    #         pic = s.get_pic(f,t)
    #         info  = get_image_info(pic)
    #         print pic
    #         print get_image_info(pic)
    #         ret.append(info)
    #     return info
    #print fpath
    #for i in r:
        #print i
    #b={'ownerPermiment_state_by_db(762484625116499968,1)ssion': 0L, 'supportCount': 0L, 'topTitle': '', 'nsort': 0L, 'pageViewBase': 474L, 'colid': 0L, 'rechid': 0L, 'oppositionCount': 0L, 'keywords': '', 'jbrowse': 0, 'style': 1, 'subTitle': '', 'oppositionBase': 832L, 'title': '\xe6\x96\x87\xe5\xad\x97\xe7\xa8\xbf\xe4\xbb\xb619', 'otherPermission': 0L, 'rootInfoid': 0L, 'owner': 0L, 'note': '', 'state': 30, 'replyCount': 0L, 'editor': '', 'targetUrl': '', 'insoid': 0L, 'type': 1, 'releaseTime': datetime.datetime(2016, 8, 8, 11, 4, 36), 'model': 2, 'pageView': 0L, 'groupPermission': 0L, 'supportBase': 489L, 'placeCode': 0L, 'sourceid': 762484625116499968L, 'listTitle': '', 'insn': 0L, 'y': 0L, 'flag': 0, 'link': 0, 'stick': 0, 'groups': 0L, 'parentid': 0L, 'listSummary': '', 'createTime': datetime.datetime(2016, 8, 8, 11, 4, 36), 'recommendChannel': 762483404200742912L, 'z': 420000000010000L, 'cateid': 762483404183965696L, 'author': '', 'infoid': 762484625116499968L, 'summary': '', 'comThumb': '[]', 'shareCount': 0L, 'sort1': 'fKtwdAm100', 'x': 2L, 'sort3': '0fKtwdAm100', 'sort2': ''}
