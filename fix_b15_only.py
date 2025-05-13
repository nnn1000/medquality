#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

def fix_b15_only():
    """将B15修正为危急值报告及时率，删除所有B15子指标，并删除B18"""
    print("开始修正B15及相关子指标...")
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    try:
        cursor.execute('BEGIN TRANSACTION')
        # 1. 更新B15为危急值报告及时率
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
            WHERE code = 'B15'
        ''')
        print("已将B15修正为危急值报告及时率")
        # 2. 删除所有B15子指标
        cursor.execute('DELETE FROM indicators WHERE code LIKE "B15.%"')
        print("已删除所有B15子指标")
        # 3. 删除B18（如有）
        cursor.execute('DELETE FROM indicators WHERE code = "B18"')
        print("已删除B18（如存在）")
        conn.commit()
        print("修正完成！")
    except Exception as e:
        conn.rollback()
        print(f"错误: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    fix_b15_only() 