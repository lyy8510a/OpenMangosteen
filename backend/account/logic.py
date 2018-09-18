#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by liaoyangyang1 on 2018/9/8 下午12:14.
"""

from datetime import timedelta

from backend.models import db
from backend.models.UserModel import User
# from backend.views import session

from flask import current_app as app,session
from flask_login import login_user,login_required,logout_user,current_user



# 注册逻辑
def register_logic(form):
    def to_register(username,password,email):
        try:
            user = User(username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            return {'RETURN_CODE':'S','RETURN_DESC':u'创建用户成功','RETURN_DATA':{'username':username,'email':email,'password':password}}
        except Exception as e:
            app.logger.error(e)
            return {'RETURN_CODE':'E','RETURN_DESC':u'创建用户失败,用户名已存在','RETURN_DATA':{'username':username,'email':email,'password':password}}

    if isinstance(form['username'],list):
        if(len(form['username'])>0):
            result = []
            for i in range(len(form['username'])):
                username = form['username'][i]
                email = form['email'][i]
                password = form['password'][i]
                res = to_register(username,password,email)
                result.append(res)
        else:
            result = {'RETURN_CODE':'E','RETURN_DESC':u'参数异常','RETURN_DATA':''}
    else:
        username = form['username']
        email = form['email']
        password = form['password']
        result = to_register(username, password, email)

    return result

# 登录逻辑
def login_logic(form):

    username = form['username'][0] if isinstance(form['username'],list) else form['username']
    password = form['password'][0] if isinstance(form['password'],list) else form['password']

    try:
        user = User.query.filter_by(username=username).first()  # 查出用户信息
    except Exception as e:
        app.logger.error(e)
        return {
            'RETURN_CODE':'E',
            'RETURN_DESC':u'登录失败,此用户不存在',
            'RETURN_DATA':{'username':username,'password':password}
        }



    if not user.verify_password(password):
        return {
            'RETURN_CODE': 'E',
            'RETURN_DESC': u'密码不正确',
            'RETURN_DATA': {'username': username, 'password': password}
        }

    if not user.password_hash:
        return {
            'RETURN_CODE': 'E',
            'RETURN_DESC': u'密码源数据异常，请联系管理员',
            'RETURN_DATA': {'username': username, 'password': password}
        }


    login_user(user, True)  # 登录操作
    app.permanent_session_lifetime = timedelta(minutes=app.config['SESSION_LIFETIME'])  # session失效时间





    userdata = {
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'uc_role_name': user.role.name,
        'uc_role_id': user.role_id,
        'is_authenticated':True
    }
    session['userdata']=userdata



    return {'RETURN_CODE':'S','RETURN_DESC':u'登录成功','RETURN_DATA':{'userdata':userdata}}

