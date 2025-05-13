from app import db
from datetime import datetime
from sqlalchemy import func, case

class IndicatorCategory(db.Model):
    __tablename__ = 'indicator_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 与指标的关系
    indicators = db.relationship('Indicator', backref='category', lazy='dynamic')
    
    def __init__(self, name, description=None):
        self.name = name
        self.description = description
    
    def __repr__(self):
        return f'<IndicatorCategory {self.name}>'


class Indicator(db.Model):
    __tablename__ = 'indicators'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32), unique=True, nullable=False)  # 指标编码
    name = db.Column(db.String(128), nullable=False)  # 指标名称
    definition = db.Column(db.Text)  # 指标定义
    numerator_description = db.Column(db.Text)  # 分子说明
    denominator_description = db.Column(db.Text)  # 分母说明
    calculation_formula = db.Column(db.Text)  # 计算公式
    data_source = db.Column(db.String(256))  # 数据来源
    target_value = db.Column(db.String(64))  # 指标导向 - 修改为字符串类型
    unit = db.Column(db.String(32))  # 单位
    frequency = db.Column(db.String(32))  # 监测频率
    category_id = db.Column(db.Integer, db.ForeignKey('indicator_categories.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 与原始数据的关系在 RawData 模型中定义
    # 与计算结果的关系在 Result 模型中定义
    
    def __init__(self, code, name, category_id, definition=None, 
                 numerator_description=None, denominator_description=None,
                 calculation_formula=None, data_source=None, 
                 target_value=None, unit=None, frequency=None):
        self.code = code
        self.name = name
        self.category_id = category_id
        self.definition = definition
        self.numerator_description = numerator_description
        self.denominator_description = denominator_description
        self.calculation_formula = calculation_formula
        self.data_source = data_source
        self.target_value = target_value
        self.unit = unit
        self.frequency = frequency
    
    def __repr__(self):
        return f'<Indicator {self.code}: {self.name}>'
        
    @staticmethod
    def numeric_code_order():
        """创建一个能按数字顺序对指标编码排序的表达式"""
        # 提取主编码部分 (例如 'C11')
        # 使用 substr 和 instr 函数，这些在 SQLite 中都支持
        main_part = func.substr(
            Indicator.code, 
            1, 
            func.instr(Indicator.code + '.', '.') - 1
        )
        
        # 提取子代码部分 (例如 '.2', '.14' 中的数字部分)
        sub_code_part = func.substr(
            Indicator.code,
            func.instr(Indicator.code + '.', '.') + 1
        )
        
        # 将子代码转换为数字进行排序
        # 如果没有子代码（即没有小数点），则视为0
        # 修改case函数调用，将列表形式的whens参数改为位置参数形式
        numeric_sub_code = case(
            (func.instr(Indicator.code, '.') > 0, func.cast(sub_code_part, db.Float)),
            else_=0
        )
        
        # 返回排序表达式列表：先按主编码字符串排序，再按子编码数字排序
        return [main_part, numeric_sub_code] 