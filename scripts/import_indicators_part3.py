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

def import_final_indicators():
    """导入结果质量和病历质量相关指标"""
    
    print("开始导入结果质量和病历质量相关指标...")
    
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
    
    # 定义结果质量和病历质量相关指标数据
    indicators_data = [
        # 结果质量相关指标（11个）
        {
            'code': 'C01',
            'name': '医院CMI值',
            'definition': '运用DRG分组器测算产生的CMI值（病例组合指数），主要考核年度医院疾病收治难度',
            'calculation_formula': '参照DRG评价标准计算方法',
            'numerator_description': '医院能力比较',
            'denominator_description': '无',
            'data_source': '国家绩效考核发布数据/广东省事务中心反馈数据',
            'unit': '',
            'target_value': None,
            'frequency': '季度',
            'category_id': category_ids['C']
        },
        {
            'code': 'C02',
            'name': '手术患者住院死亡率',
            'definition': '手术患者住院死亡人数占同期手术患者出院人次的比例',
            'calculation_formula': '(手术患者住院死亡人数 ÷ 同期手术患者出院人次) × 100%',
            'numerator_description': '指住院患者围手术期内的死亡人数',
            'denominator_description': '指同期手术患者出院人次',
            'data_source': '病案首页',
            'unit': '%',
            'target_value': 0.37,
            'frequency': '季度',
            'category_id': category_ids['C']
        },
        {
            'code': 'C03',
            'name': 'ICU患者病死率',
            'definition': 'ICU死亡患者数（包括因不可逆疾病而自动出院的患者）所占同期ICU收治患者总数的比值',
            'calculation_formula': '(ICU死亡患者数（包括因不可逆疾病而自动出院的患者）÷ 同期ICU收治患者总数) × 100%',
            'numerator_description': 'ICU死亡患者数（包括因不可逆疾病而自动出院的患者）',
            'denominator_description': '同期ICU收治患者总数',
            'data_source': '医院重症医学科数据统计',
            'unit': '%',
            'target_value': None,
            'frequency': '月度',
            'category_id': category_ids['C']
        },
        {
            'code': 'C04',
            'name': '手术并发症发生率',
            'definition': '考核择期手术患者发生并发症例数占同期出院的手术患者人数的比例',
            'calculation_formula': '(择期手术患者发生并发症例数 ÷ 同期出院的手术患者人数) × 100%',
            'numerator_description': '手术患者并发症发生例数是指择期手术和择期介入治疗患者并发症发生人数',
            'denominator_description': '同期出院的手术患者人数是指同期出院患者择期手术人数',
            'data_source': '病案首页',
            'unit': '%',
            'target_value': None,
            'frequency': '季度',
            'category_id': category_ids['C']
        },
        {
            'code': 'C05',
            'name': '麻醉并发症发生率',
            'definition': '单位时间内，麻醉患者发生仅与麻醉及麻醉操作相关并发症的例数占同期由麻醉科实施的麻醉例次数的比例',
            'calculation_formula': '(仅与麻醉及麻醉操作相关并发症 ÷ 单位时间内同期由麻醉科实施的麻醉例次数) × 100%',
            'numerator_description': '麻醉患者发生仅与麻醉及麻醉操作相关并发症的例数',
            'denominator_description': '同期由麻醉科实施的麻醉总例次数',
            'data_source': '医院填报',
            'unit': '%',
            'target_value': None,
            'frequency': '季度',
            'category_id': category_ids['C']
        },
        {
            'code': 'C06',
            'name': '非计划重返手术室再手术率',
            'definition': '指手术患者术后非预期重返手术室再次手术例数占同期手术患者手术例数的比例',
            'calculation_formula': '(手术患者术后非预期重返手术室再次手术例数 ÷ 同期手术患者总手术例数) × 100%',
            'numerator_description': '非预期重返手术室再次手术总例数',
            'denominator_description': '同期手术患者总手术例数',
            'data_source': '医院填报',
            'unit': '%',
            'target_value': 0.18,
            'frequency': '季度',
            'category_id': category_ids['C']
        },
        {
            'code': 'C07',
            'name': '围术期死亡率',
            'definition': '住院患者进行开放手术、介入治疗及内（窥）镜下治疗性操作在手术当日、术后24小时和48小时的死亡情况',
            'calculation_formula': '(在手术当日、术后24小时和48小时的手术患者死亡人数 ÷ 同期手术患者总数) × 100%',
            'numerator_description': '围手术期期间死亡的患者人数',
            'denominator_description': '同期手术总例数（次）',
            'data_source': '病案首页',
            'unit': '%',
            'target_value': 0.10,
            'frequency': '季度',
            'category_id': category_ids['C']
        },
        {
            'code': 'C08',
            'name': '恶性肿瘤患者生存时间',
            'definition': '考核年度内符合纳入条件的10个癌种，确诊某肿瘤，经过综合治疗后，生存超过5年以上的患者比例',
            'calculation_formula': '(经过综合治疗后生存超过5年以上的某肿瘤患者数 ÷ 治疗该肿瘤总患者数) × 100%',
            'numerator_description': '确诊某肿瘤，经过综合治疗后生存超过5年的患者数量',
            'denominator_description': '确诊某肿瘤，经经过综合的全部患者数',
            'data_source': '医院填报',
            'unit': '%',
            'target_value': None,
            'frequency': '年度',
            'category_id': category_ids['C']
        },
        {
            'code': 'C09',
            'name': '血管内导管相关血流感染发生率',
            'definition': '使用血管内导管住院患者中新发血管内导管相关血流感染的发病频率',
            'calculation_formula': '(血管内导管相关血流感染例次数 ÷ 同期患者使用血管内导管留置总天数) × 1000‰',
            'numerator_description': '确定时段全院住院患者中同期新发生中央血管导管相关血流感染的例次数',
            'denominator_description': '确定时段全院住院患者同期使用中央血管导管的天数之和',
            'data_source': '医院填报或东莞市医院感染监测信息化平台反馈',
            'unit': '‰',
            'target_value': None,
            'frequency': '季度',
            'category_id': category_ids['C']
        },
        {
            'code': 'C10',
            'name': '患者院内压力性损伤发生率',
            'definition': '单位时间内，住院患者2期及以上院内压力性损伤新发病例数与住院患者总数的比例',
            'calculation_formula': '(2期及以上院内压力性损伤发生例数 ÷ 同期出院患者人次) × 100%',
            'numerator_description': '同期被诊断为2期及以上压力性损伤，深部组织损伤、不可分期、医疗器械相关性压力性损伤、粘膜压力性损伤的患者',
            'denominator_description': '所有办理出院手续的患者',
            'data_source': '医院填报',
            'unit': '%',
            'target_value': None,
            'frequency': '季度',
            'category_id': category_ids['C']
        },
        {
            'code': 'C11',
            'name': '住院患者手术术后获得性指标发生率',
            'definition': '重点监测手术患者术后各类并发症发生率',
            'calculation_formula': '(各类术后并发症发生例数 ÷ 同期手术患者出院人次) × 100%',
            'numerator_description': '各类术后并发症发生例数',
            'denominator_description': '同期手术患者出院人次',
            'data_source': '病案首页',
            'unit': '%',
            'target_value': 0.75,
            'frequency': '季度',
            'category_id': category_ids['C']
        },
        
        # 病历质量相关指标（4个）
        {
            'code': 'D01',
            'name': '门诊病历电子化比例',
            'definition': '考核单位时间内门（急）诊患者使用电子化病历记录的人次数占门（急）诊患者就诊总人次的比例',
            'calculation_formula': '(门诊患者使用电子化病历记录的人次数 ÷ 同期门诊患者人次数) × 100%',
            'numerator_description': '门诊患者使用电子化病历记录的人次数，即患者在门诊就诊后，医生使用门诊电子病历系统记录病历的患者人次数',
            'denominator_description': '同期门诊患者人次数，即此同期就诊患者总人次，一个人多次就诊算多次，统计单位以就诊人次计算',
            'data_source': '医院填报',
            'unit': '%',
            'target_value': None,
            'frequency': '季度',
            'category_id': category_ids['D']
        },
        {
            'code': 'D02',
            'name': '门诊结构化病历使用比例',
            'definition': '考核单位时间内门（急）诊患者使用结构化电子病历记录的人次数占门（急）诊患者就诊总人次的比例',
            'calculation_formula': '(门诊患者使用结构化电子病历记录的人次数 ÷ 同期门诊患者人次数) × 100%',
            'numerator_description': '门诊患者使用结构化电子病历记录的人次数，即患者在门诊就诊后，使用门诊电子病历系统记录结构化病历的患者人次数',
            'denominator_description': '同期门诊患者人次数，即此同期就诊患者总人次，一个人多次就诊算多次，统计单位以就诊人次计算',
            'data_source': '医院填报',
            'unit': '%',
            'target_value': None,
            'frequency': '季度',
            'category_id': category_ids['D']
        },
        {
            'code': 'D03',
            'name': '病案首页主要诊断编码正确率',
            'definition': '单位时间内，病案首页中主要诊断编码正确的出院患者病历数占同期出院患者病历总数的比例',
            'calculation_formula': '(病案首页中主要诊断编码正确的出院患者病历数 ÷ 同期出院患者病历总数) × 100%',
            'numerator_description': '病案首页中主要诊断编码正确的出院患者病历数',
            'denominator_description': '单位时间内，医疗机构所有出院患者病历总数',
            'data_source': '医院填报',
            'unit': '%',
            'target_value': None,
            'frequency': '季度',
            'category_id': category_ids['D']
        },
        {
            'code': 'D04',
            'name': '病历记录及时性',
            'definition': '包括入院记录24小时内完成率、手术记录24小时内完成率、出院记录24小时内完成率、病案首页24小时内完成率',
            'calculation_formula': '(各类记录在规定时间内完成的病历数 ÷ 同期相应患者病历总数) × 100%',
            'numerator_description': '各类记录在规定时间内完成的病历数',
            'denominator_description': '同期相应患者病历总数',
            'data_source': '医院填报',
            'unit': '%',
            'target_value': None,
            'frequency': '月度',
            'category_id': category_ids['D']
        }
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
    print("成功完成所有指标导入")

if __name__ == '__main__':
    import_final_indicators() 