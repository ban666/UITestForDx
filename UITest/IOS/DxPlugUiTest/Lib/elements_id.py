# -*- coding: utf-8 -*-
__author__ = 'liaoben'

from selenium.webdriver.common.by import By
from appium.webdriver.common.mobileby import MobileBy

PACKAGE = 'com.cnhubei.ycdx'
PREFIX = PACKAGE+':id/'
BACK_BUTTON_LIST = [('id','ic fanhui grey'),('id','back white')]
BACK_BUTTON = ('id','ic fanhui grey')
PHOTO_BACK_BUTTON = ('id','back white')

START_BUTTON = {
    'normal':('id',u'新闻'),
    'no_share':('id',u'无分享新闻'),
    'no_fav':('id',u'无收藏新闻'),
    'no_share_fav':('id',u'无分享收藏新闻'),
    'my_fav':('id',u'我的收藏'),

}


#comment
COMMENT_ENTRANCE = ('id','btn news coments visited1')
COMMENT_ENTRANCE_AUDIO = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIAButton[2]')
COMMENT_INPUT_BUTTON = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIAButton[2]')
COMMENT_INPUT_EDIT = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIATextView[1]')
# COMMENT_SEND_CANCEL = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIAButton[2]')
# COMMENT_SEND_OK = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIAButton[3]')
COMMENT_ITEM = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[%d]')
COMMENT_VIEW = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIATableView[1]')
COMMENT_INPUT_IN_ARTICLE = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIATextField[1]')
COMMENT_SEND_OK = ('id',u'确定')
COMMENT_SEND_CANCEL = ('id',u'取消')
COMMENT_COUNT = {
    'normal':('xpath','//UIAApplication[1]/UIAWindow[1]/UIAStaticText[4]'),
    'photo':('xpath','//UIAApplication[1]/UIAWindow[1]/UIAStaticText[6]'),
    'audio':('xpath','//UIAApplication[1]/UIAWindow[1]/UIAButton[2]'),
}

COMMENT_DICT = {
    2:#嵌套评论
        {
            'content':('xpath','/UIAStaticText[3]'),
            'author':('xpath','/UIAStaticText[1]'),
            'loc_time':('xpath','/UIAStaticText[2]'),
            'digg_count':('xpath','/UIAStaticText[4]'),
            'quote_author_loc':('xpath','/UIAStaticText[5]'),
            'quote_content':('xpath','/UIAStaticText[6]'),
            'quote_button':('xpath','/UIAButton[1]'),
            'digg_button':('xpath','/UIAButton[2]'),

        },
    1:#非嵌套评论
        {
            'author':('xpath','/UIAStaticText[1]'),
            'loc_time':('xpath','/UIAStaticText[2]'),
            'content':('xpath','/UIAStaticText[3]'),
            'digg_count':('xpath','/UIAStaticText[4]'),
            'digg_button':('xpath','/UIAButton[1]'),
        }
}
COLLECT_BUTTON = ('id','ic collectGray')
COLLECT_BUTTON_TYPE_B = ('id','ic collect')
SHARE_BUTTON = ('id','btn news share gray')
FONT_BUTTON = ('id','font sidesGray')
DOWNLOAD_BUTTON = ('id','download')
SHARE_METHOD = {
    'pengyouquan':('id','UMS wechat timeline icon'),
    'weixin':('id','UMS wechat session icon'),
    'qq':('id', 'UMS qq icon'),
    'qzone':('id', 'UMS qzone icon'),
    'weibo':('id', 'UMS sina icon'),
    'sms':('id', 'UMS sms icon'),
    'email':('id', 'UMS email icon'),
    'copy':('id', 'UMS copylink icon')
}

MORE_COMMENTS = ('id',u'查看更多评论')

