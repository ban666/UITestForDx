# -*- coding: utf-8 -*-
__author__ = 'liaoben'

from conf import *

class StructCheck(object):

    def sturct_init(self,content,model,struct_type='dx_plug'):
        self.data = content
        self.model = model
        self._model,self._struct = type_struct[struct_type]
        self.struct = self._struct.get(self._model.get(self.model))

    def keys_compare(self,d1):
        result=False
        keys_list=d1.keys().sort()
        if isinstance(self.struct,type(None)):
            print 'No type match'
            return False
        print keys_list,self.struct.sort()
        if self.struct.sort() == keys_list:
            result = True
        return result

    def struct_check(self,content,model):
        self.sturct_init(content,model)
        result = False
        print type(self.data)
        print self.data
        if isinstance(self.data,dict):
            result = self.keys_compare(self.data)

        if isinstance(self.data,list):
            result = self.keys_compare(self.data[0])
        return result