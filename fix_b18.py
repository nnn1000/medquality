#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

def fix_b18():
    """修复B18指标的详细信息"""
    
    print("开始修复B18指标数据...")
    
    # 连接到数据库
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    try:
        # 开始事务
        cursor.execute('BEGIN TRANSACTION')
        
        # 查询B18指标ID
        cursor.execute('SELECT id FROM indicators WHERE code = ?', ('B18',))
        b18_id = cursor.fetchone()
        
        if b18_id:
            # 更新B18指标信息为正确的数据
            cursor.execute('''
                UPDATE indicators 
                SET name = '危急值报告及时率',
                    definition = '考核年度医院的检验项目危急值报告、处置时间符合规定报告制度要求的检验项目数量。',
                    calculation_formula = '危急值报告及时率 = (危急值通报时间符合规定时间的检验项目数 ÷ 同期需要危急值通报的检验项目总数) × 100%',
                    numerator_description = '危急值通报时间符合规定时间的检验项目数',
                    denominator_description = '同期需要危急值通报的检验项目总数',
                    data_source = '医院填报',
                    unit = '%',
                    frequency = '月度'
                WHERE id = ?
            ''', (b18_id[0],))
            
            print(f"已更新B18指标为'危急值报告及时率'")
        else:
            print("警告: 未找到B18指标")
            
            # 插入新的B18指标
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
                FROM indicators WHERE code = 'B15' LIMIT 1
            ''')
            print("已插入新的B18指标: 危急值报告及时率")
        
        # 提交事务
        conn.commit()
        print("B18指标数据修复完成!")
        
    except Exception as e:
        # 发生错误时回滚事务
        conn.rollback()
        print(f"错误: {str(e)}")
    finally:
        # 关闭连接
        conn.close()

if __name__ == "__main__":
    fix_b18() 