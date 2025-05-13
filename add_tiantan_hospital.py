#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# 添加项目根目录到系统路径，确保能够导入app包
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from flask import current_app
from app import create_app, db
from app.models.hospital import Hospital

def add_tiantan_hospital():
    """添加天坛医院数据"""
    
    # 创建应用上下文
    app = create_app()
    with app.app_context():
        # 天坛医院数据
        hospital_data = {
            'name': '首都医科大学附属北京天坛医院',
            'code': 'BTTH',
            'address': '北京市丰台区南四环西路119号',
            'level': '三级甲等',
            'type': '综合医院',
            'contact_person': '管理员',
            'contact_phone': '010-xxxxxxxx'
        }
            
        # 检查医院是否已存在
        existing = Hospital.query.filter_by(name=hospital_data['name']).first()
        if not existing:
            hospital = Hospital(**hospital_data)
            db.session.add(hospital)
            db.session.commit()
            print(f"成功添加医院: {hospital_data['name']}")
        else:
            print(f"医院 '{hospital_data['name']}' 已存在，ID: {existing.id}")
        
        # 显示当前所有医院
        all_hospitals = Hospital.query.all()
        print(f"\n当前医院总数: {len(all_hospitals)}")
        if all_hospitals:
            print("\n医院列表:")
            for hospital in all_hospitals:
                print(f"ID: {hospital.id}, 名称: {hospital.name}, 代码: {hospital.code}, 等级: {hospital.level}, 类型: {hospital.type}")
        
if __name__ == "__main__":
    add_tiantan_hospital() 