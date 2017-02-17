# -*- coding: utf-8 -*-
__author__ = 'liaoben'

WAIT_TIME = 5

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '4.4.2'
desired_caps['deviceName'] = 'Nexus_7_2012_API_19'
desired_caps['appPackage'] = 'com.zc.hubei_news'
desired_caps['appActivity'] = 'com.cnhubei.dx.home.A_SplashActivity'
desired_caps['resetKeyboard'] = True
desired_caps['unicodeKeyboard'] = True
desired_caps['CapabilityType.BROWSER_NAME'] = "Chrome"


desired_caps_plug = {}
desired_caps_plug['platformName'] = 'Android'
desired_caps_plug['platformVersion'] = '4.4.2'
desired_caps_plug['deviceName'] = 'Nexus_7_2012_API_19'
desired_caps_plug['appPackage'] = 'com.cnhubei.dxxwhw'
desired_caps_plug['appActivity'] = 'com.cnhubei.dxxwhw.MainActivity'
desired_caps_plug['resetKeyboard'] = True
desired_caps_plug['unicodeKeyboard'] = True

#未root的手机需先用测试手机号登录过一次
TEST_PHONE = '13417771777'
DEVICE_TID = 'a_imei000000000000000'
ISOTIMEFORMAT = '%Y-%m-%d %X'
ISODAYFORMAT = '%m-%d'
CLUE_TIME_FORMAT = '%m-%d %H:%M'

NORMAL_ARTICLE = u'自动化文字新闻'
VIDEO_ARTICLE = u'自动化视频新闻'
EXT_ARTICLE = u'自动化外链新闻'
PHOTO_ARTICLE = u'自动化组图新闻'
AUDIO_ARTICLE = u'自动化音频新闻'
WONDERFUL_COMMENT_ARTICLE = u'自动化评论测试'
NO_COMMENT_ARTICLE = u'自动化无评论新闻'
NORMAL_AUDIO_ARTICLE = u'自动化正文音频新闻'
FLAG_ARTICLE = u'自动化角标新闻'
TARGETURL_ARTICLE = u'自动化targeturl新闻'
ZHUANTI_ARTICLE = u'自动化专题新闻'
ZHUANLAN_ARTICLE = u'自动化专栏'
LIVE_VIDEO_ARTICLE = u'自动化直播视频新闻'
FOCUS_ARTICLE = u'自动化焦点图新闻'
HEAD_ARTICLE = u'自动化报料测试'
STATUS_ARTICLE = u'自动化状态测试'

#style test
SINGLE_PIC_ARTICLE = u'自动化小图新闻'
THREE_PIC_ARTICLE = u'自动化三小图新闻'
BIG_PIC_ARTICLE = u'自动化大图新闻'

#top_bar_title
LOGIN_TOP_TITLE = u'湖北日报登录'


#other
NINE_IMAGES_CLUE_KEYWORD = u'九张图对比截图专用'
DEFAULT_LOC = u'湖北日报'

ACTIVITY = {
    NORMAL_ARTICLE:'com.cnhubei.dx.core.A_HtmlBrowserActivity',
    FOCUS_ARTICLE:'com.cnhubei.dx.core.A_HtmlBrowserActivity',
    PHOTO_ARTICLE:'com.cnhubei.dx.common.A_ShowImageActivity',
    EXT_ARTICLE:'com.cnhubei.dx.core.A_WebBrowserActivity',
    VIDEO_ARTICLE:'com.cnhubei.dx.video.A_VideoCommentListActivity',
    LIVE_VIDEO_ARTICLE:'com.cnhubei.dx.video.A_VideoCommentListActivity',
    ZHUANTI_ARTICLE:'com.cnhubei.dx.news.A_SpecialActivity',
    ZHUANLAN_ARTICLE:'com.cnhubei.dx.news.A_FeatureActivity',
    TARGETURL_ARTICLE:'com.cnhubei.dx.user.A_AboutActivity',
    'comment':'com.cnhubei.dx.common.A_CommentListActivity',
    'index':'com.cnhubei.dx.home.A_MainActivity',
    'unsupport':'com.cnhubei.dx.user.A_AboutActivity',
    'first_start':'com.cnhubei.dx.home.A_WelcomeActivity',
    'head':'com.cnhubei.dx.common.A_HeadCommentListActivity',
    'search':'com.cnhubei.dx.news.A_SearchNewsActivity',
    'newspaper':'com.cnhubei.dx.core.A_HtmlBrowserActivity',
    'image':'com.cnhubei.dx.common.A_ShowImageActivity'
}

MODE = 'mcp/dx'
APPIUM_URL = 'http://localhost:4723/wd/hub'


#jpush settings
JPUSH_TIMEOUT = 20
JPUSH_TITLE = u'湖北日报'

#APK DOWNLOAD
APK_PATH = 'f:/apk/'
PIC_SAVE_PATH = 'f:/pic/'
IMAGE_SAVE_DIR = 'dongxiang'

#search_postion = (712,1048)
search_postion = {
    'Nexus 6':(1351,2277), #nexus 6
    'default':(1000,1715)  #机型相关配置,LiaoBen(712,1048),LuDi(1000,1715)
}

is_root = False