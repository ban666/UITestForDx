# -*- coding:utf-8 -*-
__author__ = 'Ban'

from case_config import CASE
import os
import sys

def get_case(fname):
    fname = os.path.split(fname)
    fname = os.path.splitext(fname[1])[0]
    func = sys._getframe().f_back.f_code.co_name
    name_func = '.'.join([fname,func])
    return CASE.get(name_func)

