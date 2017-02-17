# -*- coding: utf-8 -*-
__author__ = 'liaoben'

desired_caps={
    'app': 'com.cnhubei.ycdx',
    'udid':'16f8e9bde0d805ab524a9db4d79fb63e79b26015',
    'platformName': 'iOS',
    'platformVersion': '8.3',
    'deviceName': 'iPhone 6',
    'appium-version':'1.0',
    'unicodeKeyboard':True,
    'resetKeyboard':True
}

AK=7
EC=''
VERSION= '1.0.0'
MODE = 'mcp/plug/app'
IS_ROOT = True
TEST_PHONE = '13417771777'
DEVICE_TID = 'a_imei000000000000000'
PHONE_INFO = 'Nexus 6'

NORMAL_ARTICLE = u'自动化文字新闻'
VIDEO_ARTICLE = u'自动化视频新闻'
VIDEO_ARTICLE_B = u'自动化视频B新闻'
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
NORMAL_VIDEO_ARTICLE = u'自动化正文视频新闻'
NORMAL_VIDEO_ARTICLE_B = u'自动化正文视频B新闻'

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
    'clue_pic':'com.cnhubei.clue.module.cluepicshow.A_CluePicShow',
    'install':'.PackageInstallerActivity',
    'index':'com.cnhubei.home.A_NewsHomeActivity',
    'unsupport':'com.cnhubei.libnews.module.normalweb.A_WebBrowserActivity',
    'search':'com.cnhubei.libnews.module.search.A_SearchActivity',
    'login':'com.cnhubei.home.module.login.A_UserResigerActivity',
    'clue_reply':'com.cnhubei.clue.module.cluereply.A_ClueReplyActivity',
}

APPIUM_URL = 'http://10.99.13.46:4723/wd/hub'
MSG = {
    'unsupport':u'您访问的页面不存在!',
    'cache_tips':u'确认要清除缓存吗？'
}

WAIT_TIME = 8

PIC_SAVE_PATH = 'f:/pic'

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