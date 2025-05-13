from app import db
from datetime import datetime

class Hospital(db.Model):
    __tablename__ = 'hospitals'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    code = db.Column(db.String(32), unique=True, nullable=False)
    address = db.Column(db.String(256))
    level = db.Column(db.String(32))  # 医院等级 (三甲、三乙等)
    type = db.Column(db.String(32))   # 医院类型 (综合、专科等)
    contact_person = db.Column(db.String(64))
    contact_phone = db.Column(db.String(32))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 用户关系在 User 模型中定义
    # 原始数据关系在 RawData 模型中定义
    
    def __init__(self, name, code, address=None, level=None, type=None, 
                 contact_person=None, contact_phone=None):
        self.name = name
        self.code = code
        self.address = address
        self.level = level
        self.type = type
        self.contact_person = contact_person
        self.contact_phone = contact_phone
    
    def __repr__(self):
        return f'<Hospital {self.name}>' 