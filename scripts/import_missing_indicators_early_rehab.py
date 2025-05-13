#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# 添加项目根目录到系统路径，确保能够导入app包
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import current_app
from app import create_app, db
from app.models.indicator import Indicator

def import_early_rehab_sub_indicators():
    """导入指标21（早期康复介入率）的子指标"""
    
    # 创建应用上下文
    app = create_app()
    with app.app_context():
        # 确保主指标B15存在
        main_indicator = Indicator.query.filter_by(code='B15').first()
        if not main_indicator:
            print("主指标 B15 (早期康复介入率) 不存在，请先导入主指标")
            return
            
        # 早期康复介入率的9个子指标
        sub_indicators = [
            {
                'code': 'B15.1', 
                'name': '早期康复介入率（神经内科）',
                'definition': '接受早期康复介入的神经内科住院患者数占同期神经内科住院患者总数的比例',
                'calculation_formula': '(接受早期康复介入的神经内科住院患者数 ÷ 同期神经内科住院患者总数) × 100%',
                'numerator_description': '接受早期康复介入的神经内科住院患者数',
                'denominator_description': '同期神经内科住院患者总数',
                'data_source': '医院填报',
                'unit': '%',
                'target_value': None,
                'frequency': '季度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'B15.2', 
                'name': '早期康复介入率（神经外科）',
                'definition': '接受早期康复介入的神经外科住院患者数占同期神经外科住院患者总数的比例',
                'calculation_formula': '(接受早期康复介入的神经外科住院患者数 ÷ 同期神经外科住院患者总数) × 100%',
                'numerator_description': '接受早期康复介入的神经外科住院患者数',
                'denominator_description': '同期神经外科住院患者总数',
                'data_source': '医院填报',
                'unit': '%',
                'target_value': None,
                'frequency': '季度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'B15.3', 
                'name': '早期康复介入率（骨科）',
                'definition': '接受早期康复介入的骨科住院患者数占同期骨科住院患者总数的比例',
                'calculation_formula': '(接受早期康复介入的骨科住院患者数 ÷ 同期骨科住院患者总数) × 100%',
                'numerator_description': '接受早期康复介入的骨科住院患者数',
                'denominator_description': '同期骨科住院患者总数',
                'data_source': '医院填报',
                'unit': '%',
                'target_value': None,
                'frequency': '季度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'B15.4', 
                'name': '早期康复介入率（心血管内科）',
                'definition': '接受早期康复介入的心血管内科住院患者数占同期心血管内科住院患者总数的比例',
                'calculation_formula': '(接受早期康复介入的心血管内科住院患者数 ÷ 同期心血管内科住院患者总数) × 100%',
                'numerator_description': '接受早期康复介入的心血管内科住院患者数',
                'denominator_description': '同期心血管内科住院患者总数',
                'data_source': '医院填报',
                'unit': '%',
                'target_value': None,
                'frequency': '季度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'B15.5', 
                'name': '早期康复介入率（重症ICU）',
                'definition': '接受早期康复介入的重症ICU住院患者数占同期重症ICU住院患者总数的比例',
                'calculation_formula': '(接受早期康复介入的重症ICU住院患者数 ÷ 同期重症ICU住院患者总数) × 100%',
                'numerator_description': '接受早期康复介入的重症ICU住院患者数',
                'denominator_description': '同期重症ICU住院患者总数',
                'data_source': '医院填报',
                'unit': '%',
                'target_value': None,
                'frequency': '季度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'B15.6', 
                'name': '早期康复介入率（脑卒中）',
                'definition': '接受早期康复介入的脑卒中住院患者数占同期脑卒中住院患者总数的比例',
                'calculation_formula': '(接受早期康复介入的脑卒中住院患者数 ÷ 同期脑卒中住院患者总数) × 100%',
                'numerator_description': '接受早期康复介入的脑卒中住院患者数',
                'denominator_description': '同期脑卒中住院患者总数',
                'data_source': '医院填报',
                'unit': '%',
                'target_value': None,
                'frequency': '季度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'B15.7', 
                'name': '早期康复介入率（脊髓损伤）',
                'definition': '接受早期康复介入的脊髓损伤住院患者数占同期脊髓损伤住院患者总数的比例',
                'calculation_formula': '(接受早期康复介入的脊髓损伤住院患者数 ÷ 同期脊髓损伤住院患者总数) × 100%',
                'numerator_description': '接受早期康复介入的脊髓损伤住院患者数',
                'denominator_description': '同期脊髓损伤住院患者总数',
                'data_source': '医院填报',
                'unit': '%',
                'target_value': None,
                'frequency': '季度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'B15.8', 
                'name': '早期康复介入率（髋、膝关节置换术后）',
                'definition': '接受早期康复介入的髋、膝关节置换术后住院患者数占同期髋、膝关节置换术后住院患者总数的比例',
                'calculation_formula': '(接受早期康复介入的髋、膝关节置换术后住院患者数 ÷ 同期髋、膝关节置换术后住院患者总数) × 100%',
                'numerator_description': '接受早期康复介入的髋、膝关节置换术后住院患者数',
                'denominator_description': '同期髋、膝关节置换术后住院患者总数',
                'data_source': '医院填报',
                'unit': '%',
                'target_value': None,
                'frequency': '季度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'B15.9', 
                'name': '康复评定率',
                'definition': '接受康复评定的康复医学科住院患者数占同期康复医学科住院患者总数的比例',
                'calculation_formula': '(接受康复评定的康复医学科住院患者数 ÷ 同期康复医学科住院患者总数) × 100%',
                'numerator_description': '接受康复评定的康复医学科住院患者数',
                'denominator_description': '同期康复医学科住院患者总数',
                'data_source': '医院填报',
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
        
        # 提交更改
        db.session.commit()
        
        print(f"成功添加 {added_count} 个早期康复介入率子指标")

if __name__ == '__main__':
    import_early_rehab_sub_indicators() 