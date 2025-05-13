#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# 添加项目根目录到系统路径，确保能够导入app包
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import current_app
from app import create_app, db
from app.models.indicator import Indicator

def import_more_sub_indicators():
    """导入其他指标的子指标"""
    
    # 创建应用上下文
    app = create_app()
    with app.app_context():
        
        # 1. 指标9（疼痛评估规范率）的子指标
        main_indicator = Indicator.query.filter_by(code='B03').first()
        if main_indicator:
            sub_indicators = [
                {
                    'code': 'B03.1', 
                    'name': '门诊疼痛评估规范率',
                    'definition': '疼痛门诊完成疼痛程度评估例数占同期门诊患者数的比例',
                    'calculation_formula': '(疼痛门诊患者例数 ÷ 同期疼痛门诊患者总例数) × 100%',
                    'numerator_description': '疼痛门诊患者例数',
                    'denominator_description': '同期疼痛门诊患者总例数',
                    'data_source': '医院填报',
                    'unit': '%',
                    'target_value': None,
                    'frequency': '季度',
                    'category_id': main_indicator.category_id
                },
                {
                    'code': 'B03.2', 
                    'name': '住院患者入院8h内评估规范率',
                    'definition': '入院8h内完成疼痛程度评估的住院患者例数占住院患者总例数的比例',
                    'calculation_formula': '(入院8h内完成疼痛程度评估的住院患者例数 ÷ 住院患者总例数) × 100%',
                    'numerator_description': '入院8h内完成疼痛程度评估的住院患者例数',
                    'denominator_description': '住院患者总例数',
                    'data_source': '医院填报',
                    'unit': '%',
                    'target_value': None,
                    'frequency': '季度',
                    'category_id': main_indicator.category_id
                }
            ]
            
            # 添加指标9的子指标
            added_count = 0
            for indicator_data in sub_indicators:
                existing = Indicator.query.filter_by(code=indicator_data['code']).first()
                if not existing:
                    indicator = Indicator(**indicator_data)
                    db.session.add(indicator)
                    added_count += 1
            
            print(f"成功添加 {added_count} 个疼痛评估规范率子指标")
        
        # 2. 指标17（住院患者静脉输液规范使用率）的子指标
        main_indicator = Indicator.query.filter_by(code='B11').first()
        if main_indicator:
            # 更新主指标名称
            main_indicator.name = '住院患者静脉输液规范使用率'
            db.session.add(main_indicator)
            
            sub_indicators = [
                {
                    'code': 'B11.1', 
                    'name': '住院患者静脉输液使用率',
                    'definition': '使用静脉输液的住院患者人数占同期住院患者总人数的比例',
                    'calculation_formula': '(使用静脉输液的出院患者人数 ÷ 同期出院患者总人次数) × 100%',
                    'numerator_description': '静脉输液的定义为给药途径为静脉滴注、静脉推注和泵入且输注液体量为50ml以上，按出院人次计算',
                    'denominator_description': '同期出院患者总人次数，未用药的出院患者也纳入统计',
                    'data_source': '医院填报',
                    'unit': '%',
                    'target_value': None,
                    'frequency': '季度',
                    'category_id': main_indicator.category_id
                },
                {
                    'code': 'B11.2', 
                    'name': '住院患者静脉输液平均每床日使用数量',
                    'definition': '考核住院患者平均每床日使用静脉输液的数量（袋/瓶）',
                    'calculation_formula': '静脉输液使用总袋/瓶数 ÷ 同期出院患者累计总床日数',
                    'numerator_description': '给药途径为静脉滴注、静脉推注和泵入的50ml以上大输液消耗数量，单位为瓶、袋',
                    'denominator_description': '同期所有出院患者累计总床日数',
                    'data_source': '医院填报',
                    'unit': '袋/瓶',
                    'target_value': None,
                    'frequency': '季度',
                    'category_id': main_indicator.category_id
                },
                {
                    'code': 'B11.3', 
                    'name': '住院患者静脉输液平均每床日使用体积',
                    'definition': '住院患者平均每床日使用静脉输液的体积数（毫升/ml）',
                    'calculation_formula': '静脉输液总体积数 ÷ 同期出院患者累计总床日数',
                    'numerator_description': '给药途径为静脉滴注、静脉推注和泵入的50ml以上大输液消耗总体积(ml)',
                    'denominator_description': '同期所有出院患者累计总床日数',
                    'data_source': '医院填报',
                    'unit': 'ml',
                    'target_value': None,
                    'frequency': '季度',
                    'category_id': main_indicator.category_id
                },
                {
                    'code': 'B11.4', 
                    'name': '住院患者平均使用输液药品品种数量',
                    'definition': '考核住院患者平均使用输液药品品种的数量',
                    'calculation_formula': '出院患者静脉输液药品品种总数 ÷ 同期出院患者总人次数',
                    'numerator_description': '出院患者给药途径为静脉滴注、静脉推注和泵入且输注液体量50ml以上的药品（不含溶媒）累积数量之和，按药品品规数算',
                    'denominator_description': '同期出院患者总人次数，未用药的出院患者也纳入统计',
                    'data_source': '医院填报',
                    'unit': '个',
                    'target_value': None,
                    'frequency': '季度',
                    'category_id': main_indicator.category_id
                }
            ]
            
            # 添加指标17的子指标
            added_count = 0
            for indicator_data in sub_indicators:
                existing = Indicator.query.filter_by(code=indicator_data['code']).first()
                if not existing:
                    indicator = Indicator(**indicator_data)
                    db.session.add(indicator)
                    added_count += 1
            
            print(f"成功添加 {added_count} 个住院患者静脉输液规范使用率子指标")
        
        # 3. 指标31（非计划重返手术室再手术率）子指标
        main_indicator = Indicator.query.filter_by(code='C06').first()
        if main_indicator:
            sub_indicators = [
                {
                    'code': 'C06.1', 
                    'name': '非计划重返手术室再手术率',
                    'definition': '指手术患者术后非预期重返手术室再次手术例数占同期手术患者手术例数的比例',
                    'calculation_formula': '(手术患者术后非预期重返手术室再次手术例数 ÷ 同期手术患者总手术例数) × 100%',
                    'numerator_description': '非预期重返手术室再次手术总例数',
                    'denominator_description': '同期手术患者总手术例数',
                    'data_source': '医院填报',
                    'unit': '%',
                    'target_value': 0.18,
                    'frequency': '季度',
                    'category_id': main_indicator.category_id
                },
                {
                    'code': 'C06.2', 
                    'name': '手术患者术后48小时内非计划重返手术室再次手术率',
                    'definition': '手术患者术后48小时内非预期重返手术室再次手术例数占同期手术患者手术例数的比例',
                    'calculation_formula': '(手术患者术后48小时内非预期重返手术室再次手术例数 ÷ 同期手术患者手术例数的比例) × 100%',
                    'numerator_description': '48小时内非预期重返手术室再次手术例数',
                    'denominator_description': '同期手术患者总手术例数',
                    'data_source': '医院填报',
                    'unit': '%',
                    'target_value': None,
                    'frequency': '季度',
                    'category_id': main_indicator.category_id
                },
                {
                    'code': 'C06.3', 
                    'name': '手术患者术后31天内非计划重返手术室再次手术率',
                    'definition': '手术患者术后31天内非预期重返手术室再次手术例数占同期手术患者手术例数的比例',
                    'calculation_formula': '(手术患者术后31天内非预期重返手术室再次手术例数 ÷ 同期手术患者手术例数的比例) × 100%',
                    'numerator_description': '31天内非预期重返手术室再次手术例数',
                    'denominator_description': '同期手术患者总手术例数',
                    'data_source': '医院填报',
                    'unit': '%',
                    'target_value': None,
                    'frequency': '季度',
                    'category_id': main_indicator.category_id
                }
            ]
            
            # 添加指标31的子指标
            added_count = 0
            for indicator_data in sub_indicators:
                existing = Indicator.query.filter_by(code=indicator_data['code']).first()
                if not existing:
                    indicator = Indicator(**indicator_data)
                    db.session.add(indicator)
                    added_count += 1
            
            print(f"成功添加 {added_count} 个非计划重返手术室再手术率子指标")
        
        # 4. 指标39（病案首页主要诊断编码正确率）子指标
        main_indicator = Indicator.query.filter_by(code='D03').first()
        if main_indicator:
            sub_indicators = [
                {
                    'code': 'D03.1', 
                    'name': '病案首页主要诊断填写正确率',
                    'definition': '单位时间内，病案首页中主要诊断填写正确的出院患者病历数占同期出院患者病历总数的比例',
                    'calculation_formula': '(病案首页中主要诊断填写正确的出院患者病历数 ÷ 同期出院患者病历总数) × 100%',
                    'numerator_description': '病案首页中主要诊断填写正确的出院患者病历数',
                    'denominator_description': '单位时间内，医疗机构所有出院患者病历总数',
                    'data_source': '医院填报',
                    'unit': '%',
                    'target_value': None,
                    'frequency': '季度',
                    'category_id': main_indicator.category_id
                },
                {
                    'code': 'D03.2', 
                    'name': '病案首页主要诊断编码正确率',
                    'definition': '单位时间内，病案首页中主要诊断编码正确的出院患者病历数占同期出院患者病历总数的比例',
                    'calculation_formula': '(病案首页中主要诊断编码正确的出院患者病历数 ÷ 同期出院患者病历总数) × 100%',
                    'numerator_description': '病案首页中主要诊断编码正确的出院患者病历数',
                    'denominator_description': '单位时间内，医疗机构所有出院患者病历总数',
                    'data_source': '医院填报',
                    'unit': '%',
                    'target_value': None,
                    'frequency': '季度',
                    'category_id': main_indicator.category_id
                }
            ]
            
            # 添加指标39的子指标
            added_count = 0
            for indicator_data in sub_indicators:
                existing = Indicator.query.filter_by(code=indicator_data['code']).first()
                if not existing:
                    indicator = Indicator(**indicator_data)
                    db.session.add(indicator)
                    added_count += 1
            
            print(f"成功添加 {added_count} 个病案首页主要诊断编码正确率子指标")
        
        # 提交更改
        db.session.commit()

