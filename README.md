# OpenMangosteen
Devops定时调用http接口，定时执行SSH命令的WEB定时任务工具。本系统强依赖Flask-APScheduler的功能，只是拓展了web页面部分。使用Python3进行开发。

## 快速开始
### 修改配置
修改config文件夹中config.py的MYSQL数据库连接配置。
酌情修改端口和HOST

### 启动项目
```Python
pip install -r requirement.txt
python manage.py create_db
python mannage.py runserver
```
## 详细操作步骤及截图
### 添加调用HTTP接口的定时任务
  ![](https://github.com/lyy8510a/OpenMangosteen/blob/master/screenshot/interface_task_add_1.png)
  ![](https://github.com/lyy8510a/OpenMangosteen/blob/master/screenshot/interface_task_add_2.png)
### 添加定时执行远程SSH COMMAND命令
  ![](https://github.com/lyy8510a/OpenMangosteen/blob/master/screenshot/remotecmd_task_add_1.png)
### 存量定时任务管理
  ![](https://github.com/lyy8510a/OpenMangosteen/blob/master/screenshot/index_1.png)
  ![](https://github.com/lyy8510a/OpenMangosteen/blob/master/screenshot/index_2.png)
  ![](https://github.com/lyy8510a/OpenMangosteen/blob/master/screenshot/index_3.png)
  
## 主要依赖的模块
Flask==1.0.2 <br>
Flask-APScheduler==1.10.1 <br>
flasgger==0.9.1 <br>
Flask-Login==0.4.1 <br>
Flask-Assets==0.12 <br>
Flask-Migrate==2.2.1 <br>
Flask-Script==2.0.6 <br>
Flask-Session==0.3.1 <br>
Flask-SQLAlchemy==2.3.2 <br>
