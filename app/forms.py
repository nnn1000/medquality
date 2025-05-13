from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FloatField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, ValidationError
from app.models.user import User
from app.models.hospital import Hospital
from app.models.indicator import Indicator, IndicatorCategory
from app.models.report_period import ReportPeriod
from datetime import datetime, date
from flask_wtf.file import FileAllowed


# Helper function to preserve zero values
def preserve_zero_filter(x):
    # Explicitly check for zero values (numeric or string)
    if x == 0 or x == '0':
        return 0
    return x if x is not None else None


class LoginForm(FlaskForm):
    """用户登录表单"""
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class RegisterForm(FlaskForm):
    """用户注册表单"""
    username = StringField('用户名', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('电子邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password')])
    hospital_id = SelectField('所属医院', coerce=int, validators=[Optional()])
    submit = SubmitField('注册')
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.hospital_id.choices = [(0, '无')] + [(h.id, h.name) for h in Hospital.query.order_by(Hospital.name).all()]
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('该用户名已被使用，请选择其他用户名。')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('该邮箱已被注册，请使用其他邮箱。')


class HospitalForm(FlaskForm):
    """医院表单"""
    name = StringField('医院名称', validators=[DataRequired(), Length(max=128)])
    code = StringField('医院代码', validators=[DataRequired(), Length(max=32)])
    address = StringField('医院地址', validators=[Optional(), Length(max=256)])
    level = SelectField('医院等级', choices=[
        ('', '请选择'),
        ('三级甲等', '三级甲等'),
        ('三级乙等', '三级乙等'),
        ('三级丙等', '三级丙等'),
        ('二级甲等', '二级甲等'),
        ('二级乙等', '二级乙等'),
        ('二级丙等', '二级丙等'),
        ('一级甲等', '一级甲等'),
        ('一级乙等', '一级乙等'),
        ('一级丙等', '一级丙等'),
        ('其他', '其他')
    ], validators=[Optional()])
    type = SelectField('医院类型', choices=[
        ('', '请选择'),
        ('综合医院', '综合医院'),
        ('专科医院', '专科医院'),
        ('中医医院', '中医医院'),
        ('妇幼保健院', '妇幼保健院'),
        ('社区医院', '社区医院'),
        ('其他', '其他')
    ], validators=[Optional()])
    contact_person = StringField('联系人', validators=[Optional(), Length(max=64)])
    contact_phone = StringField('联系电话', validators=[Optional(), Length(max=32)])
    submit = SubmitField('提交')
    
    def validate_code(self, code):
        hospital = Hospital.query.filter_by(code=code.data).first()
        if hospital is not None and (not hasattr(self, 'id') or hospital.id != self.id.data):
            raise ValidationError('该医院代码已存在，请使用其他代码。')
    
    def validate_name(self, name):
        hospital = Hospital.query.filter_by(name=name.data).first()
        if hospital is not None and (not hasattr(self, 'id') or hospital.id != self.id.data):
            raise ValidationError('该医院名称已存在，请使用其他名称。')


class ReportPeriodForm(FlaskForm):
    """报告周期表单"""
    year = SelectField('年份', choices=[(y, str(y)) for y in range(2020, datetime.now().year + 2)], 
                      validators=[DataRequired()], coerce=int)
    period_type = SelectField('周期类型', choices=[
        ('year', '年度'),
        ('quarter', '季度'),
        ('month', '月度')
    ], validators=[DataRequired()])
    quarter = SelectField('季度', choices=[
        ('', '请选择'),
        ('1', '第一季度'),
        ('2', '第二季度'),
        ('3', '第三季度'),
        ('4', '第四季度')
    ], validators=[Optional()])
    month = SelectField('月份', choices=[
        ('', '请选择')] + [(str(i), f"{i}月") for i in range(1, 13)
    ], validators=[Optional()])
    start_date = StringField('开始日期', validators=[DataRequired()])
    end_date = StringField('结束日期', validators=[DataRequired()])
    submit = SubmitField('提交')