def delete_indicators():
    """删除B12、B14、B17、B19指标及其子指标"""
    
    # 创建应用上下文
    app = create_app()
    with app.app_context():
        # 要删除的指标代码列表
        codes_to_delete = ['B12', 'B14', 'B17', 'B19']  # 移除B13，保留危急值处置及时率
        
        for code in codes_to_delete:
            # 删除主指标
            main_indicator = Indicator.query.filter_by(code=code).first()
            if main_indicator:
                db.session.delete(main_indicator)
                print(f"已删除指标 {code}")
            
            # 删除子指标
            sub_indicators = Indicator.query.filter(Indicator.code.like(f'{code}.%')).all()
            for sub in sub_indicators:
                db.session.delete(sub)
                print(f"已删除子指标 {sub.code}")
        
        # 提交更改
        db.session.commit()
        print("删除操作完成")

def update_indicator_code():
    """将B15改为B12，B16改为B13"""
    
    # 创建应用上下文
    app = create_app()
    with app.app_context():
        # 更新B15到B12
        indicator = Indicator.query.filter_by(code='B15').first()
        if indicator:
            indicator.code = 'B12'
            db.session.add(indicator)
            
            # 更新B15的子指标代码
            sub_indicators = Indicator.query.filter(Indicator.code.like('B15.%')).all()
            for sub in sub_indicators:
                new_code = sub.code.replace('B15', 'B12')
                sub.code = new_code
                db.session.add(sub)
                print(f"已更新子指标代码 {sub.code}")
            
            print("已将B15危急值报告及时率改为B12")
        else:
            print("未找到B15指标")
            
        # 更新B16到B13
        indicator = Indicator.query.filter_by(code='B16').first()
        if indicator:
            indicator.code = 'B13'
            db.session.add(indicator)
            
            # 更新B16的子指标代码
            sub_indicators = Indicator.query.filter(Indicator.code.like('B16.%')).all()
            for sub in sub_indicators:
                new_code = sub.code.replace('B16', 'B13')
                sub.code = new_code
                db.session.add(sub)
                print(f"已更新子指标代码 {sub.code}")
            
            print("已将B16危急值处置及时率改为B13")
        else:
            print("未找到B16指标")
        
        # 提交更改
        db.session.commit()

