#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.indicator import Indicator, IndicatorCategory

# 创建应用上下文
app = create_app()
app.app_context().push()

def import_indicators():
    """导入《东莞市全面提升医疗质量操作手册（2024版）》中40个医疗质量指标"""
    
    print("开始导入医疗质量指标...")
    
    # 确保指标类别存在
    categories = {
        'A': '急诊和日间医疗质量',
        'B': '医疗行为质量',
        'C': '结果质量',
        'D': '病历质量'
    }
    
    category_ids = {}
    for code, name in categories.items():
        category = IndicatorCategory.query.filter_by(name=name).first()
        if not category:
            category = IndicatorCategory(name=name, description=f"包含{name}相关的指标")
            db.session.add(category)
            db.session.flush()
        category_ids[code] = category.id
    
    # 提交类别更改
    db.session.commit()
    
    # 定义40个指标数据
    indicators_data = [
        # 急诊和日间医疗质量相关指标（6个）
        {
            'code': 'A01',
            'name': '平均急救响应时间',
            'definition': '从接听120呼救电话到救护车到达现场的平均时间',
            'calculation_formula': '平均急救响应时间 = 急救响应时间总时长 ÷ 车次',
            'numerator_description': '急救响应时间总时长',
            'denominator_description': '车次',
            'data_source': '医院填报',
            'unit': '分钟',
            'target_value': 15,
            'frequency': '月度',
            'category_id': category_ids['A']
        },
        {
            'code': 'A02',
            'name': '心脏骤停复苏成功率',
            'definition': 'ROSC成功是指急诊呼吸心脏骤停患者，心肺复苏术（CPR）后自主呼吸循环恢复超过24小时',
            'calculation_formula': 'ROSC成功率 = (ROSC成功总例次数 ÷ 同期急诊呼吸心脏骤停患者行心肺复苏术总例次数) × 100%',
            'numerator_description': '心脏骤停复苏成功总例次数',
            'denominator_description': '同期急诊呼吸心脏骤停患者行心肺复苏术总例次数',
            'data_source': '医院填报',
            'unit': '%',
            'target_value': None,
            'frequency': '季度',
            'category_id': category_ids['A']
        },
        {
            'code': 'A03',
            'name': '急性ST段抬高型心肌梗死再灌注治疗率',
            'definition': '发病12小时内首次医疗接触的STEMI患者接受再灌注治疗(PCI或静脉溶栓)的比例',
            'calculation_formula': '(发病12小时内实施再灌注治疗（静脉溶栓和/或PCI）的STEMI患者数 ÷ 同期发病12小时内具有再灌注治疗指征的STEMI患者数) × 100%',
            'numerator_description': '发病12小时内实施再灌注治疗（静脉溶栓和/或PCI）的STEMI患者数',
            'denominator_description': '同期发病12小时内具有再灌注治疗指征的STEMI患者数',
            'data_source': '医院填报',
            'unit': '%',
            'target_value': 75,
            'frequency': '季度',
            'category_id': category_ids['A']
        },
        {
            'code': 'A04',
            'name': '急性脑梗死再灌注治疗率',
            'definition': '同期发病6小时内到院接受静脉溶栓治疗或急诊血管内介入治疗的脑梗死患者与同期发病6小时内到院的脑梗死患者总数的比例',
            'calculation_formula': '(发病6小时内静脉溶栓治疗和（或）急诊血管内介入治疗的脑梗死患者总数 ÷ 同期发病6小时内到院的脑梗死患者总数) × 100%',
            'numerator_description': '发病6小时内静脉溶栓治疗和急诊血管内介入治疗的脑梗死患者总数',
            'denominator_description': '同期发病6小时内到院的脑梗死患者总数（ICD-10：I63）',
            'data_source': '医院填报',
            'unit': '%',
            'target_value': None,
            'frequency': '季度',
            'category_id': category_ids['A']
        },
        {
            'code': 'A05',
            'name': '开展日间医疗服务的医院占比',
            'definition': '考核医院是否开展日间医疗服务',
            'calculation_formula': '医院开展填写1，否则填写0',
            'numerator_description': '医院开展填写1，否则填写0',
            'denominator_description': '无',
            'data_source': '医院填报',
            'unit': '个',
            'target_value': 1,
            'frequency': '年度',
            'category_id': category_ids['A']
        },
        {
            'code': 'A06',
            'name': '日间手术占择期手术的比例',
            'definition': '考核年度出院患者施行日间手术台次数占同期出院患者择期手术总台次数的比例',
            'calculation_formula': '(日间手术台次数 ÷ 同期出院患者择期手术总台次数) × 100%',
            'numerator_description': '日间手术台次数是指日间手术患者人数',
            'denominator_description': '同期出院患者择期手术总台次数是指同期出院患者择期手术人数',
            'data_source': '医院填报',
            'unit': '%',
            'target_value': None,
            'frequency': '季度',
            'category_id': category_ids['A']
        },
        
        # 从B01开始添加医疗行为质量相关指标
        {
            'code': 'B01',
            'name': '肿瘤治疗前临床TNM分期评估率',
            'definition': '考核年度内符合纳入条件的10个癌种，首次治疗前完成临床TNM分期评估的患者数占同期首次治疗患者数的比例',
            'calculation_formula': '(某癌种首次治疗前完成临床TNM分期评估的患者数 ÷ 同期首次治疗的某癌种患者数) × 100%',
            'numerator_description': '某癌种首次治疗前完成临床TNM分期评估的患者数',
            'denominator_description': '同期首次治疗的某癌种患者数',
            'data_source': '医院填报',
            'unit': '%',
            'target_value': None,
            'frequency': '季度',
            'category_id': category_ids['B']
        },
        {
            'code': 'B02',
            'name': '营养风险筛查率',
            'definition': '考核单位时间内，接受营养风险筛查的住院患者数占同期住院患者总数的比例',
            'calculation_formula': '(单位时间内接受营养风险筛查的住院患者数 ÷ 同期住院患者总数) × 100%',
            'numerator_description': '单位时间内接受营养风险筛查的住院患者数',
            'denominator_description': '同期住院患者总数',
            'data_source': '医院填报',
            'unit': '%',
            'target_value': None,
            'frequency': '月度',
            'category_id': category_ids['B']
        },
        {
            'code': 'B03',
            'name': '疼痛评估规范率',
            'definition': '疼痛门诊完成疼痛程度评估例数占同期门诊患者数的比例，以及入院8h内完成疼痛程度评估的住院患者例类占住院患者总例数的比例',
            'calculation_formula': '门诊疼痛评估规范率 = (疼痛门诊患者例数 ÷ 同期疼痛门诊患者总例数) × 100%；住院患者入院8h内评估规范率 = (入院8h内完成疼痛程度评估的住院患者例数 ÷ 住院患者总例数) × 100%',
            'numerator_description': '疼痛门诊患者或入院8h内完成疼痛程度评估的住院患者例数',
            'denominator_description': '同期疼痛门诊或住院患者总例数',
            'data_source': '医院填报',
            'unit': '%',
            'target_value': None,
            'frequency': '月度',
            'category_id': category_ids['B']
        }
        # 在实际脚本中继续添加其他指标...
    ]
    
    # 导入指标数据
    indicators_count = 0
    for indicator_data in indicators_data:
        # 检查指标是否已存在
        existing = Indicator.query.filter_by(code=indicator_data['code']).first()
        if not existing:
            indicator = Indicator(**indicator_data)
            db.session.add(indicator)
            indicators_count += 1
    
    # 提交更改
    db.session.commit()
    
    print(f"成功导入 {indicators_count} 个医疗质量指标")
    print("为简洁起见，本脚本仅导入了前9个指标，完整导入请扩展indicators_data列表")

if __name__ == '__main__':
    import_indicators() 