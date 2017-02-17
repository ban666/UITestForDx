# -*- coding: utf-8 -*-
__author__ = 'liaoben'
import jpush as jpush
from jpush_config import app_key, master_secret


class JpushHandler:

        def __init__(self,app_key=app_key,master_secret=master_secret):
            self._app_key = app_key
            self._master_secret = master_secret
            self._jpush = jpush.JPush(app_key, master_secret)
            self._jpush.set_logging("WARNING")

        def push_notification(self,msg,platform='all',audience =jpush.all_):
            p = {
                'all':jpush.all_ ,
                'android':jpush.platform('android'),
                'ios':jpush.platform('ios')
            }
            if audience != jpush.all_:
                audience =  jpush.audience(jpush.alias(str(audience)))
            try:
                msg = msg.encode('utf-8')
            except:
                pass
            #print audience
            self.push = self._jpush.create_push()
            self.push.audience = audience
            self.push.platform = p.get(platform)
            self.push.notification = jpush.notification(alert=msg)
            return self.push.send()

        def push_extra(self,extra,msg='test',platform='all',audience =jpush.all_):
            p = {
                'all':jpush.all_ ,
                'android':jpush.platform('android'),
                'ios':jpush.platform('ios')
            }
            if audience != jpush.all_:
                audience =  jpush.audience(jpush.alias(str(audience)))
            try:
                msg = msg.encode('utf-8')
            except:
                pass
            a_msg = jpush.android(alert=msg,extras=extra)
            i_msg = jpush.ios(alert=msg,extras=extra)
            self.push = self._jpush.create_push()
            self.push.audience = audience
            self.push.platform = p.get(platform)
            self.push.notification = jpush.notification(alert =msg,android=a_msg,ios=i_msg)
            return self.push.send()

        def push_article(self,t,i,msg='test',platform='all',audience = jpush.all_):
            if audience != jpush.all_:
                audience =  jpush.audience(jpush.alias(str(audience)))
            extra = {'t':str(t),'i':str(i)}
            return self.push_extra(extra,msg,platform,audience)


if __name__ == '__main__':
    j = JpushHandler()
    j.push_article(4424,814639314754605056,u'test')
    #j.push_notification('1',audience='422800')
