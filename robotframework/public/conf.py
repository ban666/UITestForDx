# -*- coding: utf-8 -*-
__author__ = 'liaoben'

#2:普通文字新闻
#3:组图
#4:专栏
#5:专题
#13:视频
#17:直播视频
#22:音频
STRUCT_PLUG = {
    'ResInfo':['infoid','cateid','title','pics','desc','rechid','reltime','repcount','pageview','model','flag','style','duration','sourceurl','shareurl','targeturl','turnoff'],
    'ResAudio':['id','title','pics','bg','repcount','duration','sourceurl','shareurl','desc','turnoff'],
    'ResVideo':['id','title','pics','repcount','duration','sourceurl','shareurl','desc','turnoff'],
    'ResArticle':['infoid','title','pics','desc','repcount','pageview','shareurl','turnoff','tmpl','tmplver','data'],
    'ResSpecial':['spid','title','desc','pics','columns','infos'],
    'ResPhotos':['id','title','desc','pics','repcount','pageview','shareurl','turnoff'],
    'ResClue':['cid','uname','uicon','loc','reltime','digg','share','reply','content','thumb','subcate','state','remark','extrapoint','replytxt'],
    'ResClueCate':['subcate','name']
}

MODEL_STRUCT_PLUG = {
    '2':'ResArticle',
    '3':'ResPhotos',
    '4':'ResSpecial',
    '5':'ResInfo',
    '13':'ResVideo',
    '17':'ResArticle',
    '25':'ResAudio'
}

STRUCT_DX = {
    'ResInformation':['id','title','pics','desc','colid','reltime','repcount','model','flag','style','args','turnoff'],
    'Special':['id','title','summary','pics','columns','list'],
    'ResArticle':['id','title','pics','desc','repcount','url','turnoff'],
    'ResVideo':["id", "title","pics","repcount","duration","sourceurl","shareurl","desc","turnoff"],
    'ResPhotos':["id","pics","repcount","url","title","desc","shareurl","turnoff"]
}

MODEL_STRUCT_DX = {
    '2':'ResArticle',
    '3':'ResPhotos',
    '4':'Special',
    '5':'ResInformation',
    '13':'ResVideo',
    '17':'ResArticle',
    '25':'ResAudio'
}

type_struct = {
    'dx': (MODEL_STRUCT_DX,STRUCT_DX),
    'dx_plug':(MODEL_STRUCT_PLUG,STRUCT_PLUG)
}

#QQ login info
QQ_LOGIN_INFO = {
    'platform':2,
    'uid':'3FBE43EF635AFEDEE2BE8551977FE519',
    'screen_name':'qq_test',
    'profile_image_url':'http://q.qlogo.cn/qqapp/1101963208/3FBE43EF635AFEDEE2BE8551977FE519/100'
}

#Wechat login info
WECHAT_LOGIN_INFO = {
    'platform':3,
    'uid':'ozX3swyHfP0KBdTisUzdIw7RbUkY',
    'screen_name':'wechat_test',
    'profile_image_url':'http://fake_icon'
}

#Weibo login info
WEIBO_LOGIN_INFO = {
    'platform':1,
    'uid':'6051955234',
    'screen_name':'动次打次一笑奈何',
    'profile_image_url':'http://tva3.sinaimg.cn/default/images/default_avatar_male_180.gif'
}