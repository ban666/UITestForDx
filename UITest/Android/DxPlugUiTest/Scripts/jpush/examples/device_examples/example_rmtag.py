#-*- encoding:utf-8 -*-

import jpush as jpush
from conf import app_key, master_secret
_jpush = jpush.JPush(app_key, master_secret)
_jpush.set_logging("DEBUG")
device = _jpush.create_device()
tag = "ddd"
platform = "android,ios"
device.delete_tag(tag, platform)
