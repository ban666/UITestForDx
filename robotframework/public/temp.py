# -*- coding: utf-8 -*-
__author__ = 'liaoben'

from UserTest import regist_and_login_2
from ChnlRequest import ChnlRequest
import requests
import json
def send_comment_by_proxy(coment,iid,comid='',proxy = ''):
    mode = 'mcp/dx'
    api = ChnlRequest(mode)
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


if __name__ == '__main__':
    # api = ChnlRequest('mcp/dx')
    # '''
    # chnl_list = api.chnl()['list'][0]
    # a,b,c = api.get_first_video_and_add_bullet('啦啦啦',chnl_list['id'])
    # print a,b,c
    # print api.get_bullet(a)
    # print api.check_bullet_from_db_and_delete(a,b,c)
    #     '''
    # r = api.get_first_chnl_article_for_comment()
    # print r
    # f_count = 0
    # proxies = {
    #     'http': 'http://47.89.53.92:3128',
    #     'https': 'http://127.0.0.1:8087',
    # }
    # d=[{'http': 'http://112.243.184.242:8888', 'https': 'http://112.243.184.242:8888'}, {'http': 'http://182.90.252.10:2226', 'https': 'http://182.90.252.10:2226'}, {'http': 'http://61.55.135.192:82', 'https': 'http://61.55.135.192:82'}, {'http': 'http://120.25.105.45:81', 'https': 'http://120.25.105.45:81'}, {'http': 'http://221.226.82.130:8998', 'https': 'http://221.226.82.130:8998'}, {'http': 'http://119.6.136.122:80', 'https': 'http://119.6.136.122:80'}, {'http': 'http://139.196.108.68:80', 'https': 'http://139.196.108.68:80'}, {'http': 'http://60.194.100.51:80', 'https': 'http://60.194.100.51:80'}, {'http': 'http://123.56.74.13:8080', 'https': 'http://123.56.74.13:8080'}, {'http': 'http://202.171.253.72:80', 'https': 'http://202.171.253.72:80'}, {'http': 'http://119.254.84.90:80', 'https': 'http://119.254.84.90:80'}, {'http': 'http://122.96.59.104:80', 'https': 'http://122.96.59.104:80'}, {'http': 'http://122.228.179.178:80', 'https': 'http://122.228.179.178:80'}, {'http': 'http://202.108.2.42:80', 'https': 'http://202.108.2.42:80'}, {'http': 'http://121.40.108.76:80', 'https': 'http://121.40.108.76:80'}, {'http': 'http://120.76.243.40:80', 'https': 'http://120.76.243.40:80'}, {'http': 'http://112.81.100.102:8888', 'https': 'http://112.81.100.102:8888'}, {'http': 'http://122.0.74.166:3389', 'https': 'http://122.0.74.166:3389'}, {'http': 'http://122.96.59.106:80', 'https': 'http://122.96.59.106:80'}, {'http': 'http://218.56.132.158:8080', 'https': 'http://218.56.132.158:8080'}, {'http': 'http://218.90.174.167:3128', 'https': 'http://218.90.174.167:3128'}, {'http': 'http://101.254.188.198:8080', 'https': 'http://101.254.188.198:8080'}, {'http': 'http://14.29.124.53:80', 'https': 'http://14.29.124.53:80'}, {'http': 'http://218.56.132.156:8080', 'https': 'http://218.56.132.156:8080'}, {'http': 'http://218.76.106.78:3128', 'https': 'http://218.76.106.78:3128'}, {'http': 'http://218.56.132.155:8080', 'https': 'http://218.56.132.155:8080'}, {'http': 'http://60.206.148.135:3128', 'https': 'http://60.206.148.135:3128'}, {'http': 'http://113.105.185.10:3128', 'https': 'http://113.105.185.10:3128'}, {'http': 'http://120.132.71.212:80', 'https': 'http://120.132.71.212:80'}, {'http': 'http://202.107.238.51:3128', 'https': 'http://202.107.238.51:3128'}, {'http': 'http://112.112.70.116:80', 'https': 'http://112.112.70.116:80'}, {'http': 'http://112.112.70.118:80', 'https': 'http://112.112.70.118:80'}, {'http': 'http://124.133.230.254:80', 'https': 'http://124.133.230.254:80'}, {'http': 'http://123.125.122.203:80', 'https': 'http://123.125.122.203:80'}, {'http': 'http://123.125.122.205:80', 'https': 'http://123.125.122.205:80'}, {'http': 'http://123.125.122.224:80', 'https': 'http://123.125.122.224:80'}, {'http': 'http://123.125.122.204:80', 'https': 'http://123.125.122.204:80'}, {'http': 'http://113.107.112.210:8101', 'https': 'http://113.107.112.210:8101'}, {'http': 'http://61.132.241.103:808', 'https': 'http://61.132.241.103:808'}, {'http': 'http://47.89.53.92:3128', 'https': 'http://47.89.53.92:3128'}, {'http': 'http://47.88.195.233:3128', 'https': 'http://47.88.195.233:3128'}, {'http': 'http://14.101.41.162:8080', 'https': 'http://14.101.41.162:8080'}, {'http': 'http://103.240.241.182:80', 'https': 'http://103.240.241.182:80'}, {'http': 'http://203.130.228.60:8080', 'https': 'http://203.130.228.60:8080'}, {'http': 'http://128.199.178.73:8080', 'https': 'http://128.199.178.73:8080'}, {'http': 'http://52.69.243.39:8080', 'https': 'http://52.69.243.39:8080'}, {'http': 'http://54.169.138.64:80', 'https': 'http://54.169.138.64:80'}, {'http': 'http://54.72.253.207:80', 'https': 'http://54.72.253.207:80'}, {'http': 'http://88.159.43.160:80', 'https': 'http://88.159.43.160:80'}, {'http': 'http://94.207.230.226:80', 'https': 'http://94.207.230.226:80'}, {'http': 'http://83.128.29.187:80', 'https': 'http://83.128.29.187:80'}, {'http': 'http://176.31.96.198:3128', 'https': 'http://176.31.96.198:3128'}, {'http': 'http://62.45.248.11:80', 'https': 'http://62.45.248.11:80'}, {'http': 'http://113.185.19.192:80', 'https': 'http://113.185.19.192:80'}, {'http': 'http://31.220.15.234:80', 'https': 'http://31.220.15.234:80'}, {'http': 'http://61.78.133.143:8080', 'https': 'http://61.78.133.143:8080'}, {'http': 'http://186.229.29.170:80', 'https': 'http://186.229.29.170:80'}, {'http': 'http://192.249.72.148:3128', 'https': 'http://192.249.72.148:3128'}, {'http': 'http://178.32.153.219:80', 'https': 'http://178.32.153.219:80'}, {'http': 'http://213.165.155.189:80', 'https': 'http://213.165.155.189:80'}, {'http': 'http://207.182.139.74:80', 'https': 'http://207.182.139.74:80'}, {'http': 'http://168.187.10.213:8080', 'https': 'http://168.187.10.213:8080'}, {'http': 'http://70.88.182.181:80', 'https': 'http://70.88.182.181:80'}, {'http': 'http://180.250.165.156:80', 'https': 'http://180.250.165.156:80'}, {'http': 'http://182.253.201.78:10000', 'https': 'http://182.253.201.78:10000'}, {'http': 'http://168.102.134.47:8080', 'https': 'http://168.102.134.47:8080'}, {'http': 'http://107.170.213.149:3128', 'https': 'http://107.170.213.149:3128'}, {'http': 'http://219.255.197.90:3128', 'https': 'http://219.255.197.90:3128'}, {'http': 'http://200.29.191.149:3128', 'https': 'http://200.29.191.149:3128'}, {'http': 'http://123.30.238.16:3128', 'https': 'http://123.30.238.16:3128'}, {'http': 'http://94.20.21.38:3128', 'https': 'http://94.20.21.38:3128'}, {'http': 'http://211.110.127.210:3128', 'https': 'http://211.110.127.210:3128'}, {'http': 'http://5.9.117.40:3128', 'https': 'http://5.9.117.40:3128'}, {'http': 'http://164.132.3.14:808', 'https': 'http://164.132.3.14:808'}, {'http': 'http://122.155.3.143:3128', 'https': 'http://122.155.3.143:3128'}, {'http': 'http://182.253.201.76:10000', 'https': 'http://182.253.201.76:10000'}, {'http': 'http://113.161.68.146:8080', 'https': 'http://113.161.68.146:8080'}, {'http': 'http://190.60.245.146:80', 'https': 'http://190.60.245.146:80'}, {'http': 'http://43.243.112.79:3128', 'https': 'http://43.243.112.79:3128'}, {'http': 'http://110.73.33.207:6673', 'https': 'http://110.73.33.207:6673'}, {'http': 'http://122.89.138.20:6675', 'https': 'http://122.89.138.20:6675'}, {'http': 'http://110.72.20.245:6673', 'https': 'http://110.72.20.245:6673'}, {'http': 'http://42.96.187.107:3128', 'https': 'http://42.96.187.107:3128'}, {'http': 'http://61.138.104.30:1080', 'https': 'http://61.138.104.30:1080'}, {'http': 'http://217.37.19.115:9050', 'https': 'http://217.37.19.115:9050'}, {'http': 'http://110.73.30.246:6666', 'https': 'http://110.73.30.246:6666'}, {'http': 'http://121.31.199.91:6675', 'https': 'http://121.31.199.91:6675'}, {'http': 'http://182.90.15.172:6675', 'https': 'http://182.90.15.172:6675'}, {'http': 'http://202.38.95.66:1080', 'https': 'http://202.38.95.66:1080'}, {'http': 'http://113.93.120.136:6675', 'https': 'http://113.93.120.136:6675'}, {'http': 'http://101.68.64.83:1080', 'https': 'http://101.68.64.83:1080'}, {'http': 'http://115.159.96.136:1080', 'https': 'http://115.159.96.136:1080'}, {'http': 'http://116.192.22.192:1080', 'https': 'http://116.192.22.192:1080'}, {'http': 'http://108.61.189.87:5689', 'https': 'http://108.61.189.87:5689'}, {'http': 'http://80.78.38.146:1080', 'https': 'http://80.78.38.146:1080'}, {'http': 'http://46.180.66.239:1080', 'https': 'http://46.180.66.239:1080'}, {'http': 'http://91.185.215.141:5818', 'https': 'http://91.185.215.141:5818'}]
    # for i in range(len(d)):
    #     print 'run time:'+str(i)
    #     ret = send_comment_by_proxy('abc',r,proxy=d[i])
    #     print ret
    #     if ret == False:
    #         f_count+=1
    #         print 'fail count:'+str(f_count)
    # import re
    # def multiple_replace(text, adict):
    #      rx = re.compile('|'.join(map(re.escape, adict)))
    #      def one_xlat(match):
    #            return adict[match.group(0)]
    #      return rx.sub(one_xlat, text)
    # text = 'aaaaaaaabaaaaacccc'
    # adict = {
    #     'ab':'1111',
    #     'ac':'2222'
    # }
    # print multiple_replace(text,adict)
    # mode = 'mcp/plug/app'
    # api = ChnlRequest(mode)
    # infoid = '794341899459891200'
    # content = 'a'
    # for i in range(50):
    #     api.send_comment(infoid,content)
    url = 'http://www.uphubei.com/mobile/index.php?act=connect&op=get_dxxw_info'
    payload ={
        'mid':801613291582656512,
        'sessionid':1111111,
        'token':'182083544444b4adf6cfff040552cc9e'
    }
    url = 'http://10.99.101.4/testlink/lib/api/xmlrpc/v1/xmlrpc.php'
    key = '4eb2733b98b4697bfd69d46cd8090c8c'
    from testlink import TestlinkAPIClient
    # t = TestlinkAPIClient(url,key)
    # print dir(t)
    # p = t.getProjects()
    # dx = p[5]
    # print dx.get('name')
    # #print dx
    # tp = t.getProjectTestPlans(dx['id'])
    # tp_id = tp[-1]['id']
    # tc = t.getTestCasesForTestPlan(tp_id)
    # buildname = t.getLatestBuildForTestPlan(tp_id)
    # t.getBuildsForTestPlan
    # print buildname
    # print type(tc)
    # #t.reportTCResult(testcaseid=self.testcaseid,testplanid=testplanid,status=result,notes='')
    # for i,j in tc.items():
    #     if j[0]['full_external_id'] == '1-1094':
    #         for k,l in j[0].items():
    #             print k,l
    #         case_id = j[0]['tcase_id']
    # b =u'Android湖北日报3.2.3发布性测试'
    # r = t.reportTCResult(testcaseid=case_id,testplanid=tp_id,status='f',buildname=b,notes='')
    # print r

    class TestLinkHandler(object):

        def __init__(self,test_project,test_plan,build_name,url = 'http://10.99.101.4/testlink/lib/api/xmlrpc/v1/xmlrpc.php',key = '4eb2733b98b4697bfd69d46cd8090c8c'):
            self._url = url
            self._key = key
            self.t = TestlinkAPIClient(url,key)
            self.test_project = test_project
            self.test_plan = test_plan
            self.build_name = build_name
            self.get_info()

        def get_info(self):
            self.project_id = self.t.getProjectIDByName(self.test_project)
            self.plan_id = self.t.getTestPlanByName(self.test_project,self.test_plan)[0]['id']
            print 'plan_id',self.plan_id

        def get_case_id(self,tc_full_id):
            tc = self.t.getTestCasesForTestPlan(self.plan_id)
            case_id = False
            for i,j in tc.items():
                if j[0]['full_external_id'] == tc_full_id:
                    case_id = j[0]['tcase_id']
            return case_id

        def set_tc_status(self,tc_full_id,status,notes=''):
            case_id = self.get_case_id(tc_full_id)
            result = self.t.reportTCResult(testcaseid=case_id,testplanid=self.plan_id,status=status,buildname=self.build_name,notes='')
            return result
    projects = u'湖北日报'
    plan = u'湖北日报3.2.3发布性测试'
    b = u'Android湖北日报3.2.3发布性测试'
    tkh = TestLinkHandler(projects,plan,b)
    print tkh.set_tc_status('1-1117','t')
    #print t.getLatestBuildForTestPlan
    # for i in tp:
    #     print i.get('name'),i.get('testproject_id'),i.get('id')
    #     print t.getTestCasesForTestPlan(i.get('id'))
    # for i in p:
    #     print i.get('name')
    #     print i.get('id')
    # pay = {
    #     'devKey': '4eb2733b98b4697bfd69d46cd8090c8c'
    # }
    # r = requests.post(url,pay)
    # print r.content