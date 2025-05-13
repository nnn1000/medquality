#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# 添加项目根目录到系统路径，确保能够导入app包
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import current_app
from app import create_app, db
from app.models.indicator import Indicator

def import_sub_indicators():
    """导入指标C11的子指标：住院患者手术术后获得性指标发生率的子指标"""
    
    # 创建应用上下文
    app = create_app()
    with app.app_context():
        # 确保主指标C11存在
        main_indicator = Indicator.query.filter_by(code='C11').first()
        if not main_indicator:
            print("主指标 C11 (住院患者手术术后获得性指标发生率) 不存在，请先导入主指标")
            return
            
        # 子指标数据
        sub_indicators = [
            {
                'code': 'C11.1', 
                'name': '手术部位感染率',
                'definition': '住院患者手术后发生手术部位感染的例数占同期手术患者出院人次的比例',
                'calculation_formula': '(手术后发生手术部位感染的例数 ÷ 同期手术患者出院人次) × 100%',
                'numerator_description': '手术后发生手术部位感染的例数',
                'denominator_description': '同期手术患者出院人次',
                'data_source': '病案首页',
                'unit': '%',
                'target_value': None,
                'frequency': '季度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'C11.2', 
                'name': '术后出血发生率',
                'definition': '住院患者手术后发生术后出血的例数占同期手术患者出院人次的比例',
                'calculation_formula': '(手术后发生术后出血的例数 ÷ 同期手术患者出院人次) × 100%',
                'numerator_description': '手术后发生术后出血的例数',
                'denominator_description': '同期手术患者出院人次',
                'data_source': '病案首页',
                'unit': '%',
                'target_value': None,
                'frequency': '季度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'C11.3', 
                'name': '术后呼吸系统并发症发生率',
                'definition': '住院患者手术后发生呼吸系统并发症(如肺不张、肺炎等)的例数占同期手术患者出院人次的比例',
                'calculation_formula': '(手术后发生呼吸系统并发症的例数 ÷ 同期手术患者出院人次) × 100%',
                'numerator_description': '手术后发生呼吸系统并发症的例数',
                'denominator_description': '同期手术患者出院人次',
                'data_source': '病案首页',
                'unit': '%',
                'target_value': None,
                'frequency': '季度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'C11.4', 
                'name': '术后心血管并发症发生率',
                'definition': '住院患者手术后发生心血管并发症(如心律失常、心肌梗死等)的例数占同期手术患者出院人次的比例',
                'calculation_formula': '(手术后发生心血管并发症的例数 ÷ 同期手术患者出院人次) × 100%',
                'numerator_description': '手术后发生心血管并发症的例数',
                'denominator_description': '同期手术患者出院人次',
                'data_source': '病案首页',
                'unit': '%',
                'target_value': None,
                'frequency': '季度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'C11.5', 
                'name': '术后泌尿系统感染率',
                'definition': '住院患者手术后发生泌尿系统感染的例数占同期手术患者出院人次的比例',
                'calculation_formula': '(手术后发生泌尿系统感染的例数 ÷ 同期手术患者出院人次) × 100%',
                'numerator_description': '手术后发生泌尿系统感染的例数',
                'denominator_description': '同期手术患者出院人次',
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
            else:
                print(f"子指标已存在: {indicator_data['code']} - {indicator_data['name']}")
        
        # 提交更改
        db.session.commit()
        
        print(f"成功添加 {added_count} 个住院患者手术术后获得性指标子指标")

if __name__ == '__main__':
    import_sub_indicators() 