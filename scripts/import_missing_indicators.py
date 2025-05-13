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
    """导入指标40的四个子指标：病历记录及时性（D04）的子指标"""
    
    # 创建应用上下文
    app = create_app()
    with app.app_context():
        # 确保主指标D04存在
        main_indicator = Indicator.query.filter_by(code='D04').first()
        if not main_indicator:
            print("主指标 D04 (病历记录及时性) 不存在，请先导入主指标")
            return
            
        # 四个子指标数据
        sub_indicators = [
            {
                'code': 'D04.1', 
                'name': '入院记录24小时内完成率',
                'definition': '入院记录在患者入院24小时内完成的住院患者病历数占同期住院患者病历总数的比例',
                'calculation_formula': '(入院记录在患者入院24小时内完成的住院患者病历数 ÷ 同期住院患者病历总数) × 100%',
                'numerator_description': '入院记录在患者入院24小时内完成的住院患者病历数',
                'denominator_description': '同期住院患者病历总数',
                'data_source': '医院填报',
                'unit': '%',
                'target_value': None,
                'frequency': '月度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'D04.2', 
                'name': '手术记录24小时内完成率',
                'definition': '手术记录在术后24小时内完成的住院患者病历数占同期住院手术患者病历总数的比例',
                'calculation_formula': '(手术记录在术后24小时内完成的住院患者病历数 ÷ 同期住院手术患者病历总数) × 100%',
                'numerator_description': '手术记录在术后24小时内完成的住院患者病历数',
                'denominator_description': '同期住院手术患者病历总数',
                'data_source': '医院填报',
                'unit': '%',
                'target_value': None,
                'frequency': '月度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'D04.3', 
                'name': '出院记录24小时内完成率',
                'definition': '出院记录在患者出院后24小时内完成的病历数占同期出院患者病历总数的比例',
                'calculation_formula': '(出院记录在患者出院后24小时内完成的病历数 ÷ 同期出院患者病历总数) × 100%',
                'numerator_description': '出院记录在患者出院后24小时内完成的病历数',
                'denominator_description': '同期出院患者病历总数',
                'data_source': '医院填报',
                'unit': '%',
                'target_value': None,
                'frequency': '月度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'D04.4', 
                'name': '病案首页24小时内完成率',
                'definition': '病案首页在患者出院后24小时内完成的病历数占同期出院患者病历总数的比例',
                'calculation_formula': '(病案首页在患者出院后24小时内完成的病历数 ÷ 同期出院患者病历总数) × 100%',
                'numerator_description': '病案首页在患者出院后24小时内完成的病历数',
                'denominator_description': '同期出院患者病历总数',
                'data_source': '医院填报',
                'unit': '%',
                'target_value': None,
                'frequency': '月度',
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
        
        print(f"成功添加 {added_count} 个病历记录及时性子指标")

if __name__ == '__main__':
    import_sub_indicators()
 