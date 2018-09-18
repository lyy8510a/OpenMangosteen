#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by liaoyangyang1 on 2018/8/21 下午3:50.
"""

from backend.admin.views import admin
from backend.account.views import account
from backend.api.views import api
from werkzeug.routing import BaseConverter
from backend.task.views import task


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


# 蓝图注册
def register(app):
    app.url_map.converters['regex'] = RegexConverter
    app.register_blueprint(account, url_prefix='/account', strict_slashes=False)
    app.register_blueprint(admin, url_prefix='/admin', strict_slashes=False)
    app.register_blueprint(admin, url_prefix='/', strict_slashes=False)
    app.register_blueprint(api, url_prefix='/api', strict_slashes=False)
    app.register_blueprint(task, url_prefix='/task', strict_slashes=False)
