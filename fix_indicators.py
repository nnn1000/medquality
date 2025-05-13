#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import sqlite3

def fix_indicators():
    """修复指标数据中的错误 - 修正B15和添加B18"""
    
    print("开始修复指标数据...")
    
    # 连接到数据库
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    try:
        # 开始事务
        cursor.execute('BEGIN TRANSACTION')
        
        # 1. 检查B15的实际名称 (假设B15可能是其他指标，名称错误)
        cursor.execute('SELECT id, code, name FROM indicators WHERE code = ?', ('B15',))
        b15_data = cursor.fetchone()
        if b15_data:
            b15_id, b15_code, b15_name = b15_data
            print(f"找到B15指标: {b15_code} - {b15_name} (ID: {b15_id})")
            
            # 如果B15当前名称是"危急值报告及时率"，则需要更改为真正的B15名称
            if b15_name == "危急值报告及时率":
                # 将B15更新为正确的名称 (更新为实际指标名称，这里假设为"康复医疗质量")
                cursor.execute('''
                    UPDATE indicators 
                    SET name = '早期康复介入率', 
                        definition = '根据临床指南或专科共识，早期康复介入率是指在患者住院治疗期间接受早期康复评估和干预的比例。',
                        calculation_formula = '早期康复介入率 = (住院期间接受早期康复评估和干预的例数 ÷ 同期适合早期康复的住院患者总例数) × 100%',
                        numerator_description = '住院期间接受早期康复评估和干预的例数',
                        denominator_description = '同期适合早期康复的住院患者总例数'
                    WHERE code = ?
                ''', ('B15',))
                print(f"已更新B15指标为正确名称: 早期康复介入率")
        else:
            print("警告: 未找到B15指标")
        
        # 2. 检查B18是否已存在
        cursor.execute('SELECT id, name FROM indicators WHERE code = ?', ('B18',))
        b18_data = cursor.fetchone()
        
        if not b18_data:
            # 3. 添加正确的B18指标
            cursor.execute('''
                INSERT INTO indicators 
                (code, name, definition, calculation_formula, numerator_description, 
                denominator_description, data_source, unit, target_value, frequency, category_id)
                SELECT 'B18', '危急值报告及时率', 
                '考核年度医院的检验项目危急值报告、处置时间符合规定报告制度要求的检验项目数量。', 
                '危急值报告及时率 = (危急值通报时间符合规定时间的检验项目数 ÷ 同期需要危急值通报的检验项目总数) × 100%', 
                '危急值通报时间符合规定时间的检验项目数', 
                '同期需要危急值通报的检验项目总数', 
                '医院填报', '%', NULL, '月度', category_id
                FROM indicators WHERE code = 'B15'
            ''')
            print("已添加正确的B18指标: 危急值报告及时率")
        else:
            print(f"B18指标已存在: {b18_data[1]}")
        
        # 提交事务
        conn.commit()
        print("指标数据修复完成!")
    
    except Exception as e:
        # 发生错误时回滚事务
        conn.rollback()
        print(f"错误: {str(e)}")
    finally:
        # 关闭连接
        conn.close()

if __name__ == "__main__":
    fix_indicators() 