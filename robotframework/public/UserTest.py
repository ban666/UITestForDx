# -*- coding: utf-8 -*-
__author__ = 'liaoben'

from Login import UserRequest
from time import sleep
from conf import QQ_LOGIN_INFO,WECHAT_LOGIN_INFO,WEIBO_LOGIN_INFO
from operator import *
from DbLib import DbLib
from common import download_image,same_as

mode= 'mcp/dx'
def regist_and_login(phone,clear=False,wait_time=3,*args):
    api = UserRequest(mode)
    dc_old = api.vcode(phone)
    api.dc=dc_old
    dc = dc_old.split('#')[0]
    sleep(int(wait_time))
    vcode = api.get_vcode_by_redis(phone,dc)
    print 'get vcode:',vcode
    userinfo = api.login(phone,vcode,*args)
    print userinfo
    if clear==True or clear == 'True':
        clear_result = user_clear(userinfo)
        assert clear_result
    return userinfo

def regist_and_login_with_args(phone,ak,clear=False,wait_time=3,*args):
    db = DbLib()
    secret = db.get_secret_by_ak(ak)
    api = UserRequest(mode,secret=secret)
    dc_old = api.vcode(phone,'hd_ak='+str(ak))
    api.dc=dc_old
    dc = dc_old.split('#')[0]
    sleep(int(wait_time))
    vcode = api.get_vcode_by_redis(phone,dc)
    print 'get vcode:',vcode
    userinfo = api.login(phone,vcode,'hd_ak='+str(ak),*args)
    print userinfo
    if clear==True or clear == 'True':
        clear_result = user_clear(userinfo)
        assert clear_result
    return userinfo



def regist_and_login_2(phone,sid,appid='900001',clear=False,wait_time=3):
    api = UserRequest(mode)
    dc_old = api.vcode(phone)
    api.dc=dc_old
    dc = dc_old.split('#')[0]
    sleep(wait_time)
    vcode = api.get_vcode_by_redis(phone,dc)
    print 'get vcode:',vcode
    if sid!='' and appid!='':
        d = ['sid='+str(sid),'appid='+str(appid)]
        userinfo = api.login(phone,vcode,*d)

        print 'login:result:',userinfo
    else:
        userinfo = api.login(phone,vcode)
    if clear:
        clear_result = user_clear(userinfo)
        assert clear_result
    return userinfo

def user_clear(userinfo,wait=10):
    try:
        UserRequest(mode).del_user(userinfo['data']['userinfo']['uid'])
        sleep(wait)
        return True
    except Exception as e:
        return False

def login_test(phone,vcode):
    api = UserRequest(mode)
    userinfo = api.login(phone,vcode)
    print userinfo
    return userinfo

def invite_test(user_a,user_b):
    api = UserRequest(mode)
    return api.invite_plus(user_a,user_b)

def third_login_test(third_way,clear=False,*args):
    api = UserRequest(mode)
    custom = {}
    if int(third_way) == 4:
        custom = {
            'platform':args[0],
            'uid':args[1],
            'screen_name':args[2],
            'profile_image_url':args[3]
        }
    third_way_dict = {
        '1':WEIBO_LOGIN_INFO,
        '2':QQ_LOGIN_INFO,
        '3':WECHAT_LOGIN_INFO,
        '4':custom
    }
    third_info = third_way_dict[third_way]
    platform = third_info['platform']
    uid = third_info['uid']
    screen_name = third_info['screen_name']
    profile_image_url = third_info['profile_image_url']
    userinfo = api.openid_login(platform,uid,screen_name,profile_image_url)
    if clear:
        clear_result = user_clear(userinfo)
        assert clear_result
    return userinfo

def third_login_test_with_args(third_way,ak,clear=False,*args):
    db = DbLib()
    secret = db.get_secret_by_ak(ak)
    api = UserRequest(mode,secret=secret)
    custom = {}
    third_way_dict = {
        '1':WEIBO_LOGIN_INFO,
        '2':QQ_LOGIN_INFO,
        '3':WECHAT_LOGIN_INFO,
        '4':custom
    }
    third_info = third_way_dict[str(third_way)]
    platform = third_info['platform']
    uid = third_info['uid']
    screen_name = third_info['screen_name']
    profile_image_url = third_info['profile_image_url']
    userinfo = api.openid_login(platform,uid,screen_name,profile_image_url,*args)
    if clear==True or clear == 'True':
        clear_result = user_clear(userinfo)
        assert clear_result
    return userinfo

def get_dc_mid_from_userinfo(content):
    return content['data']['userinfo']['uid'],content['dc']

def get_inv_code(dc,*args):
    api = UserRequest(mode)
    ret = api.myinvite(dc,*args)
    return ret


def get_inv_count(mid):
    d = DbLib()
    invcount = d.get_inv_count_by_db(mid)
    return invcount

