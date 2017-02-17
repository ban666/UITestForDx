# -*- coding: utf-8 -*-
__author__ = 'liaoben'

PACKAGE = 'com.cnhubei.ycdx'
PREFIX = PACKAGE+':id/'

#comment
COMMENT = PREFIX+'rl_comment'
DIGG_COUNT = PREFIX+'tv_digg'
DIGG_BUTTON = PREFIX+'iv_common_zan'
LOC_TIME = PREFIX+'tv_loc_time'
QUOTE_COMMENT = PREFIX+'ll_quote'
QUOTE_NAME = PREFIX+'tv_quote_uname'
COMMENT_ICON = PREFIX+'civ_uicon'
COMMENT_NAME = PREFIX+'tv_uname'
COMMENT_TEXT = PREFIX+'expandable_text'
COMMENT_INPUT = PREFIX+'comment_content_edt'
COMMENT_SENT_BUTTON = PREFIX+'comment_send_text'
COMMENT_COUNT = PREFIX+'comment_number_text'
SUPPORT_BUTTON = PREFIX+'ll_pop_support'
REPLY_BUTTON = PREFIX+'ll_pop_reply'
COPY_BUTTON = PREFIX+'ll_pop_copy'

MY_COMM_SUPPORT_BUTTON = PREFIX+ 'll_pop_speech'

COMMENT_EDIT_TEXT = PREFIX+'et_content'
COMMENT_SEND_OK = PREFIX+'btn_comment_ok'
COMMENT_SEND_CANCEL = PREFIX+'btn_comment_cancel'

COMMENT_PHOTO_ENTRANCE = PREFIX+'toolbar_comment'
VIDEO_FORBBIDEN_COMMENT = PREFIX+'empty_text'
NONE_COMMENT_TEXT = PREFIX+'empty_text'

#menu
MENU_ICON = PREFIX+'iv_usercenter'
MY_COMM = PREFIX+'layout_comment'
MY_FAV = PREFIX+'layout_collect'
MY_BAOLIAO = PREFIX+'layout_clue'
MY_INVITE = PREFIX+'layout_invite'
BACK = PREFIX+'btn_top_bar_back'

#login before
PHONE_LOGIN_ICON = PREFIX+'img_icon'
WELCOME_MSG = PREFIX + 'tv_welcome'



#logined
USER_ICON = PREFIX+'img_icon'
USER_NAME = PREFIX+'user_name'
USER_COINS =PREFIX+'user_integral'

#login
PHONE_INPUT = PREFIX+'user_resiger_telephone'
GET_VCODE = PREFIX+'user_resiger_getvcode'
VCODE_INPUT = PREFIX+'user_resiger_vcode'
PHONE_CLEAR_BUTTON = PREFIX+'iv_clear'
PHONE_LOGIN_BUTTON = PREFIX+'user_resiger_login'
WEIXIN_LOGIN_BUTTON = PREFIX+'ll_weixin'
QQ_LOGIN_BUTTON = PREFIX+'ll_qq'
WEIBO_LOGIN_BUTTON = PREFIX+'ll_weibo'

#user center
ICON_CHANGE = PREFIX+'ll_user_icon'
NICK_VALUE = PREFIX+'nick_value'
TEL_VALUE = PREFIX+'telephone_value'
ADDRESS_VALUE = PREFIX+'address_value'
WEIBO_ACCOUNT = PREFIX+'tv_sina_account'
WEIXIN_ACCOUNT = PREFIX+'weixin_account'
QQ_ACCOUNT = PREFIX+'qq_account'
LOGOUT_BUTTON = PREFIX+'ll_logout'



#mycomment
MY_COMM_SEND = PREFIX+'button_1'
MY_COMM_REPLY = PREFIX+'button_2'
COMM_SRC = PREFIX+'tv_src_url'

#index
INFORMATION = PREFIX+'button_1'
HEAD = PREFIX+'button_2'
DISCOVER = PREFIX+'button_3'
MY_CONFIG = PREFIX+'button_4'
SEARCH_BUTTON = PREFIX+'action_search'

