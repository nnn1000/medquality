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

def import_remaining_indicators():
    """导入剩余的医疗质量指标"""
    
    print("开始导入剩余医疗质量指标...")
    
    # 获取指标类别ID
    category_ids = {}
    categories = {
        'A': '急诊和日间医疗质量',
        'B': '医疗行为质量',
        'C': '结果质量',
        'D': '病历质量'
    }
    
    for code, name in categories.items():
        category = IndicatorCategory.query.filter_by(name=name).first()
        if category:
            category_ids[code] = category.id
    
    # 定义剩余指标数据
    indicators_data = [
        # 继续医疗行为质量相关指标
        {
            'code': 'B04',
            'name': '门诊处方审核率',
            'definition': '药品收费前药师审核门诊处方张数占同期门诊处方总数的比例',
            'calculation_formula': '(药品收费前药师审核门诊处方张数 ÷ 同期门诊总处方张数) × 100%',
            'numerator_description': '收费前经药师审核的门诊处方张数',
            'denominator_description': '门诊同期所有处方总数之和',
            'data_source': '医院填报',
            'unit': '%',
            'target_value': None,
            'frequency': '月度',
            'category_id': category_ids['B']
        },
        {
            'code': 'B05',
            'name': '急诊处方审核率',
            'definition': '药品收费前药师审核急诊处方张数占同期急诊处方总数的比例',
            'calculation_formula': '(药品收费前药师审核急诊处方张数 ÷ 同期急诊总处方数) × 100%',
            'numerator_description': '收费前经药师审核的急诊处方张数',
            'denominator_description': '急诊同期所有处方总数之和',
            'data_source': '医院填报',
            'unit': '%',
            'target_value': None,
            'frequency': '月度',
            'category_id': category_ids['B']
        },
        {
            'code': 'B06',
            'name': '住院处方审核率',
            'definition': '药品调配前药师审核住院患者用药医嘱条目数占同期住院患者用药医嘱总条目数的比例',
            'calculation_formula': '(药品调配前药师审核住院患者用药医嘱条目数 ÷ 同期住院患者用药医嘱总条目数) × 100%',
            'numerator_description': '药品调配前由药师审核的住院医嘱条目数',
            'denominator_description': '同期住院患者用药医嘱总条目数',
            'data_source': '医院填报',
            'unit': '%',
            'target_value': None,
            'frequency': '月度',
            'category_id': category_ids['B']
        },
        {
            'code': 'B07',
            'name': '门诊处方审核合格率',
            'definition': '合格的门诊处方张数占同期所有门诊处方总数的比例',
            'calculation_formula': '(合格门诊处方张数 ÷ 同期审核的门诊处方总数) × 100%',
            'numerator_description': '人工审核或由药师维护处方审核规则的前置审方系统审核的合格门诊处方张数',
            'denominator_description': '同期审核的门诊处方总数',
            'data_source': '医院填报',
            'unit': '%',
            'target_value': None,
            'frequency': '月度',
            'category_id': category_ids['B']
        },
        {
            'code': 'B08',
            'name': '急诊处方审核合格率',
            'definition': '合格的急诊处方张数占同期急诊所有处方总数的比例',
            'calculation_formula': '(合格急诊处方张数 ÷ 同期审核的急诊处方总数) × 100%',
            'numerator_description': '人工审核或由药师维护处方审核规则的前置审方系统审核的合格急诊处方张数',
            'denominator_description': '同期审核的急诊处方总数',
            'data_source': '医院填报',
            'unit': '%',
            'target_value': None,
            'frequency': '月度',
            'category_id': category_ids['B']
        },
        {
            'code': 'B09',
            'name': '基本药物采购品种数占比',
            'definition': '医院采购国家基本药物品规数占医院同期采购药物品规总数的比例',
            'calculation_formula': '(医院采购的国家基本药物品规数 ÷ 医院同期采购药物品规总数) × 100%',
            'numerator_description': '按照《国家基本药物目录（2018年版）》中的药品通用名、剂型、规格进行统计',
            'denominator_description': '按照同期医院使用药品品种总数进行统计，即同期医院使用的全部药品品种总数',
            'data_source': '医院填报',
            'unit': '%',
            'target_value': None,
            'frequency': '季度',
            'category_id': category_ids['B']
        },
        {
            'code': 'B10',
            'name': '住院处方审核合格率',
            'definition': '合格的住院医嘱条目数占同期住院医嘱总条目数的比例',
            'calculation_formula': '(药师点评合格的住院患者医嘱条目数 ÷ 同期药师点评的总医嘱条目数) × 100%',
            'numerator_description': '药师处方点评工作中合格的住院医嘱条目数',
            'denominator_description': '同期药师点评的总的医嘱条目数',
            'data_source': '医院填报',
            'unit': '%',
            'target_value': None,
            'frequency': '月度',
            'category_id': category_ids['B']
        },
        {
            'code': 'B11',
            'name': '住院患者静脉输液规范使用率',
            'definition': '使用静脉输液的住院患者人数占同期住院患者总人数的比例',
            'calculation_formula': '(使用静脉输液的出院患者人数 ÷ 同期出院患者总人次数) × 100%',
            'numerator_description': '静脉输液的定义为给药途径为静脉滴注、静脉推注和泵入且输注液体量为50ml以上，按出院人次计算',
            'denominator_description': '同期出院患者总人次数，未用药的出院患者也纳入统计',
            'data_source': '医院填报',
            'unit': '%',
            'target_value': None,
            'frequency': '月度',
            'category_id': category_ids['B']
        },
        {
            'code': 'B12',
            'name': '住院患者静脉输液平均每床日使用数量',
            'definition': '考核住院患者平均每床日使用静脉输液的数量（袋/瓶）',
            'calculation_formula': '静脉输液使用总袋/瓶数 ÷ 同期出院患者累计总床日数',
            'numerator_description': '给药途径为静脉滴注、静脉推注和泵入的50ml以上大输液消耗数量，单位为瓶、袋',
            'denominator_description': '同期所有出院患者累计总床日数',
            'data_source': '医院填报',
            'unit': '袋/瓶',
            'target_value': None,
            'frequency': '月度',
            'category_id': category_ids['B']
        },
        {
            'code': 'B13',
            'name': '住院患者静脉输液平均每床日使用体积',
            'definition': '住院患者平均每床日使用静脉输液的体积数（毫升/ml）',
            'calculation_formula': '静脉输液总体积数 ÷ 同期出院患者累计总床日数',
            'numerator_description': '给药途径为静脉滴注、静脉推注和泵入的50ml以上大输液消耗总体积(ml)',
            'denominator_description': '同期所有出院患者累计总床日数',
            'data_source': '医院填报',
            'unit': 'ml',
            'target_value': None,
            'frequency': '月度',
            'category_id': category_ids['B']
        },
        {
            'code': 'B14',
            'name': '住院患者平均使用输液药品品种数量',
            'definition': '考核住院患者平均使用输液药品品种的数量',
            'calculation_formula': '出院患者静脉输液药品品种总数 ÷ 同期出院患者总人次数',
            'numerator_description': '出院患者给药途径为静脉滴注、静脉推注和泵入且输注液体量50ml以上的药品（不含溶媒）累积数量之和，按药品品规数算',
            'denominator_description': '同期出院患者总人次数，未用药的出院患者也纳入统计',
            'data_source': '医院填报',
            'unit': '个数',
            'target_value': None,
            'frequency': '月度',
            'category_id': category_ids['B']
        },
        {
            'code': 'B15',
            'name': '危急值报告及时率',
            'definition': '考核年度医院的检验项目危急值报告、处置时间符合规定报告制度要求的检验项目数量',
            'calculation_formula': '(危急值通报时间符合规定时间的检验项目数 ÷ 同期需要危急值通报的检验项目总数) × 100%',
            'numerator_description': '危急值通报时间符合规定时间的检验项目数',
            'denominator_description': '同期需要危急值通报的检验项目总数',
            'data_source': '医院填报',
            'unit': '%',
            'target_value': None,
            'frequency': '月度',
            'category_id': category_ids['B']
        },
        {
            'code': 'B16',
            'name': '危急值处置及时率',
            'definition': '考核年度医院的检验项目危急值报告、处置时间符合规定报告制度要求的检验项目数量',
            'calculation_formula': '(临床医生在符合规定时间处置的危急值检验项目数 ÷ 同期需要处置的危急值检验项目数) × 100%',
            'numerator_description': '临床医生在符合规定时间处置的危急值检验项目数',
            'denominator_description': '同期需要处置的危急值检验项目数',
            'data_source': '医院填报',
            'unit': '%',
            'target_value': None,
            'frequency': '月度',
            'category_id': category_ids['B']
        },
        # 添加结果质量相关指标和病历质量相关指标略，实际使用时需要扩展完整
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
    print("此脚本为第二部分，包含部分医疗行为质量指标，完整导入请扩展indicators_data列表")

if __name__ == '__main__':
    import_remaining_indicators() 