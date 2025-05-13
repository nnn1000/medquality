from app import db
from datetime import datetime, timedelta

# Helper function to get current Beijing time
def beijing_now():
    """Return current time in Beijing timezone (UTC+8)"""
    return datetime.utcnow() + timedelta(hours=8)

class RawData(db.Model):
    __tablename__ = 'raw_data'
    
    id = db.Column(db.Integer, primary_key=True)
    indicator_id = db.Column(db.Integer, db.ForeignKey('indicators.id'), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False)
    period_id = db.Column(db.Integer, db.ForeignKey('report_periods.id'), nullable=False)
    numerator = db.Column(db.Float)  # 分子
    denominator = db.Column(db.Float)  # 分母
    submitter_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 提交人
    submit_time = db.Column(db.DateTime, default=beijing_now)  # 提交时间，使用北京时间
    note = db.Column(db.Text)  # 备注
    
    # 关系
    indicator = db.relationship('Indicator', backref='raw_data')
    hospital = db.relationship('Hospital', backref='raw_data')
    period = db.relationship('ReportPeriod', backref='raw_data')
    submitter = db.relationship('User', backref='raw_data_submitted')
    
    def __init__(self, indicator_id, hospital_id, period_id, numerator=None, 
                 denominator=None, submitter_id=None, note=None):
        self.indicator_id = indicator_id
        self.hospital_id = hospital_id
        self.period_id = period_id
        self.numerator = numerator
        self.denominator = denominator
        self.submitter_id = submitter_id
        self.note = note
    
    def __repr__(self):
        return f'<RawData {self.indicator_id} for {self.hospital_id} in period {self.period_id}>'


class Result(db.Model):
    __tablename__ = 'results'
    
    id = db.Column(db.Integer, primary_key=True)
    indicator_id = db.Column(db.Integer, db.ForeignKey('indicators.id'), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False)
    period_id = db.Column(db.Integer, db.ForeignKey('report_periods.id'), nullable=False)
    raw_data_id = db.Column(db.Integer, db.ForeignKey('raw_data.id'))
    value = db.Column(db.Float)  # 计算结果值
    target_achieved = db.Column(db.Boolean)  # 是否达标
    calculation_time = db.Column(db.DateTime, default=beijing_now)  # 计算时间，使用北京时间
    
    # 关系
    indicator = db.relationship('Indicator', backref='results')
    hospital = db.relationship('Hospital', backref='results')
    period = db.relationship('ReportPeriod', backref='results')
    raw_data = db.relationship('RawData', backref=db.backref('result', uselist=False))
    
    def __init__(self, indicator_id, hospital_id, period_id, raw_data_id=None, 
                 value=None, target_achieved=None):
        self.indicator_id = indicator_id
        self.hospital_id = hospital_id
        self.period_id = period_id
        self.raw_data_id = raw_data_id
        self.value = value
        self.target_achieved = target_achieved
    
    def __repr__(self):
        return f'<Result {self.indicator_id} for {self.hospital_id} in period {self.period_id}>' 