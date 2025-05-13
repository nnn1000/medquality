#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from datetime import date, datetime

# 添加项目根目录到系统路径，确保能够导入app包
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from flask import current_app
from app import create_app, db
from app.models.report_period import ReportPeriod
from app.models.hospital import Hospital
from app.models.data import Result
from app.services.report_generator import ReportGenerator

def test_report_generation():
    """测试报表生成功能"""
    
    # 创建应用上下文
    app = create_app()
    with app.app_context():
        print("\n============ 测试报表生成功能 ============")
        
        # 获取第一个有结果数据的期间和医院
        result = Result.query.first()
        
        if not result:
            print("❌ 系统中没有计算结果数据，请先确保有计算结果")
            return
            
        period = ReportPeriod.query.get(result.period_id)
        hospital = Hospital.query.get(result.hospital_id)
        
        print(f"找到计算结果: 指标={result.indicator.code}, 医院={hospital.name}, 期间={period.name}")
        
        # 尝试生成标准报表
        try:
            print(f"\n尝试为 {period.name} 生成标准报表...")
            report_path = ReportGenerator.generate_excel_report(period.id, None, 'standard')
            
            if report_path:
                print(f"✅ 报表生成成功: {report_path}")
                print(f"报表文件大小: {os.path.getsize(report_path) / 1024:.1f} KB")
            else:
                print("❌ 报表生成失败")
                
        except Exception as e:
            print(f"❌ 报表生成出错: {str(e)}")
            import traceback
            traceback.print_exc()
            
        # 尝试生成汇总报表
        try:
            print(f"\n尝试为 {period.name} 生成汇总报表...")
            report_path = ReportGenerator.generate_excel_report(period.id, None, 'summary')
            
            if report_path:
                print(f"✅ 汇总报表生成成功: {report_path}")
                print(f"汇总报表文件大小: {os.path.getsize(report_path) / 1024:.1f} KB")
            else:
                print("❌ 汇总报表生成失败")
                
        except Exception as e:
            print(f"❌ 汇总报表生成出错: {str(e)}")
            import traceback
            traceback.print_exc()
            
        print("\n============ 报表测试完成 ============")
        
if __name__ == "__main__":
    test_report_generation() 