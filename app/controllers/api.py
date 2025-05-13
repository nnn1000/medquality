from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.models.indicator import Indicator, IndicatorCategory

# 创建API蓝图
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/indicators', methods=['GET'])
@login_required
def get_indicators():
    """获取指标列表，支持可选的类别筛选"""
    # 获取查询参数
    category_id = request.args.get('category_id', type=int)
    
    # 构建基础查询
    query = Indicator.query
    
    # 应用类别筛选
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    # 使用自定义数字排序方法获取指标
    indicators = query.order_by(*Indicator.numeric_code_order()).all()
    
    # 转换为JSON格式
    indicators_list = []
    for indicator in indicators:
        indicators_list.append({
            'id': indicator.id,
            'code': indicator.code,
            'name': indicator.name,
            'category': {
                'id': indicator.category.id,
                'name': indicator.category.name
            }
        })
    
    return jsonify({
        'success': True,
        'indicators': indicators_list
    })

@api_bp.route('/indicators/<int:indicator_id>', methods=['GET'])
@login_required
def get_indicator(indicator_id):
    """获取单个指标的详细信息"""
    indicator = Indicator.query.get(indicator_id)
    
    if not indicator:
        return jsonify({
            'success': False,
            'message': f'指标ID {indicator_id} 不存在'
        }), 404
    
    # 构建指标数据
    indicator_data = {
        'id': indicator.id,
        'code': indicator.code,
        'name': indicator.name,
        'definition': indicator.definition,
        'numerator_description': indicator.numerator_description,
        'denominator_description': indicator.denominator_description,
        'calculation_formula': indicator.calculation_formula,
        'unit': indicator.unit,
        'target_value': indicator.target_value,
        'frequency': indicator.frequency,
        'data_source': indicator.data_source,
        'category': {
            'id': indicator.category.id,
            'name': indicator.category.name
        }
    }
    
    return jsonify({
        'success': True,
        'indicator': indicator_data
    }) 