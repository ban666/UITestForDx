import jpush as jpush
from conf import app_key, master_secret
# _jpush = jpush.JPush(app_key, master_secret)
# _jpush.set_logging("DEBUG")
# push = _jpush.create_push()
# push.audience = jpush.all_
# android_msg = jpush.android(alert="Hello, android msg",extras={"t":"2","i":"762545419699097600"})
# push.notification = jpush.notification(alert="Hello, world!",android=android_msg)
# push.platform = jpush.all_
# #push.options = {"t":"2","i":"762545419699097600"}
# #push.options = {"time_to_live":86400, "sendno":12345,"apns_production":True}
# push.send()


if __name__ == '__main__':
    class JpushHandler:

        def __init__(self,app_key,master_secret):
            self._app_key = app_key
            self._master_secret = master_secret
            self._jpush = jpush.JPush(app_key, master_secret)
            self._jpush.set_logging("DEBUG")

        def push_notification(self,msg,platform='all',audience = 'all'):
            p = {
                'all':jpush.all_ ,
                'android':jpush.platform('android'),
                'ios':jpush.platform('ios')
            }
            a = {
                'all':jpush.all_ ,
            }
            self.push = self._jpush.create_push()
            self.push.audience = a.get(audience)
            self.push.platform = p.get(platform)
            self.push.notification = jpush.notification(alert=msg)
            return self.push.send()

        def push_extra(self,extra,msg='test',platform='all',audience = 'all'):
            p = {
                'all':jpush.all_ ,
                'android':jpush.platform('android'),
                'ios':jpush.platform('ios')
            }
            a = {
                'all':jpush.all_ ,
            }
            a_msg = jpush.android(alert=msg,extras=extra)
            i_msg = jpush.ios(alert=msg,extras=extra)
            self.push = self._jpush.create_push()
            self.push.audience = a.get(audience)
            self.push.platform = p.get(platform)
            self.push.notification = jpush.notification(alert =msg,android=a_msg,ios=i_msg)
            return self.push.send()

    JH = JpushHandler(app_key,master_secret)
    option = {"t":"2","i":"762545419699097600"}
    JH.push_extra(option)