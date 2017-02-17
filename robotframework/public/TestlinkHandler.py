# -*- coding: utf-8 -*-
__author__ = 'liaoben'

from testlink import TestlinkAPIClient


class TestLinkHandler(object):

        def __init__(self,enable,test_project,test_plan,build_name,url = 'http://10.99.101.4/testlink/lib/api/xmlrpc/v1/xmlrpc.php',key = '4eb2733b98b4697bfd69d46cd8090c8c'):
            self._url = url
            self._key = key
            self.t = TestlinkAPIClient(url,key)
            self.test_project = test_project
            self.test_plan = test_plan
            self.build_name = build_name
            self.enable = enable
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
            status_dict = {
                True:'p',
                'True':'p',
                False:'f',
                'False':'f',
                1:'p',
                '1':'p',
                0:'f',
                '0':'f'
            }
            if self.enable == True or self.enable == 'True':
                case_id = self.get_case_id(tc_full_id)
                result = self.t.reportTCResult(testcaseid=case_id,testplanid=self.plan_id,status=status_dict.get(status),buildname=self.build_name,notes=notes)
                return result



if __name__ == '__main__':
    projects = u'湖北日报'
    plan = u'湖北日报3.2.3发布性测试'
    b = u'Android湖北日报3.2.3发布性测试'
    tkh = TestLinkHandler(1,projects,plan,b)
    print tkh.set_tc_status('1-1117',1)