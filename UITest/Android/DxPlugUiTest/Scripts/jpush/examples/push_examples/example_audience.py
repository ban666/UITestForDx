import jpush as jpush
from conf import app_key, master_secret
_jpush = jpush.JPush(app_key, master_secret)
_jpush.set_logging("DEBUG")
push = _jpush.create_push()
# push.audience = jpush.audience(
#             # jpush.tag("tag1", "tag2"),
#             # jpush.alias("alias1", "alias2")
#         )
push.audience = jpush.audience(
            # jpush.tag("tag1", "tag2"),
            jpush.alias("420922")
        )
push.audience = 'all'
#jpush.audience()
push.notification = jpush.notification(alert="123!")
push.platform = jpush.all_
print (push.payload)
r = push.send()
print r
