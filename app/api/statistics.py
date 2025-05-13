from flask import jsonify, request
from app.api import api
from app.models.indicator import Indicator
from app.models.indicator_data import IndicatorData
from sqlalchemy import func
from datetime import datetime, timedelta

@api.route('/statistics/period_comparison', methods=['GET'])
def get_period_comparison():
    """获取同期对比数据"""
    indicator_code = request.args.get('indicator_code')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not all([indicator_code, start_date, end_date]):
        return jsonify({'error': '缺少必要参数'}), 400
        
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': '日期格式错误'}), 400
        
    # 获取去年同期数据
    last_year_start = start_date - timedelta(days=365)
    last_year_end = end_date - timedelta(days=365)
    
    # 查询当前期间数据
    current_data = IndicatorData.query.filter(
        IndicatorData.indicator_code == indicator_code,
        IndicatorData.report_date >= start_date,
        IndicatorData.report_date <= end_date
    ).order_by(IndicatorData.report_date).all()
    
    # 查询去年同期数据
    last_year_data = IndicatorData.query.filter(
        IndicatorData.indicator_code == indicator_code,
        IndicatorData.report_date >= last_year_start,
        IndicatorData.report_date <= last_year_end
    ).order_by(IndicatorData.report_date).all()
    
    # 格式化数据
    result = {
        'current_period': [{
            'date': data.report_date.strftime('%Y-%m-%d'),
            'value': float(data.value) if data.value is not None else None
        } for data in current_data],
        'last_year': [{
            'date': data.report_date.strftime('%Y-%m-%d'),
            'value': float(data.value) if data.value is not None else None
        } for data in last_year_data]
    }
    
    return jsonify(result) 