#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

# 连接到数据库
conn = sqlite3.connect('instance/medquality.db')
cursor = conn.cursor()

# 查询B18指标的详细信息
cursor.execute('''
    SELECT id, code, name, definition, calculation_formula, 
           numerator_description, denominator_description, 
           data_source, unit, target_value, frequency
    FROM indicators 
    WHERE code = 'B18'
''')

b18_data = cursor.fetchone()

if b18_data:
    print("B18指标详细信息:")
    print(f"ID: {b18_data[0]}")
    print(f"编码: {b18_data[1]}")
    print(f"名称: {b18_data[2]}")
    print(f"定义: {b18_data[3]}")
    print(f"计算公式: {b18_data[4]}")
    print(f"分子描述: {b18_data[5]}")
    print(f"分母描述: {b18_data[6]}")
    print(f"数据来源: {b18_data[7]}")
    print(f"单位: {b18_data[8]}")
    print(f"目标值: {b18_data[9]}")
    print(f"频率: {b18_data[10]}")
else:
    print("未找到B18指标")

# 关闭连接
conn.close() 