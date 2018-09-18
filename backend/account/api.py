#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by liaoyangyang1 on 2018/9/8 下午12:13.
"""
from urllib import parse
from flask import Blueprint,request,current_app as app
from utils.layout import outputJsonByMessage
from backend.models.UserModel import User
import random

api = Blueprint('api', __name__)

requied = {
    'api.register':['email','username','password'],
    'api.get_token':['username','password']
}


# 钩子 在请求执行之前
@api.before_request
def before_request():

    # 请求格式校验拦截
    if not request.is_json:
        return outputJsonByMessage('E', u'带参数请求请使用json格式')
    # 缺少必填参数拦截
    try:
        if request.endpoint in requied:
            if request.method == "POST":
                missparam_list = [x for x in requied[request.endpoint] if x.encode('utf8') not in list(parse.parse_qs(request.data).keys())]
            else:
                missparam_list = [x for x in requied[request.endpoint] if x not in request.json.keys()]

            if len(missparam_list) > 0:
                return outputJsonByMessage('E', u"缺少以下参数:{0}".format(",".join(missparam_list)))
    except Exception as e:
        app.logger.error(e)
        return outputJsonByMessage('E', e)

# 注册接口
@api.route('/register',methods=(['GET','POST']))
def register():
    from backend.account.logic import register_logic
    form = parse.parse_qs((request.data).decode('utf8'))
    return outputJsonByMessage('S',u'注册成功') if register_logic(form) else outputnJsoByMessage('E',u'注册失败')

# 登录接口
@api.route('/login',methods=(['GET','POST']))
def login():
    from backend.account.logic import login_logic
    form = parse.parse_qs((request.data).decode('utf8'))
    return outputJsonByMessage('S', u'登录成功') if login_logic(form) else outputnJsoByMessage('E',u'登录失败')

