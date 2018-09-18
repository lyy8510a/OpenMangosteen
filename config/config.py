#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by liaoyangyang1 on 2017/11/8.
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config(object):
    """Base config class."""
    # 版本
    VERSION = 'beta 0.1'
    # 项目名称
    PROJECTNAME = '任务中心'
    # 端口
    PORT = 10103
    ADMIN_USER = 'admin'
    ADMIN_EMAIL = '51263921@qq.com'
    SECRET_KEY = os.urandom(24)

    SCHEDULER_API_ENABLED = True
    MAX_INSTANCES = 3
    # SCHEDULER_ALLOWED_HOSTS = '127.0.0.1'

    TOKEN_API = ['http://127.0.0.1:10102/api/get_token', 'http://127.0.0.1:10102/api/check_token']


class ProdConfig(Config):
    """Production config class."""

    # 是否开启调试
    DEBUG = False

    # 主机ip地址
    HOST = '0.0.0.0'


class SitConfig(Config):
    """Development config class."""
    # Open the DEBUG
    # 是否开启调试
    DEBUG = True
    # 主机ip地址
    HOST = '127.0.0.1'

    STATIC_URL = "http://{0}:{1}/static".format(HOST, Config.PORT)
    BASE_URL = "http://{0}:{1}".format(HOST, Config.PORT)

    #### Flask-Assets's config
    # Can not compress the CSS/JS on Dev environment.
    ASSETS_DEBUG = True

    # # 数据库配置
    MYSQL_HOST = '127.0.0.1'  # 此处修改为您的mysql的主机IP
    MYSQL_PORT = 3306  # 此处修改为您的mysql的主机端口
    MYSQL_USER = 'root'  # 此处修改为您的mysql的用户名称
    MYSQL_PASS = '123456'  # 此处修改为您的mysql的用户密码
    MYSQL_DB = 'task'  # 此处修改为您的mysql的数据库名称

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8".format(MYSQL_USER, MYSQL_PASS,
                                                                                        MYSQL_HOST
                                                                                        , MYSQL_PORT, MYSQL_DB)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LOGIN_URL = 'http://127.0.0.1:10102/account/login'
    LOGOUT_URL = 'http://127.0.0.1:10102/account/logout'


class DevConfig(Config):
    pass


# Default using Config settings, you can write if/else for different env
config = SitConfig()
