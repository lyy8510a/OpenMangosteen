#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by liaoyangyang1 on 2018/9/9 下午3:16.
"""
import os
import logging
from config.config import config


def init_app(app):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logpath = '{0}/logs'.format(BASE_DIR)
    if not os.path.exists(logpath):
        os.mkdir(logpath)

    handler = logging.FileHandler(logpath + "/{0}.log".format(config.MYSQL_DB), encoding='UTF-8')
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)


