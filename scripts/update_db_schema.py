#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import sqlite3

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def update_db_schema():
    """更新数据库表结构"""
    
    print("开始更新数据库表结构...")
    
    # 连接数据库
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    try:
        # 检查indicator_categories表结构
        cursor.execute("PRAGMA table_info(indicator_categories)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        # 添加缺失的列
        if 'description' not in column_names:
            print("添加description列到indicator_categories表...")
            cursor.execute("ALTER TABLE indicator_categories ADD COLUMN description TEXT")
        
        # 检查indicators表结构
        cursor.execute("PRAGMA table_info(indicators)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        # 添加缺失的列
        missing_columns = {
            'definition': 'TEXT',
            'numerator_description': 'TEXT',
            'denominator_description': 'TEXT',
            'calculation_formula': 'TEXT',
            'data_source': 'VARCHAR(256)',
            'target_value': 'FLOAT',
            'unit': 'VARCHAR(32)',
            'frequency': 'VARCHAR(32)'
        }
        
        for col_name, col_type in missing_columns.items():
            if col_name not in column_names:
                print(f"添加{col_name}列到indicators表...")
                cursor.execute(f"ALTER TABLE indicators ADD COLUMN {col_name} {col_type}")
        
        # 提交更改
        conn.commit()
        print("数据库表结构更新完成！")
        
    except Exception as e:
        print(f"更新数据库表结构时出错: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    update_db_schema() 