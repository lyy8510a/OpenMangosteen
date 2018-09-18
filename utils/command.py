#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by liaoyangyang1 on 2018/9/12 下午9:37.
"""
import json
import datetime
import paramiko
import requests


def saveRecode(logfile, level, msg):
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg = msg.replace('\r\n','').replace('\r','').replace('\n','')
    if not ( '\r' in msg and '\r\n' in msg and '\n' in msg):
        msg = msg + '\r\n'

    with open(logfile, 'a+') as f:
        f.write("[{0}]-{1}-{2}".format(nowTime, level, str(msg)))


# 调用http请求
def doHttpRequest(url, params=None, isPost=0, useProxy=0, logfile='/tmp/task.log'):
    if params and not isinstance(params, dict):
        params = eval(params)
    else:
        params = {'1':1}

    req = requests.session()
    req.headers = ({
        'Accept-Encoding': ', '.join(('gzip', 'deflate')),
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
    })
    if useProxy == 1:
        req.proxies = {'http': '127.0.0.1:10002'}

    try:
        if isPost == 1:
            result = req.post(url, json=json.dumps(params)) if params and isinstance(params, dict) else req.post(url)
        else:
            result = req.get(url, data=json.dumps(params)) if params and isinstance(params, dict) else req.get(url)

        if (result.status_code == 200):
            # RETURN_CODE = json.loads(result.text)['RESPONSE']['RETURN_CODE']
            # RETURN_DATA = json.loads(result.text)['RESPONSE']['RETURN_DATA']
            # RETURN_DESC = json.loads(result.text)['RETURN_DESC']
            saveRecode(logfile, 'INFO', result.text)
            return ('S',result.text)
        else:
            saveRecode(logfile, 'INFO', result.text)
            return ('E', u'接口请求异常,请检查防火墙')
    except Exception as e:
        saveRecode(logfile, 'ERROR', str(e))
        return ('E', u'接口请求异常,请检查防火墙')


# 读文件最后一行
def tail(filename):
    try:
        with open(filename, 'rb+') as f:  # 打开文件
            lines = f.readlines()
        return lines[-1]
    except Exception as e:
        print(e)


# 远程执行命令
def remotecommand(host, port, username, password, cmd, logfile='/tmp/task.log'):
    try:
        ssh = paramiko.SSHClient()
        # ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=str(host), port=int(port), username=str(username), password=str(password), timeout=1)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        saveRecode(logfile, 'INFO', "".join(stdout.readlines()).replace('\r', '').replace('\r\n', ''))
        return stdout.readlines()
    except Exception as e:
        saveRecode(logfile, 'ERROR', e)


if __name__ == '__main__':
    result = remotecommand('10.0.53.129', 22, 'root', 'Hrt@2017', 'id',
                           '/Users/liaoyangyang/crc/codes-dc/python/Mangosteen/logs/20180917/test_3.log')
    print(result)
