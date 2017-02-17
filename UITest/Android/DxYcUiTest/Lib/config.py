# -*- coding: utf-8 -*-
__author__ = 'liaoben'

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '4.4.2'
desired_caps['deviceName'] = 'Nexus_7_2012_API_19'
desired_caps['appPackage'] = 'com.cnhubei.ycdx'
desired_caps['appActivity'] = 'com.cnhubei.home.module.splash.A_SplashActivity'
desired_caps['resetKeyboard'] = True
desired_caps['unicodeKeyboard'] = True

AK=7
EC=''
VERSION= '1.0.0'
MODE = 'mcp/plug/app'
IS_ROOT = False
TEST_PHONE = '13417771777'
DEVICE_TID = 'a_imei000000000000000'
PHONE_INFO = 'Nexus 6'
ISOTIMEFORMAT = '%Y-%m-%d %X'

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
CLUE_NINE_PIC = u'自动化九张图'



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
    'clue_pic':'com.cnhubei.clue.module.cluepicshow.A_CluePicShow',
    'install':'.PackageInstallerActivity',
    'index':'com.cnhubei.home.A_NewsHomeActivity',
    'unsupport':'com.cnhubei.libnews.module.normalweb.A_WebBrowserActivity',
    'search':'com.cnhubei.libnews.module.search.A_SearchActivity',
    'login':'com.cnhubei.home.module.login.A_UserResigerActivity',
    'clue_reply':'com.cnhubei.clue.module.cluereply.A_ClueReplyActivity',
}

APPIUM_URL = 'http://localhost:4723/wd/hub'
MSG = {
    'unsupport':u'您访问的页面不存在!',
    'cache_tips':u'确认要清除缓存吗？'
}

WAIT_TIME = 8

PIC_SAVE_PATH = 'f:/pic'
IMAGE_SAVE_DIR = 'cnhubei'

#APK DOWNLOAD
APK_PATH = 'g:/apk/'

BASE_PATH = 'g:/workspace/UITestForDx/DxYcUiTest/'

IMAGE_PATH = BASE_PATH+'Images'

#audio pic config
IMAGES = {
    'notification_pause':['notification_pause_nexus6.png','notification_pause.png','notification_pause_xiaomi4.png'],
    'notification_start':['notification_start_nexus6.png','notification_start.png','notification_pause_xiaomi4.png'],
    'image_30':'33.2M.jpg',
    'image_10.2':'10.2M.jpg',
    'image1':'1.jpg',
    '960_10000':'960_10000.jpg',
    '10630_4724':'10630_4724.jpg',
    '950_3953':'950_3953.jpg'
}

JPUSH_TIMEOUT=20
JPUSH_TITLE = u'宜昌动向'