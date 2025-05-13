#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import sqlite3
import re

# 连接到数据库
conn = sqlite3.connect('instance/medquality.db')
cursor = conn.cursor()

# 查询所有指标
cursor.execute('SELECT code, name FROM indicators ORDER BY code')
indicators = cursor.fetchall()

# 按照数字顺序重新排序指标
def numeric_sort_key(item):
    code = item[0]
    # 检查是否包含小数点
    if '.' in code:
        main_part, sub_part = code.split('.', 1)
        # 返回主部分和子部分的数字值用于排序
        # 例如对于C11.2，返回('C11', 2.0)，确保C11.2排在C11.14之前
        return (main_part, float(sub_part))
    else:
        # 如果没有小数点，子部分视为0
        return (code, 0.0)

# 使用自定义排序函数排序
indicators.sort(key=numeric_sort_key)

# 统计指标数量
total_count = len(indicators)
main_indicators = [ind for ind in indicators if "." not in ind[0]]
sub_indicators = [ind for ind in indicators if "." in ind[0]]

main_count = len(main_indicators)
sub_count = len(sub_indicators)

print(f"总指标数量: {total_count}")
print(f"主指标数量: {main_count}")
print(f"子指标数量: {sub_count}")

# 显示所有子指标
print("\n所有子指标:")
for code, name in sub_indicators:
    print(f"{code}: {name}")

# 根据前缀进行分组统计
prefix_counts = {}
for code, _ in sub_indicators:
    prefix = code.split('.')[0]
    if prefix in prefix_counts:
        prefix_counts[prefix] += 1
    else:
        prefix_counts[prefix] = 1

print("\n各指标子指标数量:")
# 排序前缀字典的键，确保按照C1, C2, C10这样的顺序排序而不是C1, C10, C2
sorted_prefixes = sorted(prefix_counts.keys(), key=lambda x: (x[0], int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 0))

for prefix in sorted_prefixes:
    count = prefix_counts[prefix]
    cursor.execute('SELECT name FROM indicators WHERE code = ?', (prefix,))
    result = cursor.fetchone()
    name = result[0] if result else "未知"
    print(f"{prefix} ({name}): {count}个子指标")

# 关闭连接
conn.close() 