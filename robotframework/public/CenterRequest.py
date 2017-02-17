# -*- coding: utf-8 -*-
__author__ = 'liaoben'

from RequestForDx import RequestForDx
from DbLib import DbLib
from mongo import Mongo
import back
import requests
import json
import os


class CenterRequest(RequestForDx):

    def __init__(self,mode,ec='420000000010000',cc='420106',p='a',v='3.1.2',ak='1',dc = '1,0,0,jv5RDypcLOG1Ho6UTgf8NN5sUcLGl4Zvk2eH3fH3wEI=#5942cf325a19a9d552f2ad6b617f235e',tid='a_imei865479020303095',pid = '100d855909470b42cd9',loc = '',chnl_para='cnhubei'):
        super(CenterRequest,self).__init__(ec,cc,p,v,ak,dc,tid,pid,loc,chnl_para)
        self.mode = mode
        self.dx_mode = 'mcp/dx'
        self.dx_plug_mode = 'mcp/plug/app'

    def get_suggest(self,content,*args):
        try:
            content = content.encode('utf-8')
        except:
            pass
        data=[self.mode+u'/1/user/suggest','content='+str(content)]
        for arg in args:
            data.append(arg)
        result=self.send_request_for_dx(*data)
        assert result['code']=='0'
        return True

