#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# 添加项目根目录到系统路径，确保能够导入app包
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import current_app
from app import create_app, db
from app.models.indicator import Indicator

def import_perioperative_mortality_sub_indicators():
    """导入指标C07（围术期死亡率）的三个子指标"""
    
    # 创建应用上下文
    app = create_app()
    with app.app_context():
        # 确保主指标C07存在
        main_indicator = Indicator.query.filter_by(code='C07').first()
        if not main_indicator:
            print("主指标 C07 (围术期死亡率) 不存在，请先导入主指标")
            return
            
        # 围术期死亡率的三个子指标
        sub_indicators = [
            {
                'code': 'C07.1', 
                'name': '手术当日死亡率',
                'definition': '手术当日死亡的患者人数占同期手术患者总数的比例',
                'calculation_formula': '(手术当日死亡的患者人数 ÷ 同期手术患者总数) × 100%',
                'numerator_description': '手术当日死亡的患者人数',
                'denominator_description': '同期手术患者总数',
                'data_source': '病案首页',
                'unit': '%',
                'target_value': None,
                'frequency': '季度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'C07.2', 
                'name': '术后24小时内死亡率',
                'definition': '术后24小时内死亡的患者人数占同期手术患者总数的比例',
                'calculation_formula': '(术后24小时内死亡的患者人数 ÷ 同期手术患者总数) × 100%',
                'numerator_description': '术后24小时内死亡的患者人数',
                'denominator_description': '同期手术患者总数',
                'data_source': '病案首页',
                'unit': '%',
                'target_value': None,
                'frequency': '季度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'C07.3', 
                'name': '术后24-48小时内死亡率',
                'definition': '术后24-48小时内死亡的患者人数占同期手术患者总数的比例',
                'calculation_formula': '(术后24-48小时内死亡的患者人数 ÷ 同期手术患者总数) × 100%',
                'numerator_description': '术后24-48小时内死亡的患者人数',
                'denominator_description': '同期手术患者总数',
                'data_source': '病案首页',
                'unit': '%',
                'target_value': None,
                'frequency': '季度',
                'category_id': main_indicator.category_id
            }
        ]
        
        # 导入子指标
        added_count = 0
        for indicator_data in sub_indicators:
            # 检查指标是否已存在
            existing = Indicator.query.filter_by(code=indicator_data['code']).first()
            if not existing:
                indicator = Indicator(**indicator_data)
                db.session.add(indicator)
                added_count += 1
        
        if added_count > 0:
            db.session.commit()
            print(f"成功导入 {added_count} 个围术期死亡率子指标")
        else:
            print("没有新指标需要导入，围术期死亡率子指标可能已存在")
            
if __name__ == "__main__":
    import_perioperative_mortality_sub_indicators()
