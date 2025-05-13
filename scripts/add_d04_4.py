#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# 添加项目根目录到系统路径，确保能够导入app包
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import current_app
from app import create_app, db
from app.models.indicator import Indicator

def add_d04_4():
    """添加 D04.4 指标：病案首页24小时内完成率"""
    
    # 创建应用上下文
    app = create_app()
    with app.app_context():
        # 获取主指标 D04
        main_indicator = Indicator.query.filter_by(code='D04').first()
        if not main_indicator:
            print("主指标 D04 不存在，无法添加子指标")
            return
            
        # 检查 D04.4 是否已存在
        existing = Indicator.query.filter_by(code='D04.4').first()
        if existing:
            print("D04.4 指标已存在")
            return
            
        # 创建新指标
        indicator = Indicator(
            code='D04.4',
            name='病案首页24小时内完成率',
            definition='病案首页在患者出院后24小时内完成的病历数占同期出院患者病历总数的比例',
            calculation_formula='(病案首页在患者出院后24小时内完成的病历数 ÷ 同期出院患者病历总数) × 100%',
            numerator_description='病案首页在患者出院后24小时内完成的病历数',
            denominator_description='同期出院患者病历总数',
            data_source='医院填报',
            unit='%',
            target_value=None,
            frequency='月度',
            category_id=main_indicator.category_id
        )
        
        # 添加到数据库
        db.session.add(indicator)
        db.session.commit()
        print("已成功添加 D04.4 指标")

if __name__ == "__main__":
    add_d04_4() 