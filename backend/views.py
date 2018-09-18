#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by liaoyangyang1 on 2018/8/21 下午3:51.
"""
from flask_login import LoginManager
from flask_session import Session
from flask_apscheduler import APScheduler
from flask_wtf import CSRFProtect
from datetime import timedelta
from flasgger import Swagger

# Set up Flask-Login
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'account.login'
login_manager.remember_cookie_duration = timedelta(minutes=30)  # cookie失效时间

session = Session()

scheduler = APScheduler()

swagger = Swagger()

csrf = CSRFProtect()