class RawDataForm(FlaskForm):
    """原始数据录入表单"""
    hospital_id = SelectField('医院', coerce=int, validators=[DataRequired()])
    period_id = SelectField('报告周期', coerce=int, validators=[DataRequired()])
    indicator_id = SelectField('指标', coerce=int, validators=[DataRequired()])
    numerator = FloatField('分子', validators=[Optional()], filters=[preserve_zero_filter])
    denominator = FloatField('分母', validators=[Optional()], filters=[preserve_zero_filter])
    note = TextAreaField('备注', validators=[Optional(), Length(max=1000)])
    submit_btn = SubmitField('提交')  # 改名为submit_btn避免与form.submit()方法冲突
    
    def __init__(self, *args, **kwargs):
        super(RawDataForm, self).__init__(*args, **kwargs)
        self.hospital_id.choices = [(h.id, h.name) for h in Hospital.query.order_by(Hospital.name).all()]
        self.period_id.choices = [(p.id, p.name) for p in ReportPeriod.query.order_by(ReportPeriod.year.desc(), 
                                                                                   ReportPeriod.quarter.desc(), 
                                                                                   ReportPeriod.month.desc()).all()]
        self.indicator_id.choices = [(i.id, f"{i.code} - {i.name}") for i in Indicator.query.order_by(*Indicator.numeric_code_order()).all()]


class BulkDataImportForm(FlaskForm):
    """批量数据导入表单"""
    file = FileField('Excel文件', validators=[DataRequired(), FileAllowed(['xlsx', 'xls'], '只能上传Excel文件')])
    hospital_id = SelectField('医院', coerce=int, validators=[DataRequired()])
    period_id = SelectField('报告周期', coerce=int, validators=[DataRequired()])
    submit = SubmitField('导入')
    
    def __init__(self, *args, **kwargs):
        super(BulkDataImportForm, self).__init__(*args, **kwargs)
        self.hospital_id.choices = [(h.id, h.name) for h in Hospital.query.order_by(Hospital.name).all()]
        self.period_id.choices = [(p.id, p.name) for p in ReportPeriod.query.order_by(ReportPeriod.year.desc(), 
                                                                                   ReportPeriod.quarter.desc(), 
                                                                                   ReportPeriod.month.desc()).all()]


class ReportGenerationForm(FlaskForm):
    """报表生成表单"""
    period_id = SelectField('报告周期', coerce=int, validators=[DataRequired()])
    hospital_id = SelectField('医院', coerce=int, validators=[Optional()])
    report_type = SelectField('报告类型', choices=[
        ('standard', '标准报告'),
        ('detailed', '详细报告'),
        ('summary', '汇总报告')
    ], validators=[DataRequired()])
    submit = SubmitField('生成报告')
    
    def __init__(self, *args, **kwargs):
        super(ReportGenerationForm, self).__init__(*args, **kwargs)
        self.period_id.choices = [(p.id, p.name) for p in ReportPeriod.query.order_by(ReportPeriod.year.desc(), 
                                                                                   ReportPeriod.quarter.desc(), 
                                                                                   ReportPeriod.month.desc()).all()]
        self.hospital_id.choices = [(0, '所有医院')] + [(h.id, h.name) for h in Hospital.query.order_by(Hospital.name).all()]


class IndicatorForm(FlaskForm):
    """指标编辑表单"""
    indicator_id = StringField('指标ID')  # 隐藏字段，用于编辑时存储当前指标ID
    code = StringField('指标编码', validators=[DataRequired(), Length(max=32)])
    name = StringField('指标名称', validators=[DataRequired(), Length(max=128)])
    category_id = SelectField('指标类别', coerce=int, validators=[DataRequired()])
    definition = TextAreaField('指标定义', validators=[Optional()])
    numerator_description = TextAreaField('分子说明', validators=[Optional()])
    denominator_description = TextAreaField('分母说明', validators=[Optional()])
    calculation_formula = TextAreaField('计算公式', validators=[Optional()])
    data_source = StringField('数据来源', validators=[Optional(), Length(max=256)])
    target_value = StringField('指标导向', validators=[Optional()])
    unit = StringField('单位', validators=[Optional(), Length(max=32)])
    frequency = StringField('监测频率', validators=[Optional(), Length(max=32)])
    submit = SubmitField('保存')
    
    def __init__(self, *args, **kwargs):
        super(IndicatorForm, self).__init__(*args, **kwargs)
        self.category_id.choices = [(c.id, c.name) for c in IndicatorCategory.query.order_by(IndicatorCategory.name).all()]
    
    def validate_code(self, field):
        # 检查编码是否已存在（编辑时排除当前指标）
        indicator_id = self.indicator_id.data
        if indicator_id:
            indicator = Indicator.query.filter(Indicator.code == field.data, Indicator.id != int(indicator_id)).first()
        else:
            indicator = Indicator.query.filter_by(code=field.data).first()
        
        if indicator:
            raise ValidationError(f'指标编码 {field.data} 已存在') 