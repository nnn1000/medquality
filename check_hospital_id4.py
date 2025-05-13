#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# 添加项目根目录到系统路径，确保能够导入app包
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from flask import current_app
from app import create_app, db
from app.models.hospital import Hospital

def check_hospital_id4():
    """检查ID为4的医院"""
    
    # 创建应用上下文
    app = create_app()
    with app.app_context():
        # 查询ID为4的医院
        hospital = Hospital.query.get(4)
        
        if hospital:
            print(f"找到ID为4的医院:")
            print(f"ID: {hospital.id}, 名称: {hospital.name}, 代码: {hospital.code}, 等级: {hospital.level}, 类型: {hospital.type}")
        else:
            print("ID为4的医院不存在。")
            
if __name__ == "__main__":
    check_hospital_id4() 
 