#search
SEARCH_EDITTEXT = PREFIX+'toolbar_et_search'
PAGEVIEW_COUNT = PREFIX+'tv_news_normal_comment'
HOTWORDS_TIPS = PREFIX+'tv_tips'
HOTWORDS_GROUP = PREFIX +'tag_listview'
SEARCH_EMPTY_TIPS = PREFIX + 'tv_empty_tips'
SEARCH_CANCEL = PREFIX + 'toolbar_img_delete'

#article list
NORMAL_TITLE = PREFIX +'tv_news_normal_title'
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
IMAGE_ALL = PREFIX + 'btnAlbum'
SEND_CLUE_IMAGE = PREFIX + 'gridView'

#audio
AUDIO_BG = PREFIX+'audio_bg'
AUDIO_TITLE = PREFIX+'audio_title_tv'
AUDIO_ICON = PREFIX+'cd_icon'
AUDIO_START = PREFIX+'iv_audio_start'
AUDIO_PAUSE = PREFIX+'iv_audio_pause'
AUDIO_PLAY_TIME = PREFIX+'tv_audio_play_time'
AUDIO_ALL_TIME = PREFIX+'tv_audio_all_time'
AUDIO_PROGRESS = PREFIX+'audio_controller_progress'
AUDIO_MENU = PREFIX+'menu_more'
AUDIO_MENU_ITEMS = PREFIX+'textView1'

AUDIO_CLOSE = PREFIX+'iv_audio_close'

COMMENT_AUDIO_ENTRANCE = PREFIX+'toolbar_comment'

#notification
NOTIFICATION_AUDIO_ICON = PREFIX+'custom_song_icon'
NOTIFICATION_AUDIO_TITLE = PREFIX+'tv_custom_song_name'
NOTIFICATION_AUDIO_PLAY = PREFIX+'btn_custom_play'
NOTIFICATION_AUDIO_CLOSE = PREFIX+'btn_custom_close'

#通知栏
NOTIFICATION_TITLE = 'android:id/title'
NOTIFICATION_TEXT = 'android:id/text'
NOTIFICATION_ICON = 'android:id/icon'
#NOTIFICATION_ITEM = 'com.android.systemui:id/content_view_group'  NEXUS6
NOTIFICATION_ITEM = {
    'Huawei':'com.android.systemui:id/content',
    'default':'com.android.systemui:id/expanded',
    'Nexus 6':'com.android.systemui:id/expanded',
    'MI 3W':'com.android.systemui:id/content'
    }

#video
VIDEO_ITEM = PREFIX+'video_item_image_rl'
VIDEO_START_PAUSE =PREFIX+ 'iv_video_pause_start'
VIDEO_PROGRESS = PREFIX+'media_controller_progress'
VIDEO_TIME = PREFIX+'tv_video_time'
VIDEO_DANMAKU = PREFIX+'iv_danmaku_show'
VIDEO_CLOSE = PREFIX+'iv_video_close'
VIDEO_ROTATE = PREFIX+'iv_video_rotate'

#
BUTTON_OK = PREFIX +'btn_ok'
BUTTON_CANCEL = PREFIX + 'btn_no'
CHNL_SUB_PAGE = PREFIX+'button_more_columns'
CHNL_SUBMIT = PREFIX+'tv_menu_post'

AMAZING_COMMENT_TIPS = PREFIX +'tv_typetitle'

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
VERSION = PREFIX + 'tv_version'
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

NOTIFICATION_CLEAR_BUTTON = {
    'MI 3W':'com.android.systemui:id/clear_all_button',  #xiaomi
    'Nexus 6':'com.android.systemui:id/dismiss_text',
    'default':'com.android.systemui:id/dismiss_text',
    'Huawei':'com.android.systemui:id/clear_notification'
}

#live video
LIVE_VIDEO_BAR = PREFIX+'click_layout'


#xiaomi settings
XIAOMI_SETTINGS = 'com.android.systemui:id/settings_button'


ARTICLE_EMPTY_TIPS = PREFIX +'tv_netempty'
NETERROR_TIPS = PREFIX + 'tv_neterror'


#update dialog
UPDATE_DIALOG = PREFIX+'dialog_view'
UPDATE_MSG = PREFIX+'tv_msm'
IGNORE_BOX = PREFIX + 'checkBox'

