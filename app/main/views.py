from flask import render_template
from . import main
from app.models.indicator import Indicator

@main.route('/statistics/period_comparison')
def period_comparison():
    """同期对比分析页面"""
    indicators = Indicator.query.order_by(Indicator.code).all()
    return render_template('statistics/period_comparison.html', indicators=indicators) 