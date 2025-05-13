#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import create_app, db
from app.models.user import User
from werkzeug.security import generate_password_hash

# 创建应用上下文
app = create_app()
app.app_context().push()

def create_admin_user():
    """创建管理员用户"""
    # 检查管理员是否已存在
    if User.query.filter_by(username='admin').first() is None:
        # 创建管理员用户
        admin = User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('admin123'),
            is_admin=True
        )
        
        # 添加到数据库
        db.session.add(admin)
        db.session.commit()
        
        print('管理员用户创建成功！')
        print('用户名: admin')
        print('密码: admin123')
    else:
        print('管理员用户已存在')

if __name__ == '__main__':
    create_admin_user() 