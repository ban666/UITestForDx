import jpush as jpush
from conf import app_key, master_secret
_jpush = jpush.JPush(app_key, master_secret)
_jpush.set_logging("DEBUG")
push = _jpush.create_push()
# push.audience = jpush.audience(
#             # jpush.tag("tag1", "tag2"),
#             # jpush.alias("alias1", "alias2")
#         )
# push.audience = jpush.audience(
#             # jpush.tag("tag1", "tag2"),
#             jpush.registration_id('18171adc0301c6f4d0d')
#         )
push.options = {"time_to_live":86400, "sendno":12345,"apns_production":False}
push.audience = 'all'
#jpush.audience()
push.notification = jpush.notification(alert="123!")
push.platform = jpush.all_
print (push.payload)
r = push.send()
print r