def add_critical_value_indicators():
    """添加危急值相关指标"""
    
    # 创建应用上下文
    app = create_app()
    with app.app_context():
        # 添加B12危急值报告及时率
        indicator_data = {
            'code': 'B12',
            'name': '危急值报告及时率',
            'definition': '危急值报告及时例数占同期危急值总例数的比例',
            'calculation_formula': '(危急值报告及时例数 ÷ 同期危急值总例数) × 100%',
            'numerator_description': '危急值报告及时例数',
            'denominator_description': '同期危急值总例数',
            'data_source': '医院填报',
            'unit': '%',
            'target_value': None,
            'frequency': '季度',
            'category_id': 2  # 假设2是B类指标的category_id
        }
        
        # 检查是否已存在
        existing = Indicator.query.filter_by(code='B12').first()
        if not existing:
            indicator = Indicator(**indicator_data)
            db.session.add(indicator)
            print("已添加B12危急值报告及时率")
            
            # 添加子指标
            sub_indicators = [
                {
                    'code': 'B12.1',
                    'name': '检验危急值报告及时率',
                    'definition': '检验危急值报告及时例数占同期检验危急值总例数的比例',
                    'calculation_formula': '(检验危急值报告及时例数 ÷ 同期检验危急值总例数) × 100%',
                    'numerator_description': '检验危急值报告及时例数',
                    'denominator_description': '同期检验危急值总例数',
                    'data_source': '医院填报',
                    'unit': '%',
                    'target_value': None,
                    'frequency': '季度',
                    'category_id': 2
                },
                {
                    'code': 'B12.2',
                    'name': '影像危急值报告及时率',
                    'definition': '影像危急值报告及时例数占同期影像危急值总例数的比例',
                    'calculation_formula': '(影像危急值报告及时例数 ÷ 同期影像危急值总例数) × 100%',
                    'numerator_description': '影像危急值报告及时例数',
                    'denominator_description': '同期影像危急值总例数',
                    'data_source': '医院填报',
                    'unit': '%',
                    'target_value': None,
                    'frequency': '季度',
                    'category_id': 2
                }
            ]
            
            for sub_data in sub_indicators:
                sub = Indicator(**sub_data)
                db.session.add(sub)
                print(f"已添加子指标 {sub_data['code']}")
        
        # 添加B13危急值处置及时率
        indicator_data = {
            'code': 'B13',
            'name': '危急值处置及时率',
            'definition': '危急值处置及时例数占同期危急值总例数的比例',
            'calculation_formula': '(危急值处置及时例数 ÷ 同期危急值总例数) × 100%',
            'numerator_description': '危急值处置及时例数',
            'denominator_description': '同期危急值总例数',
            'data_source': '医院填报',
            'unit': '%',
            'target_value': None,
            'frequency': '季度',
            'category_id': 2
        }
        
        # 检查是否已存在
        existing = Indicator.query.filter_by(code='B13').first()
        if not existing:
            indicator = Indicator(**indicator_data)
            db.session.add(indicator)
            print("已添加B13危急值处置及时率")
            
            # 添加子指标
            sub_indicators = [
                {
                    'code': 'B13.1',
                    'name': '检验危急值处置及时率',
                    'definition': '检验危急值处置及时例数占同期检验危急值总例数的比例',
                    'calculation_formula': '(检验危急值处置及时例数 ÷ 同期检验危急值总例数) × 100%',
                    'numerator_description': '检验危急值处置及时例数',
                    'denominator_description': '同期检验危急值总例数',
                    'data_source': '医院填报',
                    'unit': '%',
                    'target_value': None,
                    'frequency': '季度',
                    'category_id': 2
                },
                {
                    'code': 'B13.2',
                    'name': '影像危急值处置及时率',
                    'definition': '影像危急值处置及时例数占同期影像危急值总例数的比例',
                    'calculation_formula': '(影像危急值处置及时例数 ÷ 同期影像危急值总例数) × 100%',
                    'numerator_description': '影像危急值处置及时例数',
                    'denominator_description': '同期影像危急值总例数',
                    'data_source': '医院填报',
                    'unit': '%',
                    'target_value': None,
                    'frequency': '季度',
                    'category_id': 2
                }
            ]
            
            for sub_data in sub_indicators:
                sub = Indicator(**sub_data)
                db.session.add(sub)
                print(f"已添加子指标 {sub_data['code']}")
        
        # 提交更改
        db.session.commit()

