#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# 添加项目根目录到系统路径，确保能够导入app包
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from flask import current_app
from app import create_app, db
from app.models.hospital import Hospital

def check_hospitals():
    """检查医院表中的数据"""
    
    # 创建应用上下文
    app = create_app()
    with app.app_context():
        # 获取所有医院记录
        hospitals = Hospital.query.all()
        
        print(f"医院总数: {len(hospitals)}")
        
        if hospitals:
            print("\n医院列表:")
            for hospital in hospitals:
                print(f"ID: {hospital.id}, 名称: {hospital.name}, 代码: {hospital.code}, 等级: {hospital.level}, 类型: {hospital.type}")
        else:
            print("\n医院表中没有数据。")
            
if __name__ == "__main__":
    check_hospitals() 