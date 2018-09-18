#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by liaoyangyang1 on 2018/9/13 下午3:25.
"""
from backend.models import db


class InterfaceTaskModel(db.Model):
    __tablename__ = 'interfacetask'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # id
    task_interface_name = db.Column(db.VARCHAR(200), nullable=True)  # 事件id
    task_interface_method = db.Column(db.VARCHAR(20), nullable=False)
    task_interface_url = db.Column(db.VARCHAR(200), nullable=False)
    task_interface_params = db.Column(db.VARCHAR(200), nullable=False)
    task_interface_trigger_type = db.Column(db.VARCHAR(50), nullable=True)
    task_interface_trigger_arg = db.Column(db.VARCHAR(50), nullable=False)
    task_interface_trigger_value = db.Column(db.VARCHAR(50), nullable=False)

    param_1 = db.Column(db.VARCHAR(100), nullable=True)
    param_2 = db.Column(db.VARCHAR(100), nullable=True)
    param_3 = db.Column(db.VARCHAR(100), nullable=True)
    param_4 = db.Column(db.VARCHAR(100), nullable=True)

    addwho = db.Column(db.VARCHAR(50), nullable=False)
    addtime = db.Column(db.VARCHAR(50), nullable=False)
    is_delete = db.Column(db.Integer, default=0)
    run_status = db.Column(db.Integer, default=0)  # 0:停止 1:执行中 2:暂停

class RemotecmdTaskModel(db.Model):
    __tablename__ = 'remotecmdtask'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # id
    task_remotecmd_name = db.Column(db.VARCHAR(200), nullable=True)  # 事件id
    task_remotecmd_host = db.Column(db.VARCHAR(50), nullable=False)
    task_remotecmd_port = db.Column(db.VARCHAR(200), nullable=False)
    task_remotecmd_username = db.Column(db.VARCHAR(200), nullable=False)
    task_remotecmd_password = db.Column(db.VARCHAR(50), nullable=True)
    task_remotecmd_cmd_type = db.Column(db.VARCHAR(50), nullable=False)
    task_remotecmd_cmd_value = db.Column(db.VARCHAR(50), nullable=False)

    task_remotecmd_trigger_type = db.Column(db.VARCHAR(50), nullable=True)
    task_remotecmd_trigger_arg = db.Column(db.VARCHAR(50), nullable=False)
    task_remotecmd_trigger_value = db.Column(db.VARCHAR(50), nullable=False)

    param_1 = db.Column(db.VARCHAR(100), nullable=True)
    param_2 = db.Column(db.VARCHAR(100), nullable=True)
    param_3 = db.Column(db.VARCHAR(100), nullable=True)
    param_4 = db.Column(db.VARCHAR(100), nullable=True)

    addwho = db.Column(db.VARCHAR(50), nullable=False)
    addtime = db.Column(db.VARCHAR(50), nullable=False)
    is_delete = db.Column(db.Integer, default=0)
    run_status = db.Column(db.Integer, default=0)  # 0:停止 1:执行中 2:暂停