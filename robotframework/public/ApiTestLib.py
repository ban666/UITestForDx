# -*- coding: cp936 -*-
import json
import re
import hashlib
import sys
import types
import Cookie
import time
app_key = "sO&C%3Mq@lqY5PHt"
class ApiTestLib:
    def PickStr(self,substr,findstr):
         nPos = substr.index(findstr)
         N = len(findstr)
         getstr = substr[nPos+N:]
         return getstr
    def md5body(self,body):
		return hashlib.md5(body).hexdigest()
    def ToDic(self,str1):
        reload(sys)
	sys.setdefaultencoding('utf-8')
        dic = eval(str1)
        return dic
    def KeysToDic(self,str1,str2):
        keydic = []
        Pos = str1.rindex(str2)
        N = len(str2)
        lgetstr = str1[:Pos]
        rgetstr = str1[Pos+N:]
        ln = lgetstr.rindex("[")
        rn = rgetstr.index("]")
        i = str1[ln+1:Pos]
        j = str1[Pos+N:Pos+N+rn]
        key = str1[ln+1:Pos+N+rn]
        i = int (i)
        j = int (j)
        while i <= j:
            strkey = str1.replace(key,str(i))
            keydic.append(strkey)
            i += 1
        return keydic
    def Deunicode(self,str1):
        if type(str1) is types.StringType:    
            regex = '\\\u\w\w\w\w'
            results = re.findall (regex,str1)
            length = len(results)
            if length >= 1:
                decode_str = str1.decode('unicode_escape')
                return decode_str
        else:
            return str1
    def Deutf8(self,str1):
        return str1.decode('utf-8')
    def GetKeyList(self,data):
        lists = data.keys()
        return lists
    def ConvertToJson(self,data):
        json_data = json.dumps(data,ensure_ascii=False)
        return json_data
    def GetLastStr(self,substr,str1):
        nPos = substr.rindex(str1)
        getstr = substr[nPos+1:]
        return getstr
    def GetKeyListFromStr(self,data):
        reload(sys)
	sys.setdefaultencoding('utf-8')
        parts = data.split('":[{')
        parts.remove(parts[-1])
        parts1 = []
        for part in parts:
            part1 = self.GetLastStr(part,'"')
            parts1.append(part1)
        return parts1
    def GetTimeStamp(self):
        return "%d"%(time.time()*1000)



if __name__ == "__main__" :
    t = ApiTestLib()
    #print t.md5body("loginName=ludi&passwd=123456&nickName=nick1418614119")
    #print t.ToDic("{'aaa','bbb','ccc'}")
    #print t.PickStr("web/apk/tt.json","apk")
    #print t.KeysToDic("['data']['apps'][4***12]['package_name']","***")
    #print t.Deunicode("[{u'model': 14, u'flag': 0, u'id': 652278232246390784L, u'title': u'\u4e13\u9898'}, {u'model': 14, u'flag': 0, u'id': 999999999999999999L, u'title': u'\u70ed\u63a8'}")
    #print t.GetKeyList({"bbb": "111","aaa": "222","ccc": "333"})
    #print t.Deutf8("\xe6\xa0\xbc\xe5\xbc\x8f\xe9\x94\x99\xe8\xaf\xaf\xe3\x80\x82")
    #print t.GetLastStr('{"data":{"uc1','"')
    #print t.GetKeyListFromStr('{"data":{"uc1":[{"appid":31146,"title":"UCBrowser"},{"appid":21147,"title":"UCmobile"}],"uc2":[{"appid":31148,"title":"UCBrowser1"},{"appid":31149,"title":"UCBrowser2"}]}}')
    print t.GetTimeStamp()
