#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import sqlite3
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

def update_indicator_directions():
    """更新指标导向信息"""
    
    print("开始更新指标导向信息...")
    
    # 连接数据库
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    # 指标导向数据
    direction_data = {
        # 急诊和日间医疗质量相关指标
        'A01': "逐步降低",
        'A02': "逐步升高",
        'A03': "逐步提高-不低于75%",
        'A04': "监测比较",
        'A05': "监测比较",
        'A06': "监测比较",
        
        # 医疗行为质量相关指标
        'B01': "逐步提高",
        'B02': "逐步提高",
        'B03': "逐步提高",
        'B04': "逐步提高",
        'B05': "逐步提高", 
        'B06': "逐步提高",
        'B07': "逐步提高",
        'B08': "逐步提高",
        'B09': "达到省的要求",
        'B10': "逐步提高",
        'B11.1': "逐步降低",
        'B11.2': "逐步降低",
        'B11.3': "逐步降低",
        'B11.4': "逐步降低",
        'B12': "逐步提高",
        'B13': "逐步提高",
        'B14': "逐步提高",
        'B15.1': "逐步提高",
        'B15.2': "逐步提高",
        'B15.3': "逐步提高",
        'B15.4': "逐步提高",
        'B15.5': "逐步提高",
        'B15.6': "逐步提高",
        'B15.7': "逐步提高",
        'B15.8': "逐步提高",
        'B15.9': "逐步提高",
        'B16': "逐步提高",
        'B17': "逐步提高",
        'B18': "每百出院人次主动报告不良事件年均大于2.5例次",
        'B19': "逐步提高",
        
        # 结果质量相关指标
        'C01': "逐步提高",
        'C02': "逐步降低，≤0.37%",
        'C03': "监测比较",
        'C04': "逐步降低",
        'C05': "逐步降低",
        'C06.1': "逐步降低，三甲评审要求不高于0.18%，高水平医院要求不高于0.5%",
        'C06.2': "逐步降低",
        'C06.3': "逐步降低",
        'C07': "逐步降低，≤0.10%",
        'C08': "逐步提高",
        'C09': "逐步降低",
        'C10': "逐步降低",
        'C11.1': "逐步降低",
        'C11.2': "逐步降低",
        'C11.3': "逐步降低",
        'C11.4': "逐步降低",
        'C11.5': "逐步降低",
        'C11.6': "逐步降低",
        'C11.7': "逐步降低",
        'C11.8': "逐步降低",
        'C11.9': "逐步降低",
        'C11.10': "逐步降低",
        'C11.11': "逐步降低",
        'C11.12': "逐步降低",
        'C11.13': "逐步降低",
        'C11.14': "逐步降低",
        'C11.15': "逐步降低",
        'C11.16': "逐步降低",
        'C11.17': "逐步降低",
        'C11.18': "逐步降低",
        'C11.19': "逐步降低",
        
        # 病历质量相关指标
        'D01': "监测比较",
        'D02': "监测比较",
        'D03.1': "逐步提高",
        'D03.2': "逐步提高",
        'D04.1': "逐步提高",
        'D04.2': "逐步提高",
        'D04.3': "逐步提高",
        'D04.4': "逐步提高"
    }
    
    # 更新指标导向
    updated_count = 0
    for code, direction in direction_data.items():
        # 检查指标是否存在
        cursor.execute("SELECT id FROM indicators WHERE code = ?", (code,))
        indicator = cursor.fetchone()
        
        if indicator:
            indicator_id = indicator[0]
            # 更新指标导向
            cursor.execute(
                "UPDATE indicators SET target_value = ? WHERE id = ?",
                (direction, indicator_id)
            )
            updated_count += 1
            print(f"已更新指标 {code} 的导向为: {direction}")
        else:
            print(f"警告: 未找到指标代码 {code}")
    
    # 提交更改
    conn.commit()
    
    # 检查结果
    cursor.execute("SELECT COUNT(*) FROM indicators WHERE target_value IS NOT NULL")
    with_direction_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM indicators")
    total_count = cursor.fetchone()[0]
    
    print(f"\n更新完成，共更新了 {updated_count} 个指标导向")
    print(f"指标总数: {total_count}")
    print(f"有导向的指标数: {with_direction_count}")
    print(f"无导向的指标数: {total_count - with_direction_count}")
    
    conn.close()

if __name__ == "__main__":
    update_indicator_directions() 