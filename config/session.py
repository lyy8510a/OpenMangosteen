#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by liaoyangyang1 on 2018/9/7 下午10:43.
"""
import redis

class Config(object):
    pass

class ProdConfig(Config):
    pass

class SitConfig(Config):
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False # 如果设置为True，则关闭浏览器session就失效。
    SESSION_USE_SIGNER = False # 是否对发送到浏览器上session的cookie值进行加密
    SESSION_KEY_PREFIX = 'crc'  # 保存到session中的值的前缀
    SESSION_REDIS =  redis.Redis(host='', password='', port='6379')  # 用于连接redis的配置

    SESSION_LIFETIME = 30 #分钟


config = SitConfig()