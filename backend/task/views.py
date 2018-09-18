#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by liaoyangyang1 on 2018/9/12 下午5:11.
"""
import os
import time

from flask import Blueprint, request, current_app as app, redirect, url_for, flash
from flask_login import current_user

from backend.models import db
from backend.models.TaskModel import InterfaceTaskModel, RemotecmdTaskModel
from backend.views import scheduler
from utils.command import doHttpRequest, tail, remotecommand
from utils.layout import layout, outputJsonByMessage

task = Blueprint('task', __name__)


@task.route('interface', methods=(['GET', 'POST']))
def task_interface():
    if request.method == "POST":
        form = request.form
        try:
            if form:
                task = InterfaceTaskModel(
                    task_interface_name=form['task_interface_name'],
                    task_interface_method=form['task_interface_method'],
                    task_interface_url=form['task_interface_url'],
                    task_interface_params=form['task_interface_params'],
                    task_interface_trigger_type=form['task_interface_trigger_type'],
                    task_interface_trigger_arg=form['task_interface_trigger_arg'],
                    task_interface_trigger_value=form['task_interface_trigger_value'],
                    addtime=time.time(),
                    addwho=current_user.username,
                )
                db.session.add(task)
                db.session.commit()
                flash(u'添加成功', 'success')
                return redirect(url_for('admin.index'))
            else:
                flash(u'参数为空', 'error')
        except Exception as e:
            app.logger.error(e)
    return layout('task/interface.html')


# 删除接口调用任务
@task.route('del_task', methods=(['POST']))
def del_task():
    task_id = request.values.get('task_id')
    task_type = request.values.get('task_type')
    try:
        if task_type == 'interface':
            task = InterfaceTaskModel.query.filter(InterfaceTaskModel.id == '{0}'.format(task_id)).first()
        else:
            task = RemotecmdTaskModel.query.filter(RemotecmdTaskModel.id == '{0}'.format(task_id)).first()

        db.session.delete(task)
        db.session.commit()
        flash(u'删除成功', 'success')
        return outputJsonByMessage('S')
    except Exception as e:
        flash(e, 'error')
        app.logger.error(e)
        return outputJsonByMessage('E')


# 启动接口调用任务
@task.route('start_task', methods=(['POST']))
def start_task():
    logfile = app.LOG_DIR + '/' + time.strftime('%Y%m%d', time.localtime(
        time.time())) + '/'

    if not os.path.exists(logfile):
        os.makedirs(logfile)

    try:
        task_id = request.values.get('task_id')
        task_type = request.values.get('task_type')

        if task_type == 'interface':
            task = InterfaceTaskModel.query.filter(InterfaceTaskModel.id == int(task_id)).first()

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
            task.run_status = 1
            db.session.commit()
        else:
            task = RemotecmdTaskModel.query.filter(RemotecmdTaskModel.id == int(task_id)).first()

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
            task.run_status = 1
            db.session.commit()

        return outputJsonByMessage('S')
    except Exception as e:
        app.logger.error(e)
        return outputJsonByMessage('E')


# 停止接口调用任务
@task.route('stop_task', methods=(['POST']))
def stop_task():
    task_id = request.values.get('task_id')
    task_type = request.values.get('task_type')
    if task_type == 'interface':
        task = InterfaceTaskModel.query.filter(InterfaceTaskModel.id == int(task_id)).first()

    else:
        task = RemotecmdTaskModel.query.filter(RemotecmdTaskModel.id == int(task_id)).first()
    task.run_status = 0
    db.session.commit()
    try:
        if task_type == 'interface':
            scheduler.remove_job(id=task.task_interface_name)
        else:
            scheduler.remove_job(id=task.task_remotecmd_name)
        return outputJsonByMessage('S', '')
    except Exception as e:
        app.logger.error(e)
        return outputJsonByMessage('E', '', str(e))


# 获取接口调用任务日志
@task.route('get_task_log', methods=(['GET']))
def get_task_log():
    logfile = app.LOG_DIR + '/' + time.strftime('%Y%m%d', time.localtime(
        time.time())) + '/'
    try:
        task_id = request.values.get('task_id')
        task_type = request.values.get('task_type')
        if task_type == 'interface':
            task = InterfaceTaskModel.query.filter(InterfaceTaskModel.id == int(task_id)).first()
            logpath = "{0}{1}_{2}.log".format(logfile, task.task_interface_name, task.id)

        else:
            task = RemotecmdTaskModel.query.filter(RemotecmdTaskModel.id == int(task_id)).first()
            logpath = "{0}{1}_{2}.log".format(logfile, task.task_remotecmd_name, task.id)

        return_data = tail(logpath)
        return outputJsonByMessage('S', '', str(return_data))
    except Exception as e:
        app.logger.error(e)
        return outputJsonByMessage('E', '', str(e))


@task.route('remotecmd', methods=(['GET', 'POST']))
def remotecmd():
    if request.method == "POST":
        form = request.form
        try:
            if form:
                task_remotecmd_host = form['task_remotecmd_hostandport'] if not ':' in form[
                    'task_remotecmd_hostandport'] else form['task_remotecmd_hostandport'].split(':')[0]
                task_remotecmd_port = '22' if not ':' in form['task_remotecmd_hostandport'] else \
                    form['task_remotecmd_hostandport'].split(':')[1]
                task = RemotecmdTaskModel(
                    task_remotecmd_name=form['task_remotecmd_name'],
                    task_remotecmd_host=task_remotecmd_host,
                    task_remotecmd_port=task_remotecmd_port,
                    task_remotecmd_username=form['task_remotecmd_username'],
                    task_remotecmd_password=form['task_remotecmd_password'],
                    task_remotecmd_trigger_type=form['task_remotecmd_trigger_type'],
                    task_remotecmd_trigger_arg=form['task_remotecmd_trigger_arg'],
                    task_remotecmd_trigger_value=form['task_remotecmd_trigger_value'],
                    task_remotecmd_cmd_type=form['task_remotecmd_cmd_type'],
                    task_remotecmd_cmd_value=form['task_remotecmd_cmd_value'],

                    addtime=time.time(),
                    addwho=current_user.username,
                )
                db.session.add(task)
                db.session.commit()
                flash(u'添加成功', 'success')
                return redirect(url_for('admin.index'))
            else:
                flash(u'参数为空', 'error')
        except Exception as e:
            app.logger.error(e)

    return layout('task/remotecmd.html')