MY_COMMENT_PUBLISH_ITEM = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[1]/UIATableView[1]/UIATableCell[%d]')
MY_COMMENT_REPLY_ITEM = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[2]/UIATableView[1]/UIATableCell[%d]')
MY_COMMENT_VIEW = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[1]/UIATableView[1]')
MY_COMMENT_DICT = {
    2:#嵌套评论
        {
            'content':('xpath','/UIAStaticText[3]'),
            'author':('xpath','/UIAStaticText[1]'),
            'loc_time':('xpath','/UIAStaticText[2]'),
            'digg_count':('xpath','/UIAStaticText[4]'),
            'quote_author_loc':('xpath','/UIAStaticText[5]'),
            'quote_content':('xpath','/UIAStaticText[6]'),
            'quote_button':('xpath','/UIAStaticText[5]'),
            'article_link':('xpath','/UIAButton[1]'),
            'digg_button':('xpath','/UIAButton[2]'),

        },
    1:#非嵌套评论
        {
            'author':('xpath','/UIAStaticText[1]'),
            'loc_time':('xpath','/UIAStaticText[2]'),
            'content':('xpath','/UIAStaticText[3]'),
            'digg_count':('xpath','/UIAStaticText[4]'),
            'article_link':('xpath','/UIAButton[1]'),
            'digg_button':('xpath','/UIAButton[2]'),
        }
}

#menu
MENU_ICON = PREFIX+'iv_usercenter'
MY_COMM = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIATableView[2]/UIATableCell[1]/UIAButton[3]')
MY_FAV = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIATableView[2]/UIATableCell[1]/UIAButton[2]')
MY_BAOLIAO = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIATableView[2]/UIATableCell[1]/UIAButton[4]')
MY_INVITE = PREFIX+'layout_invite'
BACK = PREFIX+'btn_top_bar_back'

#login before
PHONE_LOGIN_ICON = ('id',u'立即登录')
WELCOME_MSG = PREFIX + 'tv_welcome'

#logined
USER_ICON = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIATableView[2]/UIATableCell[1]/UIAButton[1]')
USER_NAME = PREFIX+'user_name'
USER_COINS =PREFIX+'user_integral'

#login
PHONE_INPUT = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIATextField[1]')
GET_VCODE = ('id',u'获取验证码')
VCODE_INPUT = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIATextField[2]')
PHONE_CLEAR_BUTTON = ('id',u'清除文本')
PHONE_LOGIN_BUTTON = ('id',u'手机快速登录')

#clue
CLUE_ITEM = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[%d]/UIATableView[1]/UIATableCell[%d]')
CLUE_LIST_DICT = {
            'status':('xpath','/UIAStaticText[3]'),
            'author':('xpath','/UIAStaticText[1]'),
            'loc_time':('xpath','/UIAStaticText[2]'),
            'content':('xpath','UIAElement[1]'),
            'share':('xpath','/UIAButton[1]'),
            'comment':('xpath','/UIAButton[2]'),
            'digg':('xpath','/UIAButton[3]'),
        }
CLUE_DETAIL_COMMENT_BUTTON = ('id',u'评论')
CLUE_DETAIL_SHARE_BUTTON = ('id',u'转发')
CLUE_DETAIL_DIGG_BUTTON = ('id',u'赞')


#user center
ICON_CHANGE = PREFIX+'ll_user_icon'
NICK_VALUE = PREFIX+'nick_value'
TEL_VALUE = PREFIX+'telephone_value'
ADDRESS_VALUE = PREFIX+'address_value'
WEIBO_ACCOUNT = PREFIX+'tv_sina_account'
WEIXIN_ACCOUNT = PREFIX+'weixin_account'
QQ_ACCOUNT = PREFIX+'qq_account'
LOGOUT_BUTTON = ('id',u'登出')

#404page
UNSUPPORT_MSG = ('id',u'您访问的页面不存在!')


#mycomment
MY_COMM_SEND = ('id',u'发布评论')
MY_COMM_REPLY = ('id',u'回复我的')
COMM_SRC = PREFIX+'tv_src_url'

