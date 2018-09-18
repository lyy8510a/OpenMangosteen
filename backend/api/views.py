#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by liaoyangyang1 on 2018/9/10 下午2:37.
"""
import os
import time
from apscheduler.jobstores.base import ConflictingIdError, JobLookupError
from flask import request, Blueprint, current_app as app
from backend.views import csrf
from utils.layout import outputJsonByMessage
from utils.command import doHttpRequest,remotecommand
from backend.views import scheduler
from urllib import parse

api = Blueprint('api', __name__)


# 钩子 在请求执行之前
@api.before_request
def before_request():
    # 请求格式校验拦截
    if not (request.is_json or 'application/json' in request.headers['Accept']):
        return outputJsonByMessage('E', u'带参数请求请使用json格式')




@api.route('/get_scheduler_info', methods=(['GET']))
def get_scheduler_info():
    """
        获取定时任务管理中心运行情况
        ---
        tags:
            - scheduler
        responses:
          200:
            description: 获取定时任务管理中心运行情况
            examples:
              rgb: {
                  "RESPONSE": {
                    "RETURN_CODE": "S",
                    "RETURN_DATA": {
                                  "allowed_hosts": [
                                    "*"
                                  ],
                                  "current_host": "liaoyangyangdemacbook-air.local",
                                  "running": true,
                                  "RETURN_STAMP": 1536824656.796751
                                  }
                     },
                  "RETURN_DESC": ""
                }
    """
    try:
        from collections import OrderedDict
        d = OrderedDict([
            ('current_host', scheduler.host_name),
            ('allowed_hosts', scheduler.allowed_hosts),
            ('running', scheduler.running)
        ])
        return outputJsonByMessage('S', '', d)
    except Exception as e:
        app.logger.error(e)
        return outputJsonByMessage('E', u'接口请求异常', {'status': False})


@api.route('/add_job', methods=(['POST']))
def add_job():
    """Adds a new job."""

    data = request.get_json(force=True)

    try:
        job = scheduler.add_job(**data)
        return outputJsonByMessage('S', '', job)
    except ConflictingIdError:
        return outputJsonByMessage('E', '', dict(error_message='Job %s already exists.' % data.get('id')))
    except Exception as e:
        return outputJsonByMessage('E', '', dict(error_message=str(e)))

    # import random
    # scheduler.add_job(func=test2, args=str(random.randint(1, 10)), trigger='interval', seconds=1, id='test_job_1')
    # return outputJsonByMessage('S')


@api.route('/get_job', methods=(['GET']))
def get_job():
    try:
        all_job = []
        for item in scheduler.get_jobs():
            dict = {}
            dict['id'] = item.id
            dict['name'] = item.name
            dict['next_run_time'] = item.next_run_time.strftime('%Y-%m-%d %H:%M:%S %f')
            dict['interval'] = item.trigger.interval
            dict['start_date'] = item.trigger.start_date.strftime('%Y-%m-%d %H:%M:%S %f')
            dict['args'] = item.args
            all_job.append(dict)
        return outputJsonByMessage('S', '', all_job)
    except Exception as e:
        app.logger.error(e)
        return outputJsonByMessage('E', u'接口请求异常')

@api.route('/test', methods=(['GET']))
def test2():
    return outputJsonByMessage('S')

@csrf.exempt
@api.route('/testconn', methods=(['GET']))
def testconn():
    """
       测试接口连通性
       ---
       tags:
           - utils

       parameters:
         - name: url
           type: string
           required: true
           default: http://127.0.0.1:10103
         - name: params
           type: string
           required: true
           default: "{'username':'','password':''}"
         - name: method
           type: string
           required: true
           enum: ['GET', 'POST']
           default: GET

       responses:
         200:
           description: 获取测试接口连通性结果
           examples:
             rgb: {
                 "RESPONSE": {
                   "RETURN_CODE": "S",
                   "RETURN_DATA": ""
                    },
                 "RETURN_DESC": ""
               }
   """
    url = request.values.get('url')
    params = request.values.get('params')
    method = request.values.get('method')

    ispost = 0 if method == 'GET' else 1
    try:
        result = doHttpRequest(url, params, ispost)
        if (result[0] == 'S'):
            return outputJsonByMessage('S')
        else:
            return outputJsonByMessage('E')
    except Exception as e:
        print(e)
        app.logger.error(e)
        return outputJsonByMessage('E')


@csrf.exempt
@api.route('/testsshconn', methods=(['POST']))
def testsshconn():
    logfile = app.LOG_DIR + '/' + time.strftime('%Y%m%d', time.localtime(
        time.time()))

    if not os.path.exists(logfile):
        os.makedirs(logfile)

    form = parse.parse_qs((request.data).decode('utf8'))


    try:
        host = form.get('host')[0] if not ':'in form.get('host')[0] else form.get('host')[0].split(':')[0]
        port = '22' if not ':'in form.get('host')[0] else form.get('host')[0].split(':')[1]
        username = form.get('username')[0]
        password = form.get('password')[0]
        cmd = 'id'
        result = remotecommand(host,port,username,password,cmd,logfile+"/test.log")
        print(result)
        return outputJsonByMessage('S','',result)
    except Exception as e:
        print(e)
        return outputJsonByMessage('E','',str(e))