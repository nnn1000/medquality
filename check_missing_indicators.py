#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import create_app, db
from app.models.indicator import Indicator, IndicatorCategory

# 创建应用上下文
app = create_app()
app.app_context().push()

# 应该有的所有指标代码
all_codes = [
    'A01', 'A02', 'A03', 'A04', 'A05', 'A06',  # 急诊和日间医疗质量（6个）
    'B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B09', 'B10', 
    'B11', 'B12', 'B13', 'B14', 'B15', 'B16', 'B17', 'B18', 'B19',  # 医疗行为质量（19个）
    'C01', 'C02', 'C03', 'C04', 'C05', 'C06', 'C07', 'C08', 'C09', 'C10', 'C11',  # 结果质量（11个）
    'D01', 'D02', 'D03', 'D04'  # 病历质量（4个）
]

# 获取已有指标代码
existing_codes = [indicator.code for indicator in Indicator.query.all()]

# 找出缺失的指标
missing_codes = [code for code in all_codes if code not in existing_codes]

# 输出结果
print(f"总应有指标数: {len(all_codes)}")
print(f"已导入指标数: {len(existing_codes)}")
print(f"缺失指标数: {len(missing_codes)}")

if missing_codes:
    print("缺失的指标代码:")
    for code in missing_codes:
        print(f"- {code}")
else:
    print("没有缺失的指标!")

# 按类别统计
categories = IndicatorCategory.query.all()
print("\n各类别指标统计:")
for category in categories:
    indicators = Indicator.query.filter_by(category_id=category.id).all()
    codes = [i.code for i in indicators]
    print(f"{category.name}: {len(indicators)}个指标")
    
    # 检查每个类别应有的数量是否正确
    if category.name == '急诊和日间医疗质量':
        expected = 6
    elif category.name == '医疗行为质量':
        expected = 19
    elif category.name == '结果质量':
        expected = 11
    elif category.name == '病历质量':
        expected = 4
    else:
        expected = 0
        
    if len(indicators) != expected:
        print(f"  警告: 应该有{expected}个指标，实际有{len(indicators)}个")
        
        # 找出该类别缺失的指标
        prefix = category.name[0]  # 使用类别名的第一个字（中文）
        if prefix == '急':
            prefix = 'A'
        elif prefix == '医':
            prefix = 'B'
        elif prefix == '结':
            prefix = 'C'
        elif prefix == '病':
            prefix = 'D'
            
        expected_codes = [code for code in all_codes if code.startswith(prefix)]
        missing_in_category = [code for code in expected_codes if code not in codes]
        if missing_in_category:
            print(f"  类别'{category.name}'缺失的指标: {', '.join(missing_in_category)}") 