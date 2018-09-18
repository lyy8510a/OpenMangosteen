#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by liaoyangyang1 on 2018/8/22 上午9:40.
"""
from flask import Blueprint,request,render_template,session,flash
from flask import redirect,url_for,abort,g
from backend.models.UserModel import User,Role
from backend.models import db
from flask_login import login_user,login_required,logout_user,current_user
from functools import wraps
from backend.models.UserModel import Permission
from utils.layout import layout
from datetime import timedelta

#账户的蓝图  访问http://host:port/account 这个链接的子链接，都会跳到这里
account = Blueprint('account', __name__)  #第二课增加内容


def permission_required(permission): #第五课新增
    """Restrict a view to users with the given permission."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# 要求管理员权限
def admin_required(f): #第五课新增
    return permission_required(Permission.ADMINISTER)(f)

# 访问http://host:port/account/register 这个链接，就会跳到这里
@account.route('/register',methods=(["GET","POST"]))  #第二课增加内容
#上面的链接，绑定的就是这个方法，我们给浏览器或者接口请求 一个json格式的返回
def register():  #第二课增加内容
    from backend.account.logic import register_logic

    if request.method == 'POST':
        result = register_logic(request.form)
        if result['RETURN_CODE']  == 'E':
            flash(result['RETURN_DESC'], 'danger')
        else:
            flash(u'注册成功', 'success')
            return redirect(url_for(request.args.get('next') or 'account.login'))

    return render_template('/account/register.html')

@account.route('/login',methods=(["GET","POST"]))
def login(): #第三课内容
    Role.insert_roles()
    if request.method == "POST":
        from backend.account.logic import login_logic
        result = login_logic(request.form)
        if result['RETURN_CODE'] == 'S':
            flash(result['RETURN_DESC'], 'success')

            if '?'in str(request.referrer) and  'cburl' in str(request.referrer).split('?')[1]:
                cburl = str(request.referrer).split('?')[1].split('=')[1]
                return redirect(cburl,302)
            return redirect( url_for('admin.index'))
        else:
            flash(result['RETURN_DESC'], 'danger')

    return render_template('/account/login.html')

@account.route('/logout')
@login_required
def logout():
    cburl = request.values.get('cburl')
    logout_user()
    session.clear()
    flash('You have been logged out.', 'info')
    if cburl:
        return redirect(cburl,302)
    return redirect(url_for('account.login'))


@account.route('/users')
@login_required
def user_list(): #第五课新增
    user_list = User.query.outerjoin(Role, User.role_id == Role.id).all()
    return layout('/account/users.html',users=user_list)

    
@account.route('/edituser',methods=(["GET","POST"]))
@login_required
@admin_required
def user_edit(): #第五课新增
    if request.method == 'POST':
        try:
            form = request.form
            use_info = User.query.filter(User.id == form['id']).first()
            use_info.email = form['email']
            use_info.role_id = form['role_id']
            db.session.commit()
            flash('修改用户信息成功！', 'success')
        except Exception as e:
            print(e)
            flash('修改用户信息失败！', 'danger')
        return redirect(url_for(request.args.get('next') or 'account.user_list'))

    id = request.values.get('id')
    user_info = User.query.filter_by(id=id).first()
    return layout('/account/edituser.html', user_info=user_info)

@account.route('/deluser')
@login_required
@admin_required
def user_del(): #第五课新增
    try:
        id = request.values.get('id')
        user = User.query.filter(User.id == id).first()
        db.session.delete(user)
        db.session.commit()
        flash('删除用户成功！', 'success')
    except Exception as e:
        print(e)
        flash('删除用户失败！', 'danger')

    return redirect(url_for(request.args.get('next') or 'account.user_list'))


