# -*- coding: utf-8 -*-
__author__ = 'liaoben'

import os

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '4.4.2'
desired_caps['deviceName'] = 'Nexus_7_2012_API_19'
desired_caps['appPackage'] = 'com.cnhubei.dxxwhw'
desired_caps['appActivity'] = 'com.cnhubei.dxxwhw.MainActivity'
desired_caps['resetKeyboard'] = True
desired_caps['unicodeKeyboard'] = True

MODE = 'mcp/plug/app'

TEST_PHONE = '13417771777'
DEVICE_TID = 'a_imei000000000000000'

NORMAL_ARTICLE = u'自动化文字新闻'
VIDEO_ARTICLE = u'自动化视频新闻'
EXT_ARTICLE = u'自动化外链新闻'
PHOTO_ARTICLE = u'自动化组图新闻'
AUDIO_ARTICLE = u'自动化音频新闻'
AUDIO_ARTICLE_B = u'自动化音频B新闻'
WONDERFUL_COMMENT_ARTICLE = u'自动化评论测试'
NO_COMMENT_ARTICLE = u'自动化无评论新闻'
NORMAL_AUDIO_ARTICLE = u'自动化正文音频新闻'
NORMAL_AUDIO_ARTICLE_B = u'自动化正文音频B新闻'
UNSUPPORT_ARTICLE = u'自动化不识别model新闻'
LIVE_VIDEO_ARTICLE = u'自动化直播视频新闻'

FLAG_ARTICLE = u'自动化角标新闻'
TARGETURL_ARTICLE = u'自动化targeturl新闻'
ZHUANTI_ARTICLE = u'自动化专题新闻'
ZHUANLAN_ARTICLE = u'自动化专栏'
LONG_TITLE_ARTICLE = u'自动化标题好长好长好长好长好长好长好长好长好长新闻'

#style test
SINGLE_PIC_ARTICLE = u'自动化小图新闻'
THREE_PIC_ARTICLE = u'自动化三小图新闻'
BIG_PIC_ARTICLE = u'自动化大图新闻'



ACTIVITY = {
    NORMAL_ARTICLE:'com.cnhubei.libnews.module.nativenews.A_HtmlBrowserActivity',
    PHOTO_ARTICLE:'com.cnhubei.libnews.module.photos.A_PhotosActivity',
    EXT_ARTICLE:'com.cnhubei.libnews.module.normalweb.A_WebBrowserActivity',
    VIDEO_ARTICLE:'com.cnhubei.libnews.module.videonewsdetail.A_VideoCommentListActivity',
    AUDIO_ARTICLE:'com.cnhubei.libnews.module.audio.A_AudioActivity',
    ZHUANTI_ARTICLE:'com.cnhubei.libnews.module.specialtopic.A_SpecialActivity',
    ZHUANLAN_ARTICLE:'com.cnhubei.libnews.module.specialcolumnlist.A_SpecialcolumnActivity',
    NORMAL_AUDIO_ARTICLE:'com.cnhubei.libnews.module.nativenews.A_HtmlBrowserActivity',
    LIVE_VIDEO_ARTICLE:'com.cnhubei.libnews.module.videonewsdetail.A_VideoCommentListActivity',
    'comment':'com.cnhubei.libnews.module.newscommentlist.A_CommentListActivity',
    'clue':'com.cnhubei.clue.module.cluedetail.A_ClueDetailActivity',
    'install':'.PackageInstallerActivity',
    'index':'com.cnhubei.home.A_NewsHomeActivity',
    'unsupport':'com.cnhubei.libnews.module.normalweb.A_WebBrowserActivity',
    'search':'com.cnhubei.libnews.module.search.A_SearchActivity',
}

APPIUM_URL = 'http://localhost:4723/wd/hub'
MSG = {
    'unsupport':u'您访问的页面不存在!'
}


WAIT_TIME = 8

PIC_SAVE_PATH = 'f:/pic'

#APK DOWNLOAD
APK_PATH = 'g:/apk/'

#audio pic config
IMAGES = {
    'notification_pause':['notification_pause_nexus6.png','notification_pause.png','notification_pause_xiaomi4.png'],
    'notification_start':['notification_start_nexus6.png','notification_start.png','notification_pause_xiaomi4.png']
}


BASE_DIR = os.path.dirname((os.path.dirname(os.path.abspath(__file__))))

JPUSH_TIMEOUT=20
JPUSH_TITLE = u'宜昌动向'

DISTRIBUTE_CONFIG_PATH = BASE_DIR+'/Config/distribute_config.txt'
#audio pic config
# IMAGES = {
#     'notification_pause':['notification_pause_nexus6.png','notification_pause.png','notification_pause_xiaomi4.png'],
#     'notification_start':['notification_start_nexus6.png','notification_start.png','notification_pause_xiaomi4.png']
# }
