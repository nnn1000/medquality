from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.user import User
from app.forms import LoginForm, RegisterForm
from datetime import datetime

# 创建认证蓝图
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # 如果用户已登录，重定向到首页
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # 查找用户
        user = User.query.filter_by(username=form.username.data).first()
        
        # 验证用户名和密码
        if user is None or not user.check_password(form.password.data):
            flash('用户名或密码不正确', 'danger')
            return redirect(url_for('auth.login'))
        
        # 登录用户
        login_user(user, remember=form.remember_me.data)
        
        # 更新最后登录时间
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # 重定向到受保护页面或首页
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('dashboard.index')
        return redirect(next_page)
    
    return render_template('auth/login.html', title='登录', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已成功退出登录', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # 只有管理员可以注册新用户
    if current_user.is_authenticated and not current_user.is_admin:
        flash('您没有权限注册新用户', 'danger')
        return redirect(url_for('dashboard.index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        # 创建新用户
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            hospital_id=form.hospital_id.data if form.hospital_id.data != 0 else None
        )
        db.session.add(user)
        db.session.commit()
        
        flash('用户注册成功！', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='注册', form=form) 