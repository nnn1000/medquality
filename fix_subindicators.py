#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import sqlite3

def fix_subindicators():
    """检查和修复B15和B18的子指标数据"""
    
    print("开始检查子指标数据...")
    
    # 连接到数据库
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    try:
        # 开始事务
        cursor.execute('BEGIN TRANSACTION')
        
        # 1. 检查B15子指标
        cursor.execute('SELECT id, code, name FROM indicators WHERE code LIKE "B15.%" ORDER BY code')
        b15_subs = cursor.fetchall()
        
        if b15_subs:
            print(f"找到 {len(b15_subs)} 个B15子指标:")
            for id, code, name in b15_subs:
                print(f"  - {code}: {name} (ID: {id})")
                
            # 这些B15子指标是正确的，只是父指标名称错误，我们已经修复了父指标名称
            print("父指标B15已更正为'早期康复介入率'，这些子指标属于该指标，保留不变。")
        else:
            print("未找到B15的子指标。")
        
        # 2. 检查是否有错误的B18子指标
        cursor.execute('SELECT id, code, name FROM indicators WHERE code LIKE "B18.%" ORDER BY code')
        b18_subs = cursor.fetchall()
        
        if b18_subs:
            print(f"警告: 找到 {len(b18_subs)} 个B18子指标:")
            for id, code, name in b18_subs:
                print(f"  - {code}: {name} (ID: {id})")
                
            # 根据您的说明，B18不应该有子指标，可以考虑删除它们
            # 但这可能会影响已经录入的数据，所以需要谨慎操作
            delete_confirm = input("B18指标不应该有子指标，是否删除这些子指标？(y/n): ")
            if delete_confirm.lower() == 'y':
                for id, code, name in b18_subs:
                    cursor.execute('DELETE FROM indicators WHERE id = ?', (id,))
                print(f"已删除 {len(b18_subs)} 个错误的B18子指标")
            else:
                print("保留B18子指标，不进行删除操作")
        else:
            print("B18没有子指标，符合预期。")
        
        # 提交事务
        conn.commit()
        print("子指标数据检查完成!")
    
    except Exception as e:
        # 发生错误时回滚事务
        conn.rollback()
        print(f"错误: {str(e)}")
    finally:
        # 关闭连接
        conn.close()

if __name__ == "__main__":
    fix_subindicators() 