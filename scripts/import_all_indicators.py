#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
导入《东莞市全面提升医疗质量操作手册（2024版）》中40个医疗质量指标到数据库
此脚本会调用三个分部导入脚本，完成所有指标的导入
"""

import os
import sys
import importlib.util
from flask import current_app
from app import create_app, db
from app.models.indicator import Indicator, IndicatorCategory

def import_module_from_file(file_path):
    """从文件路径动态导入Python模块"""
    module_name = os.path.basename(file_path).replace('.py', '')
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def import_all_indicators():
    """导入所有医疗质量指标"""
    # 创建应用上下文
    app = create_app()
    with app.app_context():
        # 检查指标类别是否已存在，如果不存在则创建
        categories = {
            'A': '急诊和日间医疗质量', 
            'B': '医疗行为质量',
            'C': '结果质量',
            'D': '病历质量'
        }
        
        category_ids = {}
        for code, name in categories.items():
            cat = IndicatorCategory.query.filter_by(name=name).first()
            if not cat:
                cat = IndicatorCategory(name=name)
                db.session.add(cat)
                db.session.commit()
            category_ids[code] = cat.id
        
        # 导入主要指标
        try:
            # 调用第一部分指标导入脚本
            from scripts.import_indicators import import_base_indicators
            import_base_indicators()
            print("成功导入第一部分指标")
            
            # 调用第二部分指标导入脚本
            from scripts.import_indicators_part2 import import_more_indicators
            import_more_indicators()
            print("成功导入第二部分指标")
            
            # 调用第三部分指标导入脚本
            from scripts.import_indicators_part3 import import_final_indicators
            import_final_indicators()
            print("成功导入第三部分指标")

            # 调用子指标导入脚本 - 病历记录及时性子指标
            from scripts.import_missing_indicators import import_sub_indicators
            import_sub_indicators()
            print("成功导入病历记录及时性子指标")
            
            # 调用更多子指标导入脚本
            from scripts.import_missing_indicators_more import import_more_sub_indicators
            import_more_sub_indicators()
            print("成功导入更多子指标")
            
            # 调用早期康复介入率子指标导入脚本
            from scripts.import_missing_indicators_early_rehab import import_early_rehab_sub_indicators
            import_early_rehab_sub_indicators()
            print("成功导入早期康复介入率子指标")
            
            # 调用围术期死亡率子指标导入脚本
            from scripts.import_perioperative_mortality import import_perioperative_mortality_sub_indicators
            import_perioperative_mortality_sub_indicators()
            print("成功导入围术期死亡率子指标")
            
            # 检查总指标数
            indicators_count = Indicator.query.count()
            print(f"数据库中共有 {indicators_count} 个指标")
            print("所有指标导入完成！")
            
        except ImportError as e:
            print(f"导入指标失败: {e}")
            return False
            
        except Exception as e:
            print(f"导入过程中出错: {e}")
            return False
            
        return True

if __name__ == '__main__':
    # 添加项目根目录到系统路径，确保能够导入app包
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    success = import_all_indicators()
    if success:
        print("指标导入成功完成")
    else:
        print("指标导入失败") 