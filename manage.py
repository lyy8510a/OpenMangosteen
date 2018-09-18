#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by liaoyangyang1 on 2018/8/21 下午3:40.
"""

from flask_script import Manager, Server
from backend import create_app, db  # 第二课新增
from flask_migrate import Migrate  # 第二课新增
from backend.models.UserModel import Role
app = create_app()
migrate = Migrate(app, db)  # 第二课新增

app.debug = app.config["DEBUG"]
# 获取根目录config.py的配置项
host = app.config["HOST"]
port = app.config["PORT"]

# Init manager object via app object
manager = Manager(app)

# Create a new commands: server
# This command will be run the Flask development_env server
manager.add_command("runserver", Server(host=host, port=port, threaded=True))


@manager.shell
def make_shell_context():
    """Create a python CLI.

    return: Default import object
    type: `Dict`
    """
    # 确保有导入 Flask app object，否则启动的 CLI 上下文中仍然没有 app 对象
    return dict(app=app, db=db)  # 第二课新增


# 创建数据库脚本
@manager.command
def create_db():  # 第二课新增
    """
    Recreates a local database. You probably should not use this on
    production.
    """
    db.create_all()
    db.session.commit()
    Role.insert_roles()


@manager.command
def recreate_db():  # 第二课新增
    """
    Recreates a local database. You probably should not use this on
    production.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()
    Role.insert_roles()

if __name__ == '__main__':
    manager.run()
