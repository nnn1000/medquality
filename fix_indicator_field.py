#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import sqlite3
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

def fix_target_value_field():
    """修复indicators表的target_value字段类型（从Float改为String）"""
    
    print("开始修复数据库字段类型...")
    
    # 连接数据库
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    try:
        # 输出当前表结构
        print("当前表结构:")
        cursor.execute('PRAGMA table_info(indicators)')
        for col in cursor.fetchall():
            print(f"  {col[1]} ({col[2]})")
        
        # 1. 备份现有数据
        print("备份现有指标数据...")
        cursor.execute('SELECT * FROM indicators')
        indicators_data = cursor.fetchall()
        print(f"备份了 {len(indicators_data)} 条记录")
        
        # 获取列名
        cursor.execute('PRAGMA table_info(indicators)')
        columns_info = cursor.fetchall()
        column_names = [col[1] for col in columns_info]
        print(f"列名: {column_names}")
        
        # 2. 创建新表（相同结构但target_value是TEXT类型）
        print("创建新表结构...")
        create_table_sql = '''
        CREATE TABLE indicators_new (
            id INTEGER PRIMARY KEY,
            code VARCHAR(32) UNIQUE NOT NULL,
            name VARCHAR(128) NOT NULL,
            definition TEXT,
            numerator_description TEXT,
            denominator_description TEXT,
            calculation_formula TEXT,
            data_source VARCHAR(256),
            target_value TEXT,
            unit VARCHAR(32),
            frequency VARCHAR(32),
            category_id INTEGER NOT NULL,
            created_at DATETIME,
            FOREIGN KEY (category_id) REFERENCES indicator_categories (id)
        )
        '''
        cursor.execute(create_table_sql)
        print("新表创建成功")
        
        # 3. 复制数据到新表
        print("复制数据到新表结构...")
        count = 0
        for row in indicators_data:
            # 构建INSERT语句
            placeholders = ','.join(['?' for _ in range(len(row))])
            insert_sql = f'INSERT INTO indicators_new VALUES ({placeholders})'
            
            # 转换target_value（如果为None则保持None，否则转为字符串）
            row_list = list(row)
            target_value_index = column_names.index('target_value')
            if row_list[target_value_index] is not None:
                row_list[target_value_index] = str(row_list[target_value_index])
            
            cursor.execute(insert_sql, row_list)
            count += 1
        
        print(f"复制了 {count} 条记录")
        
        # 4. 删除旧表
        print("替换旧表...")
        cursor.execute('DROP TABLE indicators')
        print("旧表已删除")
        
        # 5. 重命名新表
        cursor.execute('ALTER TABLE indicators_new RENAME TO indicators')
        print("新表已重命名")
        
        # 验证新表结构
        print("新表结构:")
        cursor.execute('PRAGMA table_info(indicators)')
        for col in cursor.fetchall():
            print(f"  {col[1]} ({col[2]})")
        
        # 6. 提交更改
        conn.commit()
        print("数据库表结构修复完成！")
        
    except Exception as e:
        conn.rollback()
        print(f"错误: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_target_value_field() 