#article_toolbar
TOOLBAR_ITEM = PREFIX+'toolbar_rel'
COMMENT_ITEM = PREFIX+'rl_coments'
SHARE_BUTTON = PREFIX+'ic_share'
COLLECT_BOTTON = PREFIX+'ic_favorite'

#share
SHARE_METHOD_IMAGE = PREFIX + 'socialize_image_view'
SHARE_METHOD_TEXT = PREFIX + 'socialize_text_view'

#clue
SUBTYPE = PREFIX + 'button_'
SUBTYPE_1 = PREFIX + 'button_1'
SUBTYPE_2 = PREFIX + 'button_2'
SUBTYPE_3 = PREFIX + 'button_3'
SUBTYPE_4 = PREFIX + 'button_4'
CLUE_LIST_MY_CLUE_ENTRY = PREFIX + 'action_wodebaoliao'
CLUE_SEARCH = PREFIX + 'action_search'
CLUE_LIST_ICON = PREFIX + 'iv_user'
CLUE_LIST_USERNAME = PREFIX + 'tv_name'
CLUE_LIST_TIME = PREFIX + 'tv_time'
CLUE_LIST_FLAG = PREFIX + 'tv_flag'
CLUE_LIST_DESC = PREFIX + 'tv_descr'
CLUE_LIST_PIC = PREFIX + 'gl'
CLUE_LIST_PIC_CLASS = 'android.widget.ImageView'
CLUE_LIST_SHARE_BUTTON = PREFIX + 'll_share'
CLUE_LIST_COMMENT_COUNT = PREFIX + 'tv_comment'
CLUE_LIST_COMMENT_BUTTON = PREFIX + 'll_comment'
CLUE_LIST_DIGG_COUNT = PREFIX + 'tv_dianzan'
CLUE_LIST_DIGG_BUTTON = PREFIX + 'll_dianzan'
CLUE_LOCATION = PREFIX + 'tv_location'
SEND_CLUE_BUTTON = PREFIX + 'iv_baoliao'
SEND_CLUE_PIC = PREFIX + 'imageView'
SEND_CLUE_CHECK_MARK = PREFIX + 'checkmark'
SEND_CLUE_PIC_CONFIRM = PREFIX + 'tv_done'


CLUE_SEARCH_EDIT = PREFIX + 'toolbar_et_search'
CLUE_SEARCH_LIST_TYPE = PREFIX + 'tv_name_type'

CLUE_DETAIL_SUBTYPE = PREFIX + 'tv_type'
CLUE_DETAIL_REPLY_TXT = PREFIX + 'tv_reply'
CLUE_DETAIL_DIGG_BUTTON = PREFIX + 'iv_dianzan'
CLUE_DETAIL_DIGG_COUNT = PREFIX + 'tv_digg_count'
CLUE_DETAIL_COMMENT_DIGG_COUNT = PREFIX + 'tv_digg'
CLUE_IMAGE = PREFIX + 'pv_img'
CLUE_IMAGE_DOWNLOAD_BUTTON = PREFIX + 'btn_xiazai'

CLUE_DETAIL_BIG_IMAGE = PREFIX + 'iv_big'
BACK_BUTTON_CLASS = 'android.widget.ImageButton'

#send clue
SEND_CLUE_TYPE_CHOOSE = PREFIX + 'rl_type'
SEND_CLUE_TYPE_TXT = PREFIX + 'textview'
SEND_CLUE_TYPE_CHECK = PREFIX + 'check'
SEND_CLUE_DESC_INPUT = PREFIX + 'et_context'
SEND_CLUE_IMAGE_ADD = PREFIX + 'imageView'
SEND_CLUE_IMAGE_LIST_VIEW = PREFIX + 'gridView'
SEND_CLUE_LOCATION = PREFIX + 'tv_location'
SEND_CLUE_ANONYMOUS = PREFIX + 'cb_push'
SEND_CLUE_CONFIRM_BUTTON = PREFIX + 'tv_reply'
LOCATION_EDIT_TEXT = PREFIX + 'et_location'
LOCATION_EDIT_OK = PREFIX + 'btn_submit'
LOCATION_EDIT_CANCEL = PREFIX + 'btn_cancel'