#index
INFORMATION = ('id','menu1 2')
HEAD = ('id','menu2 1')
DISCOVER = ('id','menu3 1')
MY_CONFIG = ('id','menu4 1')
SEARCH_BUTTON = [By.ID,"zoom white"]

#search
SEARCH_EDITTEXT = [By.XPATH,'//UIAApplication[1]/UIAWindow[1]/UIASearchBar[1]']
PAGEVIEW_COUNT = PREFIX+'tv_news_normal_comment'
HOTWORDS_TIPS = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIAStaticText[1]')
HOTWORDS_GROUP = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]')
SEARCH_EDITTEXT_CLEAR = ('id',u'清除文本')
SEARCH_EMPTY_TIPS = PREFIX + 'tv_empty_tips'
SEARCH_CANCEL = ['id',u'取消']
SEARCH_KEYBOARD = [By.ID,u"搜索"]
SEARCH_LIST_PV_COUNT = ['xpath','//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[1]/UIAStaticText[3]']

#article list
NORMAL_TITLE = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIAStaticText[1]')
NORMAL_IMAGE = PREFIX +'iv_news_normal'
THREE_PIC_TITLE = PREFIX +'tv_news_three_title'
THREE_PIC_IMAGE = [PREFIX +'iv_news_three_1',PREFIX +'iv_news_three_2',PREFIX +'iv_news_three_3']
ARTICLE_FLAG = PREFIX +'tv_news_normal_flag'
VIDEO_TITLE = PREFIX + 'tv_video_title'
VIDEO_IMAGE = PREFIX +'iv_video_img'
BIG_TITLE = PREFIX + 'tv_large_title'
BIG_IMAGE = PREFIX + 'iv_large_image'


#head
HEAD_HOT = PREFIX+'rb_head_hot'
HEAD_PUBLISH = PREFIX+'rb_head_publish'
HEAD_SHOWME = PREFIX+'rb_head_showme'
HEAD_REPLY_BUTTON = PREFIX+'layout_pl'
HEAD_REPLY_COUNT = PREFIX+'tv_pingluncount'
HEAD_DIGG_BUTTON = PREFIX+'iv_head_digg'
HEAD_DIGG_COUNT = PREFIX+'tv_zancount'
HEAD_CONTENT = PREFIX+'tv_descr'
HEAD_PIC = PREFIX+'gl'
HEAD_INPAGE_REPLY_COUNT = PREFIX+'tv_pl_count'
HEAD_INPAGE_DIGG_COUNT = PREFIX+'tv_zan_count'

#audio
# AUDIO_BG = PREFIX+'audio_bg'
# AUDIO_TITLE = PREFIX+'audio_title_tv'
# AUDIO_ICON = PREFIX+'cd_icon'
# AUDIO_START = PREFIX+'iv_audio_start'
# AUDIO_PAUSE = PREFIX+'iv_audio_pause'
# AUDIO_PLAY_TIME = PREFIX+'tv_audio_play_time'
# AUDIO_ALL_TIME = PREFIX+'tv_audio_all_time'
# AUDIO_PROGRESS = PREFIX+'audio_controller_progress'
# AUDIO_MENU = PREFIX+'menu_more'
# AUDIO_MENU_ITEMS = PREFIX+'textView1'
#
# AUDIO_CLOSE = PREFIX+'iv_audio_close'
#
# COMMENT_AUDIO_ENTRANCE = PREFIX+'toolbar_comment'
AUDIO_TITLE = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIAStaticText[3]')
AUDIO_START = ('id','btn news audio bofang')
AUDIO_PAUSE = ('id','btn news audio zhant')
AUDIO_START_IN_ARTICLE = ('id','icon news audiobofang')
AUDIO_PAUSE_IN_ARTICLE = ('id','icon news audiozhant')
AUDIO_PLAY_TIME = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIAStaticText[4]')
AUDIO_ALL_TIME = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIAStaticText[5]')
AUDIO_PROGRESS = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIASlider[2]')

