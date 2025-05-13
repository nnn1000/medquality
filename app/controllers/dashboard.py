from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.indicator import Indicator, IndicatorCategory
from app.models.hospital import Hospital
from app.models.report_period import ReportPeriod
from app.models.data import RawData, Result
from app.services.calculator import IndicatorCalculator
from app.forms import ReportGenerationForm
from sqlalchemy import func, case
import pandas as pd
import json
import re

# 创建仪表盘蓝图
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def index():
    """显示仪表盘首页"""
    # 获取基本统计信息
    stats = {
        'hospital_count': Hospital.query.count(),
        'indicator_count': Indicator.query.count(),
        'raw_data_count': RawData.query.count(),
        'result_count': Result.query.count()
    }
    
    # 获取最新数据周期
    latest_period = ReportPeriod.query.order_by(
        ReportPeriod.year.desc(), 
        ReportPeriod.quarter.desc(), 
        ReportPeriod.month.desc()
    ).first()
    
    # 获取指标类别分布数据
    category_distribution = db.session.query(
        IndicatorCategory.name, 
        func.count(Indicator.id)
    ).join(
        Indicator, 
        Indicator.category_id == IndicatorCategory.id
    ).group_by(
        IndicatorCategory.name
    ).order_by(
        case(
            (IndicatorCategory.name == '急诊和日间医疗质量', 1),
            (IndicatorCategory.name == '医疗行为质量', 2),
            (IndicatorCategory.name == '结果质量', 3),
            (IndicatorCategory.name == '病历质量', 4)
        )
    ).all()
    
    category_names = [cat[0] for cat in category_distribution]
    category_counts = [cat[1] for cat in category_distribution]
    
    # 获取最近的数据录入
    recent_data = RawData.query.order_by(RawData.submit_time.desc()).limit(5).all()
    
    # 获取最近的计算结果
    recent_results = Result.query.order_by(Result.calculation_time.desc()).limit(5).all()
    
    # 准备图表数据
    chart_data = {
        'category_names': json.dumps(category_names),
        'category_counts': json.dumps(category_counts)
    }
    
    # 获取达标情况统计
    if latest_period:
        # 筛选出最新周期的结果，计算达标率
        achieved_count = Result.query.filter_by(
            period_id=latest_period.id, 
            target_achieved=True
        ).count()
        
        total_count = Result.query.filter_by(
            period_id=latest_period.id
        ).count()
        
        achievement_rate = (achieved_count / total_count * 100) if total_count > 0 else 0
        
        # 准备达标率数据
        chart_data['achievement_rate'] = json.dumps(round(achievement_rate, 2))
    else:
        chart_data['achievement_rate'] = json.dumps(0)
    
    return render_template(
        'dashboard/index.html',
        title='全面提升医疗质量管理系统',
        stats=stats,
        latest_period=latest_period,
        recent_data=recent_data,
        recent_results=recent_results,
        chart_data=chart_data
    )

@dashboard_bp.route('/stats')
@login_required
def stats():
    """显示详细统计信息页面"""
    # 获取筛选参数
    period_id = request.args.get('period_id', type=int)
    hospital_id = request.args.get('hospital_id', type=int)
    category_id = request.args.get('category_id', type=int)
    
    # 准备筛选选项
    periods = ReportPeriod.query.order_by(
        ReportPeriod.year.desc(), 
        ReportPeriod.quarter.desc(), 
        ReportPeriod.month.desc()
    ).all()
    
    hospitals = Hospital.query.order_by(Hospital.name).all()
    categories = IndicatorCategory.query.order_by(
        case(
            (IndicatorCategory.name == '急诊和日间医疗质量', 1),
            (IndicatorCategory.name == '医疗行为质量', 2),
            (IndicatorCategory.name == '结果质量', 3),
            (IndicatorCategory.name == '病历质量', 4)
        )
    ).all()
    
    # 默认使用最新周期
    if not period_id and periods:
        period_id = periods[0].id
    
    # 如果已选定周期，获取结果数据
    if period_id:
        # 使用计算服务获取数据框
        df = IndicatorCalculator.get_results_dataframe(period_id, hospital_id, category_id)
        
        # 转换为HTML表格
        if not df.empty:
            # 自定义排序函数，确保指标按照数字顺序排序
            def numeric_sort_key(code_str):
                # 检查是否包含小数点
                if '.' in code_str:
                    main_part, sub_part = code_str.split('.', 1)
                    # 返回主部分和子部分的数字值用于排序
                    # 尝试提取主部分的数字
                    main_num = re.search(r'\d+', main_part)
                    if main_num:
                        main_num = int(main_num.group())
                    else:
                        main_num = 0
                    return (main_part[0], main_num, float(sub_part))
                else:
                    # 如果没有小数点，尝试提取数字部分
                    main_num = re.search(r'\d+', code_str)
                    if main_num:
                        main_num = int(main_num.group())
                    else:
                        main_num = 0
                    return (code_str[0], main_num, 0.0)
            
            # 按指标代码的数字部分排序
            df['sort_key'] = df['code'].apply(numeric_sort_key)
            df = df.sort_values(by='sort_key')
            df = df.drop('sort_key', axis=1)
            
            stats_table = df.to_html(classes='table table-striped table-bordered', index=False)
            
            # 计算统计信息
            total_indicators = len(df)
            achieved_count = df['target_achieved'].sum()
            achievement_rate = achieved_count / total_indicators * 100 if total_indicators > 0 else 0
            
            # 按指标类别统计达标率
            category_stats = []
            if not df.empty:
                # 根据指标代码前缀分组（A-急诊, B-医疗行为, C-结果, D-病历）
                df['category_prefix'] = df['code'].str[0]
                for prefix, category_name in [
                    ('A', '急诊和日间医疗质量'), 
                    ('B', '医疗行为质量'), 
                    ('C', '结果质量'), 
                    ('D', '病历质量')
                ]:
                    category_df = df[df['category_prefix'] == prefix]
                    if not category_df.empty:
                        cat_total = len(category_df)
                        cat_achieved = category_df['target_achieved'].sum()
                        cat_rate = cat_achieved / cat_total * 100 if cat_total > 0 else 0
                        category_stats.append({
                            'name': category_name,
                            'total': cat_total,
                            'achieved': cat_achieved,
                            'rate': round(cat_rate, 2)
                        })
        else:
            stats_table = "<p>无数据可显示</p>"
            total_indicators = 0
            achieved_count = 0
            achievement_rate = 0
            category_stats = []
        
        # 获取当前周期和医院信息
        current_period = ReportPeriod.query.get(period_id)
        current_hospital = Hospital.query.get(hospital_id) if hospital_id else None
        current_category = IndicatorCategory.query.get(category_id) if category_id else None
    else:
        stats_table = "<p>请选择报告周期查看数据</p>"
        total_indicators = 0
        achieved_count = 0
        achievement_rate = 0
        category_stats = []
        current_period = None
        current_hospital = None
        current_category = None
        
    return render_template(
        'dashboard/stats.html',
        title='指标统计分析',
        periods=periods,
        hospitals=hospitals,
        categories=categories,
        current_period=current_period,
        current_hospital=current_hospital,
        current_category=current_category,
        stats_table=stats_table,
        total_indicators=total_indicators,
        achieved_count=achieved_count,
        achievement_rate=round(achievement_rate, 2),
        category_stats=category_stats
    ) 