def add_rehabilitation_indicator():
    """添加B15早期康复介入率指标"""
    
    # 创建应用上下文
    app = create_app()
    with app.app_context():
        # 添加B15早期康复介入率
        indicator_data = {
            'code': 'B15',
            'name': '早期康复介入率',
            'definition': '早期康复介入的住院患者人数占同期住院患者总人数的比例',
            'calculation_formula': '(早期康复介入的住院患者人数 ÷ 同期住院患者总人数) × 100%',
            'numerator_description': '早期康复介入的住院患者人数',
            'denominator_description': '同期住院患者总人数',
            'data_source': '医院填报',
            'unit': '%',
            'target_value': None,
            'frequency': '季度',
            'category_id': 2
        }
        
        # 检查是否已存在
        existing = Indicator.query.filter_by(code='B15').first()
        if not existing:
            indicator = Indicator(**indicator_data)
            db.session.add(indicator)
            print("已添加B15早期康复介入率")
            
            # 添加子指标
            sub_indicators = [
                {
                    'code': 'B15.1',
                    'name': '神经内科早期康复介入率',
                    'definition': '神经内科早期康复介入的住院患者人数占同期神经内科住院患者总人数的比例',
                    'calculation_formula': '(神经内科早期康复介入的住院患者人数 ÷ 同期神经内科住院患者总人数) × 100%',
                    'numerator_description': '神经内科早期康复介入的住院患者人数',
                    'denominator_description': '同期神经内科住院患者总人数',
                    'data_source': '医院填报',
                    'unit': '%',
                    'target_value': None,
                    'frequency': '季度',
                    'category_id': 2
                },
                {
                    'code': 'B15.2',
                    'name': '骨科早期康复介入率',
                    'definition': '骨科早期康复介入的住院患者人数占同期骨科住院患者总人数的比例',
                    'calculation_formula': '(骨科早期康复介入的住院患者人数 ÷ 同期骨科住院患者总人数) × 100%',
                    'numerator_description': '骨科早期康复介入的住院患者人数',
                    'denominator_description': '同期骨科住院患者总人数',
                    'data_source': '医院填报',
                    'unit': '%',
                    'target_value': None,
                    'frequency': '季度',
                    'category_id': 2
                },
                {
                    'code': 'B15.3',
                    'name': '神经外科早期康复介入率',
                    'definition': '神经外科早期康复介入的住院患者人数占同期神经外科住院患者总人数的比例',
                    'calculation_formula': '(神经外科早期康复介入的住院患者人数 ÷ 同期神经外科住院患者总人数) × 100%',
                    'numerator_description': '神经外科早期康复介入的住院患者人数',
                    'denominator_description': '同期神经外科住院患者总人数',
                    'data_source': '医院填报',
                    'unit': '%',
                    'target_value': None,
                    'frequency': '季度',
                    'category_id': 2
                },
                {
                    'code': 'B15.4',
                    'name': '重症医学科早期康复介入率',
                    'definition': '重症医学科早期康复介入的住院患者人数占同期重症医学科住院患者总人数的比例',
                    'calculation_formula': '(重症医学科早期康复介入的住院患者人数 ÷ 同期重症医学科住院患者总人数) × 100%',
                    'numerator_description': '重症医学科早期康复介入的住院患者人数',
                    'denominator_description': '同期重症医学科住院患者总人数',
                    'data_source': '医院填报',
                    'unit': '%',
                    'target_value': None,
                    'frequency': '季度',
                    'category_id': 2
                },
                {
                    'code': 'B15.5',
                    'name': '呼吸内科早期康复介入率',
                    'definition': '呼吸内科早期康复介入的住院患者人数占同期呼吸内科住院患者总人数的比例',
                    'calculation_formula': '(呼吸内科早期康复介入的住院患者人数 ÷ 同期呼吸内科住院患者总人数) × 100%',
                    'numerator_description': '呼吸内科早期康复介入的住院患者人数',
                    'denominator_description': '同期呼吸内科住院患者总人数',
                    'data_source': '医院填报',
                    'unit': '%',
                    'target_value': None,
                    'frequency': '季度',
                    'category_id': 2
                },
                {
                    'code': 'B15.6',
                    'name': '心内科早期康复介入率',
                    'definition': '心内科早期康复介入的住院患者人数占同期心内科住院患者总人数的比例',
                    'calculation_formula': '(心内科早期康复介入的住院患者人数 ÷ 同期心内科住院患者总人数) × 100%',
                    'numerator_description': '心内科早期康复介入的住院患者人数',
                    'denominator_description': '同期心内科住院患者总人数',
                    'data_source': '医院填报',
                    'unit': '%',
                    'target_value': None,
                    'frequency': '季度',
                    'category_id': 2
                },
                {
                    'code': 'B15.7',
                    'name': '普外科早期康复介入率',
                    'definition': '普外科早期康复介入的住院患者人数占同期普外科住院患者总人数的比例',
                    'calculation_formula': '(普外科早期康复介入的住院患者人数 ÷ 同期普外科住院患者总人数) × 100%',
                    'numerator_description': '普外科早期康复介入的住院患者人数',
                    'denominator_description': '同期普外科住院患者总人数',
                    'data_source': '医院填报',
                    'unit': '%',
                    'target_value': None,
                    'frequency': '季度',
                    'category_id': 2
                },
                {
                    'code': 'B15.8',
                    'name': '胸外科早期康复介入率',
                    'definition': '胸外科早期康复介入的住院患者人数占同期胸外科住院患者总人数的比例',
                    'calculation_formula': '(胸外科早期康复介入的住院患者人数 ÷ 同期胸外科住院患者总人数) × 100%',
                    'numerator_description': '胸外科早期康复介入的住院患者人数',
                    'denominator_description': '同期胸外科住院患者总人数',
                    'data_source': '医院填报',
                    'unit': '%',
                    'target_value': None,
                    'frequency': '季度',
                    'category_id': 2
                },
                {
                    'code': 'B15.9',
                    'name': '妇产科早期康复介入率',
                    'definition': '妇产科早期康复介入的住院患者人数占同期妇产科住院患者总人数的比例',
                    'calculation_formula': '(妇产科早期康复介入的住院患者人数 ÷ 同期妇产科住院患者总人数) × 100%',
                    'numerator_description': '妇产科早期康复介入的住院患者人数',
                    'denominator_description': '同期妇产科住院患者总人数',
                    'data_source': '医院填报',
                    'unit': '%',
                    'target_value': None,
                    'frequency': '季度',
                    'category_id': 2
                }
            ]
            
            for sub_data in sub_indicators:
                sub = Indicator(**sub_data)
                db.session.add(sub)
                print(f"已添加子指标 {sub_data['code']}")
        
        # 提交更改
        db.session.commit()