#notification
NOTIFICATION_PAUSE = ('id',u'暂停')
NOTIFICATION_PLAY = ('id',u'播放')
NOTIFICATION_AUDIO_TITLE = ('xpath','//UIAApplication[1]/UIAWindow[7]/UIAButton[3]')
TOP_NOTIFICATION = ('xpath','//UIAApplication[1]/UIAWindow[4]/UIAButton[1]')
NOTIFICATION_BRITENESS = ('id','Brightness')
#通知栏
NOTIFICATION_TITLE = '/UIAStaticText[1]'
NOTIFICATION_TEXT = '/UIAStaticText[2]'
NOTIFICATION_TIME = '/UIAStaticText[3]'
NOTIFICATION_ICON = 'android:id/icon'
NOTIFICATION_OK = ('id',u'去看看')
NOTIFICATION_CANCEL = ('id',u'取消')
#NOTIFICATION_ITEM = 'com.android.systemui:id/content_view_group'  NEXUS6
NOTIFICATION_ITEM = '//UIAApplication[1]/UIAWindow[5]/UIAAlert[1]/UIAScrollView'
NOTIFICATION_BUTTON = ('id',u'通知')
#video
VIDEO_ITEM = ('id',u'视频')
VIDEO_START = ('id','kr video player play')
VIDEO_PAUSE = ('id','kr video player pause')
VIDEO_PROGRESS = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIASlider[2]')
VIDEO_TIME = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIAStaticText[5]')
VIDEO_DANMAKU = ('id','btn dmgb')
VIDEO_CLOSE = ('id','kr video player close')
VIDEO_ROTATE = PREFIX+'iv_video_rotate'
VIDEO_FULL_SCREEN = ('id','kr video player fullscreen')
VIDEO_PLAY_IMAGE = ('id','play.png')
VIDEO_TITLE_PLAYING = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIAStaticText[4]')
VIDEO_TITLE_PLAY_BEFORE = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIAStaticText[3]')
#
BUTTON_OK = PREFIX +'btn_ok'
BUTTON_CANCEL = PREFIX + 'btn_no'
CHNL_SUB_PAGE = PREFIX+'button_more_columns'
CHNL_SUBMIT = PREFIX+'tv_menu_post'

AMAZING_COMMENT_TIPS = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableGroup[1]/UIAStaticText[1]')

#settings
PUSH_OPTION = PREFIX+'cb_push'
LOCATION_SETIINGS = PREFIX+'choice_city_textView'
ACCOUNT_SETTINGS = PREFIX + 'll_account'
FONT_SETTINGS = PREFIX + 'll_set_zihao'
CACHE_CLEAR = PREFIX + 'tv_cache'
CACHE_CLEAR_CONFIRM = PREFIX + 'tv_quit'
CACHE_CLEAR_CANCEL = PREFIX + 'tv_cancel'
SUGGESTION = PREFIX+'layout_reply'
COVER_SETIINGS = PREFIX + 'll_see_fengmian'
VERSIONS = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIATableView[2]/UIATableCell[7]/UIAStaticText[2]')
ABOUT = PREFIX + 'layout_about_us'
CACHE_TIPS = PREFIX + 'tv_content'
MY_CLUE = PREFIX + 'layout_clue'

#suggestion
SUGGESTION_INPUT = PREFIX + 'et_leftmessage'
SUGGESTION_CONFIRM = PREFIX + 'tv_join_done'
SUGGESTION_CANCEL = PREFIX + 'tv_join_cancel'


#system
#NOTIFICATION_CLEAR_BUTTON = 'com.android.systemui:id/clear_notification' #华为荣耀
#NOTIFICATION_CLEAR_BUTTON ='com.android.systemui:id/dismiss_text' #虚拟机/Nexus6

NOTIFICATION_CLEAR_BUTTON = ('id',u'清除部分')
NOTIFICATION_CLEAR_CONFIRM = ('id',u'确认清除部分')

