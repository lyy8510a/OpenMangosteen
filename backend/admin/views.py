#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by liaoyangyang1 on 2018/8/23 上午11:09.
"""
from flask import Blueprint, session, request, redirect, current_app as app
from utils.layout import layout
from backend.views import scheduler
from backend.models.TaskModel import InterfaceTaskModel,RemotecmdTaskModel

admin = Blueprint('admin', __name__)


@admin.before_request
def before_request():
    if not 'userdata' in (session):
        return redirect(app.config['LOGIN_URL'] + '?cburl=' + request.url, 302)


@admin.route('/')
def index():
    running_jobs = []
    all_interface_tasks = [x.__dict__ for x in InterfaceTaskModel.query.all()]
    all_remotecmd_tasks = [x.__dict__ for x in RemotecmdTaskModel.query.all()]
    for item in scheduler.get_jobs():
        dict = {}
        dict['id'] = item.id
        dict['name'] = item.name
        dict['next_run_time'] = item.next_run_time.strftime('%Y-%m-%d %H:%M:%S %f')
        dict['interval'] = item.trigger.interval.seconds
        dict['start_date'] = item.trigger.start_date.strftime('%Y-%m-%d %H:%M:%S %f')
        dict['args'] = item.args
        running_jobs.append(dict)



    return layout('/base/index.html', running_jobs=running_jobs, all_interface_tasks=all_interface_tasks,all_remotecmd_tasks=all_remotecmd_tasks)
