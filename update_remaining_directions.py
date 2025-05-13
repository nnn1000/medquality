#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import sqlite3
from datetime import datetime

def update_remaining_directions():
    """更新剩余未设置的指标导向"""
    
    print("开始更新剩余指标导向信息...")
    
    # 连接数据库
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    # 剩余指标导向数据
    remaining_directions = {
        'B03.1': "逐步提高",    # 门诊疼痛评估规范率
        'B03.2': "逐步提高",    # 住院患者入院8h内评估规范率
        'B11': "逐步规范",      # 住院患者静脉输液规范使用率
        'B15': "逐步提高",      # 早期康复介入率
        'C06': "逐步降低",      # 非计划重返手术室再手术率
        'C07.1': "逐步降低",    # 手术当日围术期死亡率
        'C07.2': "逐步降低",    # 术后24小时围术期死亡率
        'C07.3': "逐步降低",    # 术后48小时围术期死亡率
        'C11': "逐步降低",      # 住院患者手术术后获得性指标发生率
        'D03': "逐步提高",      # 病案首页主要诊断编码正确率
        'D04': "逐步提高"       # 病历记录及时性
    }
    
    # 更新指标导向
    updated_count = 0
    for code, direction in remaining_directions.items():
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
    update_remaining_directions() 