def judge_length(content,length,method):
    m_dict = {
        '>':gt,
        '<':lt,
        '=':eq,
        '>=':ge,
        '<=':le
    }
    if not method in m_dict.keys():
        print 'method is error'
        return False
    return m_dict[method](int(content),int(length))

def bind_third_test(dc,third_way,clear=False,*args):
    api = UserRequest(mode)
    custom = {}
    if int(third_way) == 4:
        custom = {
            'platform':args[0],
            'uid':args[1],
            'screen_name':args[2],
            'profile_image_url':args[3]
        }
    third_way_dict = {
        '1':WEIBO_LOGIN_INFO,
        '2':QQ_LOGIN_INFO,
        '3':WECHAT_LOGIN_INFO,
        '4':custom
    }
    third_info = third_way_dict[third_way]
    platform = third_info['platform']
    uid = third_info['uid']
    screen_name = third_info['screen_name']
    profile_image_url = third_info['profile_image_url']
    userinfo = api.set_openuid(dc,platform,uid,screen_name,profile_image_url)
    if clear:
        user_clear(userinfo)
    return userinfo

def bind_phone_test(dc,phone,wait_time=10,*args):
    api = UserRequest(mode)
    api.vcode(phone,'hd_dc='+str(dc))
    print dc
    sleep(wait_time)
    vcode = api.get_vcode_by_redis(phone,dc)
    print 'get vcode:',vcode
    result = api.set_phone(dc,phone,vcode)
    return result

def get_userinfo(dc):
    api = UserRequest(mode)
    userinfo = api.get_center(dc)
    return userinfo

def get_points_by_dc(dc,id='',cmd='nearer',psize='20',*args):
    api = UserRequest(mode)
    ret = api.get_point_list(dc,id,cmd,psize,*args)
    return ret

def get_icon_and_download(userinfo,local_path):
        pass


def invite_user(info_a,info_b):
    api = UserRequest(mode)
    db = DbLib()
    dc_a = info_a['dc']
    mid_a = info_a['data']['userinfo']['uid']
    code_a = db.get_inv_code_by_db(mid_a)
    dc_b = info_b['dc']
    mid_b = info_b['data']['userinfo']['uid']
    code_b = db.get_inv_code_by_db(mid_b)
    print mid_a,mid_b
    #A邀请B
    return api.invite(dc_b,code_a)

def invite(dc,code):
    api = UserRequest(mode)
    return api.invite(dc,code)


def get_invite_info(mid):
    db = DbLib()
    ret = db.get_inv_info_by_db(mid)
    return ret.get('inviter'),ret.get('rootinviter')


def modify_screenname(dc,name):
    try:
        name = name.encode('utf-8')
    except:
        pass
    api = UserRequest(mode)
    ret = api.set_scrname(dc,name)
    return ret

def inv_count_test():
        db = DbLib()
        base = '1361234567'
        p_list = []
        mid_list = []
        user_list = []
        dc_list = []
        invcode_list = []
        invcount_dict = {

        }
        step = 1
        num = 5
        for i in range(num):
            p_list.append(base+str(i))
        try:
            for p in p_list:
                db.delete_user_by_db(p,'phone')
        except:
            pass
        for j in range(num):
            user_list.append(regist_and_login(p_list[j]))

        for k in user_list:
            t_mid,t_dc = get_dc_mid_from_userinfo(k)
            mid_list.append(t_mid)
            dc_list.append(t_dc)
            invcode_list.append(db.get_inv_code_by_db(t_mid))

        #print mid_list,invcode_list
        for l in range(num):
            t_str = '%s   mid: %s invcode: %s' % (str(l),str(mid_list[l]),str(invcode_list[l]))
            print t_str

        api =  UserRequest(mode)
        #A邀请B
        api.invite(dc_list[1],invcode_list[0])
        #B邀请C
        api.invite(dc_list[2],invcode_list[1])

        print 'check 1：', 'A:',get_inv_count(mid_list[0]),'B:',get_inv_count(mid_list[1]),'C:',get_inv_count(mid_list[2])
        assert get_inv_count(mid_list[0]) == 2 and get_inv_count(mid_list[1]) == 1 and get_inv_count(mid_list[2]) == 0
        print u'step %s:用户A邀请了用户B，用户B邀请了用户C。A:2 B:1 C:0 result:OK!' % (str(step))
        step+=1
        #C邀请A
        api.invite(dc_list[0],invcode_list[2])
        print 'check 2：', 'A:', get_inv_count(mid_list[0]),'B:',get_inv_count(mid_list[1]),'C:',get_inv_count(mid_list[2])
        assert get_inv_count(mid_list[0]) == 2 and get_inv_count(mid_list[1]) == 1 and get_inv_count(mid_list[2]) == 1
        print mid_list[0]
        inviter_A,rootinviter_A = get_invite_info(mid_list[0])
        assert inviter_A == mid_list[2] and rootinviter_A == mid_list[0]
        print u'step %s: 用户A填写了C的邀请码，A（父节点/根节点）：（C/A）。A:2 B:1 C:1 result:OK!' % (str(step))
        step+=1
        #A邀请D
        api.invite(dc_list[3],invcode_list[0])
        print 'check 3：', 'A:',get_inv_count(mid_list[0]),'B:', get_inv_count(mid_list[1]),'C:', get_inv_count(mid_list[2]),'D:', get_inv_count(mid_list[3]),'E:', get_inv_count(mid_list[4])
        assert get_inv_count(mid_list[0]) == 3 and get_inv_count(mid_list[1]) == 1 and get_inv_count(mid_list[2]) == 1 and get_inv_count(mid_list[3]) == 0 and get_inv_count(mid_list[4]) == 0
        print u'step %s:用户A邀请D A:3 B:1 C:1 D:0 E:0 result:OK!' % (str(step))
        step+=1

        #C邀请E
        api.invite(dc_list[4],invcode_list[2])
        print 'check 4：', 'A:', get_inv_count(mid_list[0]),'B:', get_inv_count(mid_list[1]),'C:', get_inv_count(mid_list[2]),'D:', get_inv_count(mid_list[3]),'E:', get_inv_count(mid_list[4])
        assert get_inv_count(mid_list[0]) == 4 and get_inv_count(mid_list[1]) == 1 and get_inv_count(mid_list[2]) == 2 and get_inv_count(mid_list[3]) == 0 and get_inv_count(mid_list[4]) == 0

        inviter_D,rootinviter_D = get_invite_info(mid_list[3])
        inviter_E,rootinviter_E = get_invite_info(mid_list[4])
        assert inviter_D == mid_list[0] and rootinviter_D == mid_list[0]
        assert inviter_E == mid_list[2] and rootinviter_E == mid_list[0]
        print u'step %s:用户C邀请E D:(A/A),E:(C/A) A:4 B:1 C:2 D:0 E:0 result:OK!' % (str(step))
        step+=1


        try:
            for p in p_list:
                db.delete_user_by_db(p,'phone')
        except:
            pass

