import click
from flask.cli import with_appcontext
from app import db
from app.models.user import User
from app.models.indicator import IndicatorCategory, Indicator
from app.models.hospital import Hospital
from app.models.report_period import ReportPeriod
from werkzeug.security import generate_password_hash
import pandas as pd
import os

@click.command('init-db')
@with_appcontext
def init_db_command():
    """初始化数据库并创建基础数据"""
    # 创建所有表
    db.create_all()
    
    # 添加初始管理员用户
    if User.query.filter_by(username='admin').first() is None:
        admin = User(
            username='admin',
            password_hash=generate_password_hash('admin123'),
            email='admin@example.com',
            is_admin=True
        )
        db.session.add(admin)
    
    # 添加指标类别
    categories = {
        '急诊和日间医疗质量': '包含急诊和日间医疗相关的6个质量指标',
        '医疗行为质量': '包含医疗行为相关的19个质量指标',
        '结果质量': '包含医疗结果相关的11个质量指标',
        '病历质量': '包含病历管理相关的4个质量指标'
    }
    
    for name, description in categories.items():
        if not IndicatorCategory.query.filter_by(name=name).first():
            category = IndicatorCategory(name=name, description=description)
            db.session.add(category)
    
    # 确保更改保存到数据库
    db.session.commit()
    
    # 添加示例指标数据
    # 实际项目中可以从Excel文件导入或手动添加全部40个指标
    add_sample_indicators()
    
    click.echo('数据库初始化完成！')


def add_sample_indicators():
    """添加示例指标数据"""
    # 获取指标类别ID
    categories = {cat.name: cat.id for cat in IndicatorCategory.query.all()}
    
    # 示例指标数据 - 每个类别添加几个指标示例
    indicators = [
        # 急诊和日间医疗质量指标示例
        {
            'code': 'A01',
            'name': '急诊抢救室滞留时间中位数',
            'category_id': categories['急诊和日间医疗质量'],
            'definition': '急诊抢救室患者滞留时间的中位数',
            'numerator_description': '所有在抢救室患者滞留时间的中位数',
            'denominator_description': '无',
            'calculation_formula': 'MEDIAN(急诊患者在抢救室的时间)',
            'data_source': '医院信息系统',
            'target_value': 120,
            'unit': '分钟',
            'frequency': '月度'
        },
        {
            'code': 'A02',
            'name': '急诊患者收入院内滞留时间中位数',
            'category_id': categories['急诊和日间医疗质量'],
            'definition': '急诊患者从急诊进入到住院的滞留时间中位数',
            'numerator_description': '所有从急诊进入住院患者的滞留时间中位数',
            'denominator_description': '无',
            'calculation_formula': 'MEDIAN(急诊患者入院前的滞留时间)',
            'data_source': '医院信息系统',
            'target_value': 240,
            'unit': '分钟',
            'frequency': '月度'
        },
        
        # 医疗行为质量指标示例
        {
            'code': 'B01',
            'name': '住院患者预防性抗菌药物使用率',
            'category_id': categories['医疗行为质量'],
            'definition': '住院患者中预防性使用抗菌药物的比例',
            'numerator_description': '预防性使用抗菌药物的住院患者数',
            'denominator_description': '住院患者总数',
            'calculation_formula': '预防性使用抗菌药物的住院患者数 / 住院患者总数 × 100%',
            'data_source': '医院信息系统和药房系统',
            'target_value': 20,
            'unit': '%',
            'frequency': '季度'
        },
        {
            'code': 'B02',
            'name': '门诊患者抗菌药物处方比例',
            'category_id': categories['医疗行为质量'],
            'definition': '门诊患者抗菌药物处方占门诊处方总数的比例',
            'numerator_description': '含抗菌药物的门诊处方数',
            'denominator_description': '门诊处方总数',
            'calculation_formula': '含抗菌药物的门诊处方数 / 门诊处方总数 × 100%',
            'data_source': '医院处方系统',
            'target_value': 15,
            'unit': '%',
            'frequency': '月度'
        },
        
        # 结果质量指标示例
        {
            'code': 'C01',
            'name': '住院患者跌倒发生率',
            'category_id': categories['结果质量'],
            'definition': '住院期间发生跌倒的患者比例',
            'numerator_description': '住院期间发生跌倒的患者数',
            'denominator_description': '住院患者总数',
            'calculation_formula': '住院期间发生跌倒的患者数 / 住院患者总数 × 100%',
            'data_source': '护理记录和不良事件报告',
            'target_value': 0.5,
            'unit': '%',
            'frequency': '季度'
        },
        {
            'code': 'C02',
            'name': '住院患者压疮发生率',
            'category_id': categories['结果质量'],
            'definition': '住院期间发生压疮的患者比例',
            'numerator_description': '住院期间发生压疮的患者数',
            'denominator_description': '住院患者总数',
            'calculation_formula': '住院期间发生压疮的患者数 / 住院患者总数 × 100%',
            'data_source': '护理记录和不良事件报告',
            'target_value': 0.3,
            'unit': '%',
            'frequency': '季度'
        },
        
        # 病历质量指标示例
        {
            'code': 'D01',
            'name': '住院病历完整率',
            'category_id': categories['病历质量'],
            'definition': '完整、符合规范的住院病历比例',
            'numerator_description': '完整、符合规范的住院病历数',
            'denominator_description': '住院病历总数',
            'calculation_formula': '完整、符合规范的住院病历数 / 住院病历总数 × 100%',
            'data_source': '病历质控评审记录',
            'target_value': 95,
            'unit': '%',
            'frequency': '季度'
        },
        {
            'code': 'D02',
            'name': '病历归档及时率',
            'category_id': categories['病历质量'],
            'definition': '出院后规定时间内完成归档的病历比例',
            'numerator_description': '规定时间内完成归档的出院病历数',
            'denominator_description': '出院病历总数',
            'calculation_formula': '规定时间内完成归档的出院病历数 / 出院病历总数 × 100%',
            'data_source': '病案室记录',
            'target_value': 98,
            'unit': '%',
            'frequency': '月度'
        }
    ]
    
    # 添加指标
    for indicator_data in indicators:
        # 检查指标是否已存在
        if not Indicator.query.filter_by(code=indicator_data['code']).first():
            indicator = Indicator(**indicator_data)
            db.session.add(indicator)
    
    # 提交更改
    db.session.commit() 