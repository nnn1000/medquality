from app import db
from datetime import datetime, date
import re

class ReportPeriod(db.Model):
    __tablename__ = 'report_periods'
    
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    quarter = db.Column(db.Integer)  # 1-4 表示季度，NULL 表示不是季度报告
    month = db.Column(db.Integer)  # 1-12 表示月份，NULL 表示不是月度报告
    name = db.Column(db.String(64), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 与原始数据的关系在 RawData 模型中定义
    # 与计算结果的关系在 Result 模型中定义
    
    def __init__(self, year, start_date, end_date, name=None, quarter=None, month=None):
        self.year = year
        self.start_date = start_date
        self.end_date = end_date
        self.quarter = quarter
        self.month = month
        
        # 如果未提供名称，自动生成
        if name is None:
            if month is not None:
                self.name = f"{year}年{month}月"
            elif quarter is not None:
                self.name = f"{year}年第{quarter}季度"
            else:
                self.name = f"{year}年"
        else:
            self.name = name
    
    def __repr__(self):
        return f'<ReportPeriod {self.name}>'
        
    @staticmethod
    def standardize_period_name(year, start_month, end_month):
        """根据起止年月返回标准化的报告周期名称"""
        # 确保参数是整型
        year = int(year)
        start_month = int(start_month)
        end_month = int(end_month)
        
        # 第一季度
        if start_month == 1 and end_month == 3:
            return f"{year}年第1季度"
        # 第二季度
        elif start_month == 4 and end_month == 6:
            return f"{year}年第2季度"
        # 第三季度
        elif start_month == 7 and end_month == 9:
            return f"{year}年第3季度"
        # 第四季度
        elif start_month == 10 and end_month == 12:
            return f"{year}年第4季度"
        # 上半年
        elif start_month == 1 and end_month == 6:
            return f"{year}年上半年"
        # 下半年
        elif start_month == 7 and end_month == 12:
            return f"{year}年下半年"
        # 全年
        elif start_month == 1 and end_month == 12:
            return f"{year}年"
        # 单月
        elif start_month == end_month:
            return f"{year}年{start_month}月"
        # 其他范围
        else:
            return f"{year}年{start_month}月-{end_month}月"
            
    @classmethod
    def get_standard_period(cls, period_name):
        """根据期间名称查找标准周期"""
        # 先尝试直接查找完全匹配
        period = cls.query.filter_by(name=period_name).first()
        if period:
            print(f"找到完全匹配的周期: {period.name}")
            return period
            
        # 解析期间名称
        print(f"尝试解析期间名称: {period_name}")
        
        # 尝试匹配"YYYY年M月-M月"格式
        month_range_match = re.match(r'(\d{4})年(\d{1,2})月-(\d{1,2})月$', period_name)
        if month_range_match:
            year = int(month_range_match.group(1))
            start_month = int(month_range_match.group(2))
            end_month = int(month_range_match.group(3))
            
            print(f"解析到月份范围: {year}年{start_month}月-{end_month}月")
            
            # 查找对应的标准周期
            if start_month == 1 and end_month == 3:
                print("匹配到第一季度")
                return cls.query.filter_by(year=year, quarter=1).first()
            elif start_month == 4 and end_month == 6:
                print("匹配到第二季度")
                return cls.query.filter_by(year=year, quarter=2).first()
            elif start_month == 7 and end_month == 9:
                print("匹配到第三季度")
                return cls.query.filter_by(year=year, quarter=3).first()
            elif start_month == 10 and end_month == 12:
                print("匹配到第四季度")
                return cls.query.filter_by(year=year, quarter=4).first()
            elif start_month == 1 and end_month == 6:
                print("匹配到上半年")
                # 上半年可能表示为1-2季度
                return cls.query.filter_by(year=year, quarter=0, month=0, half_year=1).first()
            elif start_month == 7 and end_month == 12:
                print("匹配到下半年")
                # 下半年可能表示为3-4季度
                return cls.query.filter_by(year=year, quarter=0, month=0, half_year=2).first()
            elif start_month == 1 and end_month == 12:
                print("匹配到全年")
                # 全年
                return cls.query.filter_by(year=year, quarter=0, month=0, half_year=0).first()
            elif start_month == end_month:
                print(f"匹配到单月: {year}年{start_month}月")
                # 单月
                return cls.query.filter_by(year=year, month=start_month).first()
        
        # 尝试匹配"YYYY年第Q季度"格式
        quarter_match = re.match(r'(\d{4})年第([一二三四\d])季度$', period_name)
        if quarter_match:
            year = int(quarter_match.group(1))
            quarter_text = quarter_match.group(2)
            
            # 将中文数字转换为阿拉伯数字
            quarter_mapping = {'一': 1, '二': 2, '三': 3, '四': 4}
            quarter = quarter_mapping.get(quarter_text, int(quarter_text))
            
            print(f"解析到季度: {year}年第{quarter}季度")
            
            return cls.query.filter_by(year=year, quarter=quarter).first()
        
        # 尝试匹配"YYYY年MM月"单月格式
        single_month_match = re.match(r'(\d{4})年(\d{1,2})月$', period_name)
        if single_month_match:
            year = int(single_month_match.group(1))
            month = int(single_month_match.group(2))
            
            print(f"解析到单月: {year}年{month}月")
            
            return cls.query.filter_by(year=year, month=month).first()
        
        # 尝试匹配跨年格式 "YYYY年MM月-YYYY年MM月"
        cross_year_match = re.match(r'(\d{4})年(\d{1,2})月-(\d{4})年(\d{1,2})月$', period_name)
        if cross_year_match:
            start_year = int(cross_year_match.group(1))
            start_month = int(cross_year_match.group(2))
            end_year = int(cross_year_match.group(3))
            end_month = int(cross_year_match.group(4))
            
            print(f"解析到跨年期间: {start_year}年{start_month}月-{end_year}年{end_month}月")
            
            # 如果是标准的跨年度季度格式
            if start_month == 10 and end_month == 3 and end_year == start_year + 1:
                # 特殊处理第四季度到下一年第一季度的跨度
                print("匹配到跨年冬季")
                return cls.query.filter_by(year=start_year, is_winter=True).first()
        
        # 找不到匹配，尝试按年份+名称模糊匹配
        year_match = re.search(r'(\d{4})年', period_name)
        if year_match:
            year = int(year_match.group(1))
            print(f"提取到年份: {year}，尝试模糊匹配")
            
            # 按年份查找可能的周期，按名称相似度排序
            periods = cls.query.filter_by(year=year).all()
            if periods:
                # 简单返回同年份的第一个周期
                print(f"返回同年份周期: {periods[0].name}")
                return periods[0]
        
        print("无法找到匹配的周期")
        return None 