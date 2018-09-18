#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by liaoyangyang1 on 2018/8/21 下午2:41.
"""
import os
from flask import Flask, jsonify

from backend import urls
from backend.models import db
from backend.views import login_manager, session, scheduler, swagger, csrf
from backend.assets import assets_env, main_css, main_js

from config.config import config
from config.session import config as redis_config
from config.error import BaseError, OrmError

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'frontend')
STATIC_FOLDER = os.path.join(BASE_DIR, 'frontend', 'static')


def create_app():
    # 初始化项目实例
    app = Flask(__name__, template_folder=TEMPLATE_FOLDER, static_folder=STATIC_FOLDER)
    app.secret_key = app.config['SECRET_KEY']

    # 导入配置项
    app.config.from_object(config)
    app.config.from_object(redis_config)
    # 注册路由
    urls.register(app)
    # 注册数据库
    db.init_app(app)
    # 注册登录组件
    login_manager.init_app(app)
    # 注册session组件
    session.init_app(app)
    # 定时任务
    scheduler.init_app(app)
    scheduler.start()
    # csrf 认证
    csrf.init_app(app)
    # 注册 swagger
    swagger.init_app(app)
    # css,js
    assets_env.init_app(app)
    assets_env.register('main_js', main_js)
    assets_env.register('main_css', main_css)

    # 将变量注册到jinja全局变量
    app.add_template_global(app.config['PROJECTNAME'], 'PROJECTNAME')
    app.add_template_global(app.config['STATIC_URL'], 'STATIC_URL')
    app.add_template_global(app.config['VERSION'], 'VERSION')

    app.BASE_DIR = BASE_DIR
    app.LOG_DIR = BASE_DIR + '/logs'

    # app.add_template_global(app.config['LOGIN_URL'] + '?cburl=' + app.config['BASE_URL'], 'LOGIN_URL')
    # app.add_template_global(app.config['LOGOUT_URL'] + '?cburl=' + app.config['BASE_URL'], 'LOGOUT_URL')

    # 钩子 在请求执行之前
    @app.before_first_request
    def before_first_request():
        import time
        from backend.models.TaskModel import RemotecmdTaskModel, InterfaceTaskModel
        from utils.command import remotecommand, doHttpRequest

        logfile = app.LOG_DIR + '/' + time.strftime('%Y%m%d', time.localtime(
            time.time())) + '/'

        if not os.path.exists(logfile):
            os.makedirs(logfile)

        tasks_remote = [x for x in RemotecmdTaskModel.query.filter(RemotecmdTaskModel.run_status == 1).all()]
        tasks_interface = [x for x in InterfaceTaskModel.query.filter(InterfaceTaskModel.run_status == 1).all()]

        if len(tasks_remote) > 0:
            for task in tasks_remote:
                # 将任务起起来
                scheduler.add_job(id=task.task_remotecmd_name,
                                  name=task.task_remotecmd_name,
                                  func=remotecommand,
                                  args=(task.task_remotecmd_host,
                                        task.task_remotecmd_port,
                                        task.task_remotecmd_username,
                                        task.task_remotecmd_password,
                                        task.task_remotecmd_cmd_value,

                                        "{0}{1}_{2}.log".format(logfile, task.task_remotecmd_name, task.id),
                                        ),
                                  trigger=task.task_remotecmd_trigger_type,

                                  weeks=int(
                                      task.task_remotecmd_trigger_value) if task.task_remotecmd_trigger_arg == 'weeks' else 0,
                                  days=int(
                                      task.task_remotecmd_trigger_value) if task.task_remotecmd_trigger_arg == 'days' else 0,
                                  hours=int(
                                      task.task_remotecmd_trigger_value) if task.task_remotecmd_trigger_arg == 'hours' else 0,
                                  minutes=int(
                                      task.task_remotecmd_trigger_value) if task.task_remotecmd_trigger_arg == 'minutes' else 0,
                                  seconds=int(
                                      task.task_remotecmd_trigger_value) if task.task_remotecmd_trigger_arg == 'seconds' else 0,

                                  )

        if len(tasks_interface) > 0:
            for task in tasks_interface:
                scheduler.add_job(id=task.task_interface_name,
                                  name=task.task_interface_name,
                                  func=doHttpRequest,
                                  args=(task.task_interface_url,
                                        task.task_interface_params,
                                        0 if task.task_interface_method == 'GET' else 1,
                                        0,
                                        "{0}{1}_{2}.log".format(logfile, task.task_interface_name, task.id),
                                        ),
                                  trigger=task.task_interface_trigger_type,

                                  weeks=int(
                                      task.task_interface_trigger_value) if task.task_interface_trigger_arg == 'weeks' else 0,
                                  days=int(
                                      task.task_interface_trigger_value) if task.task_interface_trigger_arg == 'days' else 0,
                                  hours=int(
                                      task.task_interface_trigger_value) if task.task_interface_trigger_arg == 'hours' else 0,
                                  minutes=int(
                                      task.task_interface_trigger_value) if task.task_interface_trigger_arg == 'minutes' else 0,
                                  seconds=int(
                                      task.task_interface_trigger_value) if task.task_interface_trigger_arg == 'seconds' else 0,

                                  )

    @app.errorhandler(BaseError)
    def custom_error_handler(e):
        if e.level in [BaseError.LEVEL_WARN, BaseError.LEVEL_ERROR]:
            if isinstance(e, OrmError):
                app.logger.exception('%s %s' % (e.parent_error, e))
            else:
                app.logger.exception('错误信息: %s %s' % (e.extras, e))
        response = jsonify(e.to_dict())
        response.status_code = e.status_code
        return response

    return app
