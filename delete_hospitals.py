#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# 添加项目根目录到系统路径，确保能够导入app包
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from flask import current_app
from app import create_app, db
from app.models.hospital import Hospital

def delete_all_hospitals():
    """删除所有医院记录"""
    
    # 创建应用上下文
    app = create_app()
    with app.app_context():
        # 获取所有医院记录数量
        hospital_count = Hospital.query.count()
        
        # 删除所有医院记录
        Hospital.query.delete()
        db.session.commit()
        
        print(f"已删除所有 {hospital_count} 家医院")
        
        # 验证删除操作
        remaining = Hospital.query.count()
        print(f"剩余医院数: {remaining}")
            
if __name__ == "__main__":
    delete_all_hospitals() 