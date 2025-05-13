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
    """导入指标C11的所有子指标：住院患者手术术后获得性指标发生率的子指标"""
    
    # 创建应用上下文
    app = create_app()
    with app.app_context():
        # 确保主指标C11存在
        main_indicator = Indicator.query.filter_by(code='C11').first()
        if not main_indicator:
            print("主指标 C11 (住院患者手术术后获得性指标发生率) 不存在，请先导入主指标")
            return
            
        # 子指标数据 - 所有19个子指标
        sub_indicators = [
            {
                'code': 'C11.1', 
                'name': '手术患者手术后肺栓塞发生率',
                'definition': '住院患者手术后发生肺栓塞的例数占同期手术患者出院人次的比例',
                'calculation_formula': '(手术后发生肺栓塞的例数 ÷ 同期手术患者出院人次) × 100%',
                'numerator_description': '手术后发生肺栓塞的例数',
                'denominator_description': '同期手术患者出院人次',
                'data_source': '病案首页',
                'unit': '%',
                'target_value': None,
                'frequency': '季度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'C11.2', 
                'name': '手术患者手术后深静脉血栓发生率',
                'definition': '住院患者手术后发生深静脉血栓的例数占同期手术患者出院人次的比例',
                'calculation_formula': '(手术后发生深静脉血栓的例数 ÷ 同期手术患者出院人次) × 100%',
                'numerator_description': '手术后发生深静脉血栓的例数',
                'denominator_description': '同期手术患者出院人次',
                'data_source': '病案首页',
                'unit': '%',
                'target_value': None,
                'frequency': '季度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'C11.3', 
                'name': '手术患者手术后败血症发生率',
                'definition': '住院患者手术后发生败血症的例数占同期手术患者出院人次的比例',
                'calculation_formula': '(手术后发生败血症的例数 ÷ 同期手术患者出院人次) × 100%',
                'numerator_description': '手术后发生败血症的例数',
                'denominator_description': '同期手术患者出院人次',
                'data_source': '病案首页',
                'unit': '%',
                'target_value': None,
                'frequency': '季度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'C11.4', 
                'name': '手术患者手术后出血或血肿发生率',
                'definition': '住院患者手术后发生出血或血肿的例数占同期手术患者出院人次的比例',
                'calculation_formula': '(手术后发生出血或血肿的例数 ÷ 同期手术患者出院人次) × 100%',
                'numerator_description': '手术后发生出血或血肿的例数',
                'denominator_description': '同期手术患者出院人次',
                'data_source': '病案首页',
                'unit': '%',
                'target_value': None,
                'frequency': '季度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'C11.5', 
                'name': '手术患者手术伤口裂开发生率',
                'definition': '住院患者手术后发生伤口裂开的例数占同期手术患者出院人次的比例',
                'calculation_formula': '(手术后发生伤口裂开的例数 ÷ 同期手术患者出院人次) × 100%',
                'numerator_description': '手术后发生伤口裂开的例数',
                'denominator_description': '同期手术患者出院人次',
                'data_source': '病案首页',
                'unit': '%',
                'target_value': None,
                'frequency': '季度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'C11.6', 
                'name': '手术患者手术后猝死发生率',
                'definition': '住院患者手术后发生猝死的例数占同期手术患者出院人次的比例',
                'calculation_formula': '(手术后发生猝死的例数 ÷ 同期手术患者出院人次) × 100%',
                'numerator_description': '手术后发生猝死的例数',
                'denominator_description': '同期手术患者出院人次',
                'data_source': '病案首页',
                'unit': '%',
                'target_value': None,
                'frequency': '季度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'C11.7', 
                'name': '手术患者手术后呼吸衰竭发生率',
                'definition': '住院患者手术后发生呼吸衰竭的例数占同期手术患者出院人次的比例',
                'calculation_formula': '(手术后发生呼吸衰竭的例数 ÷ 同期手术患者出院人次) × 100%',
                'numerator_description': '手术后发生呼吸衰竭的例数',
                'denominator_description': '同期手术患者出院人次',
                'data_source': '病案首页',
                'unit': '%',
                'target_value': None,
                'frequency': '季度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'C11.8', 
                'name': '手术患者手术后生理/代谢紊乱发生率',
                'definition': '住院患者手术后发生生理/代谢紊乱的例数占同期手术患者出院人次的比例',
                'calculation_formula': '(手术后发生生理/代谢紊乱的例数 ÷ 同期手术患者出院人次) × 100%',
                'numerator_description': '手术后发生生理/代谢紊乱的例数',
                'denominator_description': '同期手术患者出院人次',
                'data_source': '病案首页',
                'unit': '%',
                'target_value': None,
                'frequency': '季度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'C11.9', 
                'name': '与手术/操作相关感染发生率',
                'definition': '与手术/操作相关感染发生例数占同期手术患者出院人次的比例',
                'calculation_formula': '(与手术/操作相关感染发生例数 ÷ 同期手术患者出院人次) × 100%',
                'numerator_description': '与手术/操作相关感染发生例数',
                'denominator_description': '同期手术患者出院人次',
                'data_source': '病案首页',
                'unit': '%',
                'target_value': None,
                'frequency': '季度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'C11.10', 
                'name': '手术过程中异物遗留发生率',
                'definition': '手术过程中异物遗留的例数占同期手术患者出院人次的比例',
                'calculation_formula': '(手术过程中异物遗留的例数 ÷ 同期手术患者出院人次) × 100%',
                'numerator_description': '手术过程中异物遗留的例数',
                'denominator_description': '同期手术患者出院人次',
                'data_source': '病案首页',
                'unit': '%',
                'target_value': None,
                'frequency': '季度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'C11.11', 
                'name': '手术患者麻醉并发症发生率',
                'definition': '住院患者手术后发生麻醉并发症的例数占同期手术患者出院人次的比例',
                'calculation_formula': '(手术后发生麻醉并发症的例数 ÷ 同期手术患者出院人次) × 100%',
                'numerator_description': '手术后发生麻醉并发症的例数',
                'denominator_description': '同期手术患者出院人次',
                'data_source': '病案首页',
                'unit': '%',
                'target_value': None,
                'frequency': '季度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'C11.12', 
                'name': '手术患者肺部感染与肺机能不全发生率',
                'definition': '住院患者手术后发生肺部感染与肺机能不全的例数占同期手术患者出院人次的比例',
                'calculation_formula': '(手术后发生肺部感染与肺机能不全的例数 ÷ 同期手术患者出院人次) × 100%',
                'numerator_description': '手术后发生肺部感染与肺机能不全的例数',
                'denominator_description': '同期手术患者出院人次',
                'data_source': '病案首页',
                'unit': '%',
                'target_value': None,
                'frequency': '季度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'C11.13', 
                'name': '手术意外穿刺伤或撕裂伤发生率',
                'definition': '手术过程中发生意外穿刺伤或撕裂伤的例数占同期手术患者出院人次的比例',
                'calculation_formula': '(手术过程中发生意外穿刺伤或撕裂伤的例数 ÷ 同期手术患者出院人次) × 100%',
                'numerator_description': '手术过程中发生意外穿刺伤或撕裂伤的例数',
                'denominator_description': '同期手术患者出院人次',
                'data_source': '病案首页',
                'unit': '%',
                'target_value': None,
                'frequency': '季度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'C11.14', 
                'name': '手术后急性肾衰竭发生率',
                'definition': '住院患者手术后发生急性肾衰竭的例数占同期手术患者出院人次的比例',
                'calculation_formula': '(手术后发生急性肾衰竭的例数 ÷ 同期手术患者出院人次) × 100%',
                'numerator_description': '手术后发生急性肾衰竭的例数',
                'denominator_description': '同期手术患者出院人次',
                'data_source': '病案首页',
                'unit': '%',
                'target_value': None,
                'frequency': '季度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'C11.15', 
                'name': '各系统/器官术后并发症发生率',
                'definition': '住院患者手术后发生各系统/器官并发症的例数占同期手术患者出院人次的比例',
                'calculation_formula': '(手术后发生各系统/器官并发症的例数 ÷ 同期手术患者出院人次) × 100%',
                'numerator_description': '手术后发生各系统/器官并发症的例数',
                'denominator_description': '同期手术患者出院人次',
                'data_source': '病案首页',
                'unit': '%',
                'target_value': None,
                'frequency': '季度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'C11.16', 
                'name': '植入物的并发症（不包括脓毒症）发生率',
                'definition': '住院患者手术后植入物并发症（不包括脓毒症）的例数占同期手术患者出院人次的比例',
                'calculation_formula': '(手术后植入物并发症（不包括脓毒症）的例数 ÷ 同期手术患者出院人次) × 100%',
                'numerator_description': '手术后植入物并发症（不包括脓毒症）的例数',
                'denominator_description': '同期手术患者出院人次',
                'data_source': '病案首页',
                'unit': '%',
                'target_value': None,
                'frequency': '季度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'C11.17', 
                'name': '再植和截肢的并发症发生率',
                'definition': '住院患者再植和截肢手术后并发症的例数占同期再植和截肢手术患者出院人次的比例',
                'calculation_formula': '(再植和截肢手术后并发症的例数 ÷ 同期再植和截肢手术患者出院人次) × 100%',
                'numerator_description': '再植和截肢手术后并发症的例数',
                'denominator_description': '同期再植和截肢手术患者出院人次',
                'data_source': '病案首页',
                'unit': '%',
                'target_value': None,
                'frequency': '季度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'C11.18', 
                'name': '介入操作与手术患者其他并发症发生率',
                'definition': '住院患者介入操作与手术后其他并发症的例数占同期手术患者出院人次的比例',
                'calculation_formula': '(介入操作与手术后其他并发症的例数 ÷ 同期手术患者出院人次) × 100%',
                'numerator_description': '介入操作与手术后其他并发症的例数',
                'denominator_description': '同期手术患者出院人次',
                'data_source': '病案首页',
                'unit': '%',
                'target_value': None,
                'frequency': '季度',
                'category_id': main_indicator.category_id
            },
            {
                'code': 'C11.19', 
                'name': '剖宫产分娩产妇产程和分娩并发症发生率',
                'definition': '剖宫产分娩产妇产程和分娩并发症的例数占同期剖宫产分娩产妇出院人次的比例',
                'calculation_formula': '(剖宫产分娩产妇产程和分娩并发症的例数 ÷ 同期剖宫产分娩产妇出院人次) × 100%',
                'numerator_description': '剖宫产分娩产妇产程和分娩并发症的例数',
                'denominator_description': '同期剖宫产分娩产妇出院人次',
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