# -*- coding: utf-8 -*-
__author__ = 'liaoben'
import chardet

class SubchnlApiLib:

    def db_ret_to_str(self,content):
        ret = [str(x[0]) for x in(content)]
        #ret.sort()
        return ','.join(ret)

    def db_ret_to_list(self,content):
        ret = [str(x[0]) for x in(content)]
        #ret.sort()
        return ret


    def json_to_str(self,content):
        ret = [str(x['id']) for x in content]
        #ret.sort()
        return ','.join(ret)

    def unicode_to_str(self,content):
        try:
            content = content.encode('utf-8')
        except:
            pass
        return content

    def str_compare(self,str_a,str_b):
        str_a = self.unicode_to_str(str_a)
        str_b = self.unicode_to_str(str_b)
        return str_a==str_b

    def get_key(self,params):
        return params.split('=')[0]

    def get_val(self,params):
        return params.split('=')[1]

    def result_check_for_chnl_request(self,subscirbed_channel,ret_json,title):
        subchnl_list = []
        title_check = True
        for i in subscirbed_channel:
            for j in i:
                subchnl_list.append(j)

        for i in range(len(ret_json)):
            if ret_json[i]['flag'] ==5:
                assert ret_json[i-1]['sortNum']<=30
                if len(ret_json)<=i:
                    assert ret_json[i+1]['sortNum']>=30

                loc_title = ret_json[i]['title']
                print chardet.detect(title[0][0])['encoding']
                if self.unicode_to_str(loc_title) !=self.unicode_to_str(title[0][0]):
                    title_check = False
                ret_json.pop(i)
                break

        for k in range(len(subchnl_list)):
            temp = {}
            temp['parent'] = subchnl_list[k][4]
            temp['title'] = subchnl_list[k][1]
            temp['flag'] = subchnl_list[k][2]
            temp['sortNum'] = subchnl_list[k][6]
            temp['recommend'] = subchnl_list[k][5]
            temp['model'] = subchnl_list[k][3]
            temp['id'] = subchnl_list[k][0]
            temp['visible']=1
            if temp['sortNum']>=10 and temp['sortNum']<=50:
                temp['recommend'] = 2
            if temp['sortNum']==40:
                temp['visible']=0
            subchnl_list[k]=temp

        #去重
        title_list = [x['title'] for x in subchnl_list]
        pop_list = []
        for i in range(len(title_list))[::]:
            if title_list[i] in title_list[:i]:
                pop_list.append(i)
        sorted(pop_list,reverse=True)
        for i in pop_list:
            subchnl_list.pop(i)

        print len(subchnl_list),len(ret_json)

        if len(subchnl_list)!=len(ret_json):
            for i in title_list:
                print i
            for j in ret_json:
                print j['title']

            return False

        for i in range(len(subchnl_list)):

            if subchnl_list[i]!=ret_json[i]:
                print 'errrrrrrr'
                print i
                for key,val in subchnl_list[i].items():
                    subchnl_list[i][key] = self.unicode_to_str(val)
                    ret_json[i][key] = self.unicode_to_str(ret_json[i][key])
                    if not subchnl_list[i][key]==ret_json[i][key]:
                        print subchnl_list[i][key],ret_json[i][key]
                        print i,key,val

                print subchnl_list[i]['title'],ret_json[i]['title']

        print subchnl_list == ret_json
        result = title_check and subchnl_list == ret_json
        print result
        return result

    def result_check_for_chnl_request_plugin(self,chnl_list,ret_json):
        chnl_list = list(chnl_list)
        print len(chnl_list),len(ret_json)
        if len(chnl_list) != len(ret_json):
            print 'length error!'
            return False

        for k in range(len(chnl_list)):
            temp = {}
            temp['title'] = self.unicode_to_str(chnl_list[k][1])
            temp['flag'] = chnl_list[k][2]
            temp['model'] = chnl_list[k][3]
            temp['id'] = chnl_list[k][0]
            chnl_list[k]=temp
        for i in range(len(chnl_list)):

            if chnl_list[i]!=ret_json[i]:
                print i
                for key,val in chnl_list[i].items():
                    chnl_list[i][key] = self.unicode_to_str(val)
                    ret_json[i][key] = self.unicode_to_str(ret_json[i][key])
                    if not chnl_list[i][key]==ret_json[i][key]:
                        print chnl_list[i][key],ret_json[i][key]
                        print i,key,val

                print chnl_list[i]['title'],ret_json[i]['title']
        print chnl_list == ret_json
        return chnl_list==ret_json

    def result_check_for_change_city(self,ret,city_information_force,city_information):
            info_list = city_information[0]
            if len(city_information_force)!=0:
                info_list = city_information_force[0]
            expect_info=ret['data']['list'][5]
            compart_list = ['id','title']
            expect_info_list = []
            for key in compart_list:
                expect_info_list.append(expect_info.get(key))
            print info_list[1],expect_info_list[1]
            result =  tuple(info_list)==tuple(expect_info_list)
            print result
            return result