if __name__ == '__main__':




    third_login_test_with_args(1,1)
    # api = UserRequest(mode)
    # phone='13211111111'
    # data1 = ['sid=1','kind=1']
    # b = regist_and_login_2(phone,'123456','900001',clear=True)
    # print b
    # userinfo = regist_and_login(phone)
    # dc = userinfo['dc']
    # modify_name = modify_screenname(dc,'中文')
    # print modify_name
    # user_new = get_userinfo(dc)
    # print user_new['data']['userinfo']['scrname']
    # regist_and_login(phone,True)
    #
    #     api =  UserRequest(mode)
    #     #A邀请B
    #     api.invite(dc_list[1],mid_list[1],invcode_list[0])
    #     #B邀请C
    #     api.invite(dc_list[2],mid_list[2],invcode_list[1])
    #
    #     print 'check 1：', get_inv_count(mid_list[0]),get_inv_count(mid_list[1]),get_inv_count(mid_list[2])
    #
    #     #C邀请A
    #     api.invite(dc_list[0],mid_list[0],invcode_list[2])
    #     print 'check 2：', get_inv_count(mid_list[0]),get_inv_count(mid_list[1]),get_inv_count(mid_list[2])
    #
    #     #A邀请D
    #     api.invite(dc_list[3],mid_list[3],invcode_list[0])
    #     print 'check 3：', get_inv_count(mid_list[0]),get_inv_count(mid_list[1]),get_inv_count(mid_list[2]),get_inv_count(mid_list[3]),get_inv_count(mid_list[4])
    #     #C邀请E
    #     api.invite(dc_list[4],mid_list[4],invcode_list[2])
    #     print 'check 4：', get_inv_count(mid_list[0]),get_inv_count(mid_list[1]),get_inv_count(mid_list[2]),get_inv_count(mid_list[3]),get_inv_count(mid_list[4])
    #
    # #userinfo = third_login_test('1')
    # phone=13477777777
    # #ret = bind_phone_test(userinfo['dc'],phone)
    # #print ret
    # #inv_count_test()
    # # db = DbLib()
    # # db.connect()
    # # sql_str = 'delete from member where phone like %s' % ('1361234567\%')
    # # db.do(sql_str)
    # # db.disconn()
    # userinfo = regist_and_login(phone)
    # url1 = userinfo['data']['userinfo']['icon']
    # local1 = 'g:/test1.jpg'
    # print userinfo['data']['userinfo']['icon']
    # download_image(url1,local1)
    # userinfo2 = third_login_test('1')
    # url2 = userinfo2['data']['userinfo']['icon']
    # local2 = 'g:/test2.jpg'
    # download_image(url2,local2)
    # userinfo = regist_and_login(phone,True)
    # userinfo = third_login_test('1',True)
    # print same_as(local1,local2,0)