#live video
LIVE_VIDEO_BAR = PREFIX+'click_layout'


#xiaomi settings
XIAOMI_SETTINGS = 'com.android.systemui:id/settings_button'


ARTICLE_EMPTY_TIPS = ('xpath','//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[1]/UIAStaticText[1]')
EMPTY_CONTENT_TIPS = ('id',u'内容不存在，无法查看')
EMPTY_CONTENT_TIPS_CLUE = ('id',u'内容不存在,无法查看')
NETERROR_TIPS = ('id',u'点击屏幕 重新加载')


#update dialog
UPDATE_DIALOG = ('class','UIAAlert')
UPDATE_BUTTON = ('id',u'去更新')
IGNORE_BUTTON = ('id',u'忽略')
UPDATE_MSG = ('xpath','//UIAApplication[1]/UIAWindow[5]/UIAAlert[1]/UIAScrollView[1]/UIAStaticText[2]')
IGNORE_BOX = PREFIX + 'checkBox'
BACK_APP_BUTTON = ('id',u'返回“宜昌动向”')
#article_toolbar
TOOLBAR_ITEM = PREFIX+'toolbar_rel'
# COMMENT_ITEM = PREFIX+'rl_coments'
# SHARE_BUTTON = PREFIX+'ic_share'
#COLLECT_BOTTON = PREFIX+'ic_favorite'

#share
SHARE_METHOD_IMAGE = PREFIX + 'socialize_image_view'
SHARE_METHOD_TEXT = PREFIX + 'socialize_text_view'

#clue
# SUBTYPE_1 = PREFIX + 'button_1'
# SUBTYPE_2 = PREFIX + 'button_2'
# SUBTYPE_3 = PREFIX + 'button_3'
# SUBTYPE_4 = PREFIX + 'button_4'
# CLUE_LIST_MY_CLUE_ENTRY = PREFIX + 'action_wodebaoliao'
# CLUE_SEARCH = PREFIX + 'action_search'
# CLUE_LIST_ICON = PREFIX + 'iv_user'
# CLUE_LIST_USERNAME = PREFIX + 'tv_name'
# CLUE_LIST_TIME = PREFIX + 'tv_time'
# CLUE_LIST_FLAG = PREFIX + 'tv_flag'
# CLUE_LIST_DESC = PREFIX + 'tv_descr'
# CLUE_LIST_PIC = PREFIX + 'gl'
# CLUE_LIST_SHARE_BUTTON = PREFIX + 'll_share'
# CLUE_LIST_COMMENT_COUNT = PREFIX + 'tv_comment'
# CLUE_LIST_COMMENT_BUTTON = PREFIX + 'll_comment'
# CLUE_LIST_DIGG_COUNT = PREFIX + 'tv_dianzan'
# CLUE_LIST_DIGG_BUTTON = PREFIX + 'll_dianzan'
# CLUE_LOCATION = PREFIX + 'tv_location'
# SEND_CLUE_BUTTON = PREFIX + 'iv_baoliao'
MY_CLUE_BUTTON = ('id','ic wodebaoliao white')

#send clue
SEND_CLUE_TYPE_CHOOSE = PREFIX + 'rl_type'
SEND_CLUE_TYPE_TXT = PREFIX + 'textview'
SEND_CLUE_TYPE_CHECK = PREFIX + 'check'
SEND_CLUE_DESC_INPUT = PREFIX + 'et_context'
SEND_CLUE_IMAGE_ADD = PREFIX + 'imageView'
SEND_CLUE_LOCATION = PREFIX + 'tv_location'
SEND_CLUE_ANONYMOUS = PREFIX + 'cb_push'
SEND_CLUE_CONFIRM_BUTTON = PREFIX + 'tv_reply'
LOCATION_EDIT_TEXT = PREFIX + 'et_location'
LOCATION_EDIT_OK = PREFIX + 'btn_submit'
LOCATION_EDIT_CANCEL = PREFIX + 'btn_cancel'