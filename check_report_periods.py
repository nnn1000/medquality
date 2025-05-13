#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# 添加项目根目录到系统路径，确保能够导入app包
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from flask import current_app
from app import create_app, db
from app.models.report_period import ReportPeriod

def check_report_periods():
    """检查报告周期表中的数据"""
    
    # 创建应用上下文
    app = create_app()
    with app.app_context():
        # 获取所有报告周期记录
        periods = ReportPeriod.query.order_by(ReportPeriod.year.desc(), 
                                             ReportPeriod.quarter.desc(), 
                                             ReportPeriod.month.desc()).all()
        
        print(f"报告周期总数: {len(periods)}")
        
        if periods:
            print("\n报告周期列表:")
            for period in periods:
                print(f"ID: {period.id}, 名称: {period.name}, 起止日期: {period.start_date} - {period.end_date}")
        else:
            print("\n报告周期表中没有数据。")
            
if __name__ == "__main__":
    check_report_periods() 