def add_surgery_followup_indicator():
    """添加B16四级手术患者随访率指标"""
    
    # 创建应用上下文
    app = create_app()
    with app.app_context():
        # 先删除已存在的B16指标
        existing = Indicator.query.filter_by(code='B16').first()
        if existing:
            db.session.delete(existing)
            db.session.commit()
            print("已删除B16指标")
        
        # 添加B16四级手术患者随访率
        indicator_data = {
            'code': 'B16',
            'name': '四级手术患者随访率',
            'definition': '四级手术患者随访例数占同期四级手术患者总例数的比例',
            'calculation_formula': '(四级手术患者随访例数 ÷ 同期四级手术患者总例数) × 100%',
            'numerator_description': '四级手术患者随访例数',
            'denominator_description': '同期四级手术患者总例数',
            'data_source': '医院填报',
            'unit': '%',
            'target_value': None,
            'frequency': '季度',
            'category_id': 2
        }
        
        indicator = Indicator(**indicator_data)
        db.session.add(indicator)
        print("已添加B16四级手术患者随访率")
        
        # 提交更改
        db.session.commit()

def add_cancer_followup_indicator():
    """添加B17恶性肿瘤患者随访率指标"""
    
    # 创建应用上下文
    app = create_app()
    with app.app_context():
        # 先删除已存在的B17指标
        existing = Indicator.query.filter_by(code='B17').first()
        if existing:
            db.session.delete(existing)
            db.session.commit()
            print("已删除B17指标")
        
        # 添加B17恶性肿瘤患者随访率
        indicator_data = {
            'code': 'B17',
            'name': '恶性肿瘤患者随访率',
            'definition': '恶性肿瘤患者随访例数占同期恶性肿瘤患者总例数的比例',
            'calculation_formula': '(恶性肿瘤患者随访例数 ÷ 同期恶性肿瘤患者总例数) × 100%',
            'numerator_description': '恶性肿瘤患者随访例数',
            'denominator_description': '同期恶性肿瘤患者总例数',
            'data_source': '医院填报',
            'unit': '%',
            'target_value': None,
            'frequency': '季度',
            'category_id': 2
        }
        
        indicator = Indicator(**indicator_data)
        db.session.add(indicator)
        print("已添加B17恶性肿瘤患者随访率")
        
        # 提交更改
        db.session.commit()

def add_adverse_event_indicator():
    """添加B18每百出院人次主动报告不良事件例次指标"""
    
    # 创建应用上下文
    app = create_app()
    with app.app_context():
        # 先删除已存在的B18指标
        existing = Indicator.query.filter_by(code='B18').first()
        if existing:
            db.session.delete(existing)
            db.session.commit()
            print("已删除B18指标")
        
        # 添加B18每百出院人次主动报告不良事件例次
        indicator_data = {
            'code': 'B18',
            'name': '每百出院人次主动报告不良事件例次',
            'definition': '每百出院人次主动报告不良事件的例数',
            'calculation_formula': '(主动报告不良事件例数 ÷ 同期出院人次数) × 100',
            'numerator_description': '主动报告不良事件例数',
            'denominator_description': '同期出院人次数',
            'data_source': '医院填报',
            'unit': '例/百出院人次',
            'target_value': None,
            'frequency': '季度',
            'category_id': 2
        }
        
        indicator = Indicator(**indicator_data)
        db.session.add(indicator)
        print("已添加B18每百出院人次主动报告不良事件例次")
        
        # 提交更改
        db.session.commit()

if __name__ == '__main__':
    add_adverse_event_indicator() 