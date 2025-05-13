#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# 添加项目根目录到系统路径，确保能够导入app包
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from flask import current_app
from app import create_app, db
from app.models.hospital import Hospital

def check_dongguan_hospitals():
    """检查东莞医院数据"""
    
    # 创建应用上下文
    app = create_app()
    with app.app_context():
        # 获取所有医院记录
        hospitals = Hospital.query.order_by(Hospital.id).all()
        
        print(f"医院总数: {len(hospitals)}")
        
        if hospitals:
            print("\n医院列表:")
            for hospital in hospitals:
                print(f"ID: {hospital.id}, 名称: {hospital.name}, 类别: {hospital.type}, 级别: {hospital.level}")
        else:
            print("\n医院表中没有数据。")
            
if __name__ == "__main__":
    check_dongguan_hospitals() 