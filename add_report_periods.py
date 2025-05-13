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

def add_report_periods():
    """添加各种类型的报告周期"""
    
    # 创建应用上下文
    app = create_app()
    with app.app_context():
        # 添加2023年、2024年和2025年的报告周期
        years = [2023, 2024, 2025]
        added_count = 0
        
        for year in years:
            # 1. 添加月度报告周期 (12个月)
            for month in range(1, 13):
                # 根据月份确定天数
                if month in [4, 6, 9, 11]:  # 4,6,9,11月有30天
                    days_in_month = 30
                elif month == 2:  # 2月特殊处理闰年
                    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                        days_in_month = 29  # 闰年
                    else:
                        days_in_month = 28  # 平年
                else:
                    days_in_month = 31
                
                # 设置起止日期
                start_date = date(year, month, 1)
                end_date = date(year, month, days_in_month)
                name = f"{year}年{month}月"
                
                # 检查是否已存在
                if not ReportPeriod.query.filter_by(year=year, month=month, quarter=None).first():
                    period = ReportPeriod(
                        year=year,
                        month=month,
                        start_date=start_date,
                        end_date=end_date,
                        name=name
                    )
                    db.session.add(period)
                    added_count += 1
            
            # 2. 添加季度报告周期 (4个季度)
            for quarter in range(1, 5):
                # 确定季度的起止月份
                start_month = (quarter - 1) * 3 + 1
                end_month = quarter * 3
                
                # 设置起止日期
                start_date = date(year, start_month, 1)
                
                # 确定结束月的最后一天
                if end_month in [4, 6, 9, 11]:
                    end_day = 30
                elif end_month == 2:
                    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                        end_day = 29
                    else:
                        end_day = 28
                else:
                    end_day = 31
                
                end_date = date(year, end_month, end_day)
                name = f"{year}年第{quarter}季度"
                
                # 检查是否已存在
                if not ReportPeriod.query.filter_by(year=year, quarter=quarter, month=None).first():
                    period = ReportPeriod(
                        year=year,
                        quarter=quarter,
                        start_date=start_date,
                        end_date=end_date,
                        name=name
                    )
                    db.session.add(period)
                    added_count += 1
            
            # 3. 添加半年报告周期 (上半年和下半年)
            # 上半年
            start_date = date(year, 1, 1)
            end_date = date(year, 6, 30)
            name = f"{year}年上半年"
            
            if not ReportPeriod.query.filter_by(name=name).first():
                period = ReportPeriod(
                    year=year,
                    start_date=start_date,
                    end_date=end_date,
                    name=name
                )
                db.session.add(period)
                added_count += 1
            
            # 下半年
            start_date = date(year, 7, 1)
            end_date = date(year, 12, 31)
            name = f"{year}年下半年"
            
            if not ReportPeriod.query.filter_by(name=name).first():
                period = ReportPeriod(
                    year=year,
                    start_date=start_date,
                    end_date=end_date,
                    name=name
                )
                db.session.add(period)
                added_count += 1
            
            # 4. 添加年度报告周期
            start_date = date(year, 1, 1)
            end_date = date(year, 12, 31)
            name = f"{year}年"
            
            if not ReportPeriod.query.filter_by(year=year, quarter=None, month=None, name=name).first():
                period = ReportPeriod(
                    year=year,
                    start_date=start_date,
                    end_date=end_date,
                    name=name
                )
                db.session.add(period)
                added_count += 1
        
        # 5. 添加几个非正式报告周期（任意月份组合）示例
        # 例如：某个特定时段，如疫情期间等
        special_periods = [
            {
                'name': '2023年第一季末至第二季初',
                'year': 2023,
                'start_date': date(2023, 3, 15),
                'end_date': date(2023, 4, 15)
            },
            {
                'name': '2023年夏季专项报告',
                'year': 2023,
                'start_date': date(2023, 6, 1),
                'end_date': date(2023, 8, 31)
            },
            {
                'name': '2023年年末专项检查',
                'year': 2023,
                'start_date': date(2023, 11, 15),
                'end_date': date(2023, 12, 31)
            },
            {
                'name': '2024年第一季专项报告',
                'year': 2024,
                'start_date': date(2024, 1, 15),
                'end_date': date(2024, 3, 15)
            },
            {
                'name': '2025年第一季专项报告',
                'year': 2025,
                'start_date': date(2025, 1, 15),
                'end_date': date(2025, 3, 15)
            }
        ]
        
        for period_data in special_periods:
            if not ReportPeriod.query.filter_by(name=period_data['name']).first():
                period = ReportPeriod(
                    year=period_data['year'],
                    start_date=period_data['start_date'],
                    end_date=period_data['end_date'],
                    name=period_data['name']
                )
                db.session.add(period)
                added_count += 1
        
        # 提交到数据库
        if added_count > 0:
            db.session.commit()
            print(f"成功添加 {added_count} 个报告周期")
        else:
            print("没有新报告周期需要添加")
        
        # 显示当前所有报告周期
        all_periods = ReportPeriod.query.order_by(ReportPeriod.year.desc(), 
                                                 ReportPeriod.quarter.desc(), 
                                                 ReportPeriod.month.desc()).all()
        print(f"\n当前报告周期总数: {len(all_periods)}")
        
if __name__ == "__main__":
    add_report_periods() 