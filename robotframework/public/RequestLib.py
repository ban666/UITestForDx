import json
import re
import hashlib
import sys
import types
secret = "yJfRVvn6u9yCpn"
class RequestLib:
    def Sign(self,paramlist):
        paramlist.sort()
        ParamString = secret+"".join(paramlist)+secret
        return hashlib.md5(ParamString).hexdigest()
    def ListToRequestbody(self,paramlist):
        RequestBody = "&".join(paramlist)
        return RequestBody
