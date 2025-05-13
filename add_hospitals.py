#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# 添加项目根目录到系统路径，确保能够导入app包
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from flask import current_app
from app import create_app, db
from app.models.hospital import Hospital

def add_hospitals():
    """添加医院数据到数据库"""
    
    # 创建应用上下文
    app = create_app()
    with app.app_context():
        # 准备添加的医院数据
        hospitals_data = [
            {
                'name': '北京协和医院',
                'code': 'PUTH',
                'address': '北京市东城区帅府园1号',
                'level': '三级甲等',
                'type': '综合医院',
                'contact_person': '管理员',
                'contact_phone': '010-xxxxxxxx'
            },
            {
                'name': '北京大学第一医院',
                'code': 'PKUFH',
                'address': '北京市西城区西什库大街8号',
                'level': '三级甲等',
                'type': '综合医院',
                'contact_person': '管理员',
                'contact_phone': '010-xxxxxxxx'
            },
            {
                'name': '中国医学科学院肿瘤医院',
                'code': 'CICAMS',
                'address': '北京市朝阳区潘家园南里17号',
                'level': '三级甲等',
                'type': '专科医院',
                'contact_person': '管理员',
                'contact_phone': '010-xxxxxxxx'
            },
            {
                'name': '首都医科大学附属北京天坛医院',
                'code': 'BTTH',
                'address': '北京市丰台区南四环西路119号',
                'level': '三级甲等',
                'type': '综合医院',
                'contact_person': '管理员',
                'contact_phone': '010-xxxxxxxx'
            },
            {
                'name': '北京中医药大学东方医院',
                'code': 'BUCMDEH',
                'address': '北京市丰台区方庄芳星园一区6号',
                'level': '三级甲等',
                'type': '中医医院',
                'contact_person': '管理员',
                'contact_phone': '010-xxxxxxxx'
            }
        ]
            
        # 添加医院数据
        added_count = 0
        for hospital_data in hospitals_data:
            # 检查医院是否已存在
            existing = Hospital.query.filter_by(name=hospital_data['name']).first()
            if not existing:
                hospital = Hospital(**hospital_data)
                db.session.add(hospital)
                added_count += 1
            else:
                print(f"医院 '{hospital_data['name']}' 已存在，跳过添加。")
        
        # 提交到数据库
        if added_count > 0:
            db.session.commit()
            print(f"成功添加 {added_count} 家医院")
        else:
            print("没有新医院需要添加")
        
        # 显示当前所有医院
        all_hospitals = Hospital.query.all()
        print(f"\n当前医院总数: {len(all_hospitals)}")
        if all_hospitals:
            print("\n医院列表:")
            for hospital in all_hospitals:
                print(f"ID: {hospital.id}, 名称: {hospital.name}, 代码: {hospital.code}, 等级: {hospital.level}, 类型: {hospital.type}")
        
if __name__ == "__main__":
    add_hospitals() 