#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import sqlite3
from datetime import datetime

def check_indicators():
    """检查指标表中同时包含%的指标导向和单位"""
    
    # 连接数据库
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    try:
        # 查找所有指标
        cursor.execute('SELECT id, code, name, target_value, unit FROM indicators ORDER BY code')
        indicators = cursor.fetchall()
        
        print(f"指标总数: {len(indicators)}")
        print("\n可能存在问题的指标:")
        
        # 检查可能存在问题的指标
        for row in indicators:
            id, code, name, target_value, unit = row
            
            # 检查导向值中是否包含单位
            if unit and target_value and unit in target_value:
                print(f"ID: {id}, 编码: {code}, 名称: {name}")
                print(f"  指标导向: {target_value}")
                print(f"  单位: {unit}")
                print()
        
    except Exception as e:
        print(f"错误: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_indicators() 