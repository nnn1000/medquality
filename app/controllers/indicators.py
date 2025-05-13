from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_login import login_required, current_user
from app import db
from app.models.indicator import Indicator, IndicatorCategory
from app.models.hospital import Hospital
from app.models.report_period import ReportPeriod
from app.models.data import RawData, Result
from app.services.calculator import IndicatorCalculator
from app.forms import RawDataForm, BulkDataImportForm, IndicatorForm
from werkzeug.utils import secure_filename
import pandas as pd
import os
from datetime import datetime
import uuid
import re
from sqlalchemy import case

# 创建指标数据蓝图
indicators_bp = Blueprint('indicators', __name__, url_prefix='/indicators')

@indicators_bp.route('/')
@login_required
def index():
    """显示指标列表页面"""
    # 获取筛选参数
    category_id = request.args.get('category_id', type=int)
    
    # 构建查询
    query = Indicator.query
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    # 获取所有指标和类别 - 使用数字正确排序
    indicators = query.order_by(*Indicator.numeric_code_order()).all()
    
    # 按照指定顺序获取类别
    categories = IndicatorCategory.query.order_by(
        case(
            (IndicatorCategory.name == '急诊和日间医疗质量', 1),
            (IndicatorCategory.name == '医疗行为质量', 2),
            (IndicatorCategory.name == '结果质量', 3),
            (IndicatorCategory.name == '病历质量', 4)
        )
    ).all()
    
    return render_template(
        'indicators/index.html',
        title='指标列表',
        indicators=indicators,
        categories=categories,
        current_category_id=category_id
    )

@indicators_bp.route('/<int:indicator_id>')
@login_required
def view(indicator_id):
    """查看单个指标详情"""
    indicator = Indicator.query.get_or_404(indicator_id)
    
    return render_template(
        'indicators/view.html',
        title=f'指标详情: {indicator.name}',
        indicator=indicator
    )

@indicators_bp.route('/data')
@login_required
def data_list():
    """显示原始数据列表页面"""
    # 获取筛选参数
    hospital_id = request.args.get('hospital_id', type=int)
    period_id = request.args.get('period_id', type=int)
    indicator_id = request.args.get('indicator_id', type=int)
    
    # 构建查询
    query = RawData.query
    if hospital_id:
        query = query.filter_by(hospital_id=hospital_id)
    if period_id:
        query = query.filter_by(period_id=period_id)
    if indicator_id:
        query = query.filter_by(indicator_id=indicator_id)
    
    # 获取数据
    raw_data = query.order_by(RawData.submit_time.desc()).all()
    hospitals = Hospital.query.order_by(Hospital.name).all()
    periods = ReportPeriod.query.order_by(
        ReportPeriod.year.desc(), 
        ReportPeriod.quarter.desc(), 
        ReportPeriod.month.desc()
    ).all()
    # 使用数字正确排序
    indicators = Indicator.query.order_by(*Indicator.numeric_code_order()).all()
    
    return render_template(
        'indicators/data_list.html',
        title='原始数据列表',
        raw_data=raw_data,
        hospitals=hospitals,
        periods=periods,
        indicators=indicators,
        current_hospital_id=hospital_id,
        current_period_id=period_id,
        current_indicator_id=indicator_id
    )

@indicators_bp.route('/data/add', methods=['GET', 'POST'])
@login_required
def add_data():
    """添加原始数据"""
    form = RawDataForm()
    
    if request.method == 'POST':
        # 直接打印原始表单数据，便于排查问题
        print(f"表单原始数据: {request.form}")
    
    if form.validate_on_submit():
        try:
            # 打印提交数据，便于调试
            print(f"表单提交数据: period_id={form.period_id.data}, indicator_id={form.indicator_id.data}, hospital_id={form.hospital_id.data}, numerator={form.numerator.data}, denominator={form.denominator.data}")
            
            # 确保分子和分母是有效的数字（特别处理0值）
            numerator = form.numerator.data
            # 明确检查是否为0值（包括整数0和浮点数0.0）
            if isinstance(numerator, (int, float)) and numerator == 0:
                numerator = 0  # 确保0值被保留为0
            
            denominator = form.denominator.data
            if isinstance(denominator, (int, float)) and denominator == 0:
                denominator = 0  # 确保0值被保留为0
                
            # 获取选择的报告周期
            period_id = form.period_id.data
            period = ReportPeriod.query.get(period_id)
            
            if not period:
                flash('无效的报告周期，请重新选择', 'danger')
                print(f"无效的报告周期ID: {period_id}")
                return render_template(
                    'indicators/add_data.html',
                    title='添加原始数据',
                    form=form
                )
                
            print(f"找到报告周期: {period.name} (ID: {period.id})")
                
            # 验证这是否为标准化的报告周期格式
            # 如果不是标准格式，尝试找到对应的标准周期
            standardized_period = ensure_standard_period_format(period)
            if standardized_period and standardized_period.id != period.id:
                # 使用找到的标准周期
                period_id = standardized_period.id
                print(f"已自动调整为标准周期: {standardized_period.name} (ID: {standardized_period.id})")
                flash(f'已自动将报告周期 "{period.name}" 调整为系统标准格式 "{standardized_period.name}"', 'info')
            
            # 获取指标信息
            indicator = Indicator.query.get(form.indicator_id.data)
            if not indicator:
                flash('无效的指标，请重新选择', 'danger')
                return render_template(
                    'indicators/add_data.html',
                    title='添加原始数据',
                    form=form
                )
                
            print(f"指标信息: code={indicator.code}, name={indicator.name}, unit={indicator.unit}")
            
            # 打印表单原始数据的分子值，以便调试
            print(f"表单原始值 - 分子: {'0' if numerator == 0 else numerator}, 分母: {denominator}")
            
            # 分子分母必填检查
            base_code = indicator.code.split('.')[0] if '.' in indicator.code else indicator.code
            if base_code in ['B11'] and (numerator is None or denominator is None):
                if numerator is None:
                    flash('B11系列指标的分子不能为空', 'danger')
                if denominator is None:
                    flash('B11系列指标的分母不能为空', 'danger')
                return render_template(
                    'indicators/add_data.html',
                    title='添加原始数据',
                    form=form
                )
            
            # 验证分子和分母的值
            if numerator is not None and (not isinstance(numerator, (int, float)) or numerator < 0):
                flash('分子必须是有效的非负数值', 'danger')
                return render_template(
                    'indicators/add_data.html',
                    title='添加原始数据',
                    form=form
                )
                
            if denominator is not None and (not isinstance(denominator, (int, float)) or denominator <= 0):
                flash('分母必须是有效的正数值', 'danger')
                return render_template(
                    'indicators/add_data.html',
                    title='添加原始数据',
                    form=form
                )
            
            # 创建新的原始数据记录
            raw_data = RawData(
                indicator_id=form.indicator_id.data,
                hospital_id=form.hospital_id.data,
                period_id=period_id,  # 使用标准化后的period_id
                numerator=numerator,
                denominator=denominator,
                submitter_id=current_user.id,
                note=form.note.data
            )
            
            print(f"保存数据: indicator_id={raw_data.indicator_id}, hospital_id={raw_data.hospital_id}, period_id={raw_data.period_id}, numerator={raw_data.numerator}, denominator={raw_data.denominator}")
            
            db.session.add(raw_data)
            db.session.commit()
            
            # 计算指标结果
            try:
                result = IndicatorCalculator.calculate_indicator(raw_data.id)
                
                if result:
                    print(f"指标计算成功: 值={result.value}, 达标={result.target_achieved}")
                    flash('数据已成功添加，指标计算完成', 'success')
                else:
                    print(f"指标计算失败：raw_data_id={raw_data.id}, indicator={indicator.code}, numerator={numerator}, denominator={denominator}")
                    flash('数据已添加，但计算结果失败，请检查数据', 'warning')
            except Exception as calc_error:
                print(f"指标计算异常: {str(calc_error)}")
                import traceback
                traceback.print_exc()
                flash('数据已添加，但计算过程中发生错误，请联系管理员', 'warning')
                
            return redirect(url_for('indicators.data_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'数据录入出错: {str(e)}', 'danger')
            print(f"数据录入错误: {str(e)}")
            import traceback
            traceback.print_exc()
    else:
        # 输出表单验证错误信息
        if request.method == 'POST':
            print(f"表单验证失败，错误信息: {form.errors}")
            
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", 'danger')
                print(f"表单验证错误: {getattr(form, field).label.text}: {error}")
    
    # 预先选择当前用户的医院（如果有）
    if current_user.hospital_id and not form.hospital_id.data:
        form.hospital_id.data = current_user.hospital_id
    
    return render_template(
        'indicators/add_data.html',
        title='添加原始数据',
        form=form
    )

def ensure_standard_period_format(period):
    """确保使用标准化的报告周期格式"""
    if not period:
        return None
        
    # 直接使用ReportPeriod类的方法
    standard_period = ReportPeriod.get_standard_period(period.name)
    
    # 如果没有找到标准周期，返回原始周期
    return standard_period or period

@indicators_bp.route('/data/<int:data_id>')
@login_required
def view_data(data_id):
    """查看单条原始数据详情"""
    raw_data = RawData.query.get_or_404(data_id)
    
    # 查找对应的计算结果
    result = Result.query.filter_by(raw_data_id=data_id).first()
    
    return render_template(
        'indicators/view_data.html',
        title='数据详情',
        raw_data=raw_data,
        result=result
    )

@indicators_bp.route('/data/<int:data_id>/calculate')
@login_required
def calculate(data_id):
    """计算单条数据的指标结果"""
    raw_data = RawData.query.get_or_404(data_id)
    
    result = IndicatorCalculator.calculate_indicator(raw_data.id)
    
    if result:
        flash(f'指标计算成功，结果为 {result.value} {raw_data.indicator.unit}，{"达标" if result.target_achieved else "未达标"}', 'success')
    else:
        flash('指标计算失败，请检查数据', 'danger')
    
    return redirect(url_for('indicators.view_data', data_id=data_id))

@indicators_bp.route('/data/<int:data_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_data(data_id):
    """删除原始数据"""
    raw_data = RawData.query.get_or_404(data_id)
    
    # 检查权限，只有管理员或数据提交者可以删除
    if not current_user.is_admin and raw_data.submitter_id != current_user.id:
        flash('您没有权限删除此数据', 'danger')
        return redirect(url_for('indicators.data_list'))
    
    try:
        # 获取一些信息用于显示在删除确认信息中
        indicator_name = raw_data.indicator.name
        hospital_name = raw_data.hospital.name
        period_name = raw_data.period.name
        
        # 删除相关的结果记录
        if raw_data.result:
            db.session.delete(raw_data.result)
        
        # 删除原始数据
        db.session.delete(raw_data)
        db.session.commit()
        
        flash(f'已删除 {hospital_name} 的 {indicator_name} 在 {period_name} 的数据记录', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'删除数据时出错: {str(e)}', 'danger')
    
    return redirect(url_for('indicators.data_list'))

@indicators_bp.route('/data/recalculate_all')
@login_required
def recalculate_all():
    """重新计算所有缺失计算结果的数据"""
    if not current_user.is_admin:
        flash('只有管理员可以执行此操作', 'danger')
        return redirect(url_for('indicators.data_list'))
    
    # 查找所有没有对应结果的原始数据
    missing_results_subquery = db.session.query(Result.raw_data_id)
    raw_data_missing_results = RawData.query.filter(
        ~RawData.id.in_(missing_results_subquery)
    ).all()
    
    # 计算所有缺失的结果
    success_count = 0
    for raw_data in raw_data_missing_results:
        result = IndicatorCalculator.calculate_indicator(raw_data.id)
        if result:
            success_count += 1
    
    if success_count > 0:
        flash(f'成功计算 {success_count} 条缺失的结果', 'success')
    else:
        flash('没有找到需要计算的数据', 'info')
    
    return redirect(url_for('indicators.data_list'))

@indicators_bp.route('/data/import', methods=['GET', 'POST'])
@login_required
def import_data():
    """批量导入原始数据"""
    form = BulkDataImportForm()
    
    if form.validate_on_submit():
        # 保存上传的文件
        f = form.file.data
        filename = secure_filename(f.filename)
        
        # 创建上传目录
        uploads_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'instance', 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        
        # 生成唯一文件名
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(uploads_dir, unique_filename)
        f.save(filepath)
        
        try:
            # 读取Excel数据
            df = pd.read_excel(filepath)
            
            # 校验必要列
            required_columns = ['指标编码', '分子', '分母']
            if not all(col in df.columns for col in required_columns):
                flash('Excel文件格式不正确，必须包含：指标编码、分子、分母列', 'danger')
                return redirect(url_for('indicators.import_data'))
            
            # 获取医院和周期
            hospital = Hospital.query.get(form.hospital_id.data)
            period = ReportPeriod.query.get(form.period_id.data)
            
            if not hospital or not period:
                flash('无效的医院或报告周期', 'danger')
                return redirect(url_for('indicators.import_data'))
            
            # 导入计数
            import_count = 0
            error_count = 0
            
            # 处理每一行数据
            for index, row in df.iterrows():
                try:
                    # 查找指标
                    indicator = Indicator.query.filter_by(code=row['指标编码']).first()
                    if not indicator:
                        error_count += 1
                        continue
                    
                    # 创建原始数据记录
                    raw_data = RawData(
                        indicator_id=indicator.id,
                        hospital_id=hospital.id,
                        period_id=period.id,
                        numerator=row['分子'] if not pd.isna(row['分子']) else None,
                        denominator=row['分母'] if not pd.isna(row['分母']) else None,
                        submitter_id=current_user.id,
                        note=f"批量导入于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    )
                    
                    db.session.add(raw_data)
                    db.session.flush()  # 获取ID
                    
                    # 计算指标结果
                    IndicatorCalculator.calculate_indicator(raw_data.id)
                    
                    import_count += 1
                except Exception as e:
                    error_count += 1
                    continue
            
            db.session.commit()
            
            if import_count > 0:
                flash(f'成功导入 {import_count} 条数据，失败 {error_count} 条', 'success')
            else:
                flash(f'导入失败，请检查Excel文件格式', 'danger')
            
        except Exception as e:
            flash(f'导入出错: {str(e)}', 'danger')
        
        # 删除临时文件
        try:
            os.remove(filepath)
        except:
            pass
        
        return redirect(url_for('indicators.data_list'))
    
    # 预先选择当前用户的医院（如果有）
    if current_user.hospital_id and not form.hospital_id.data:
        form.hospital_id.data = current_user.hospital_id
    
    return render_template(
        'indicators/import_data.html',
        title='批量导入数据',
        form=form
    )

@indicators_bp.route('/<int:indicator_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(indicator_id):
    """编辑指标"""
    indicator = Indicator.query.get_or_404(indicator_id)
    form = IndicatorForm(obj=indicator)
    
    # 设置隐藏的indicator_id字段
    form.indicator_id.data = str(indicator_id)
    
    if form.validate_on_submit():
        form.populate_obj(indicator)
        db.session.commit()
        flash(f'指标 {indicator.code} - {indicator.name} 已更新', 'success')
        return redirect(url_for('indicators.view', indicator_id=indicator.id))
        
    return render_template(
        'indicators/edit.html',
        title=f'编辑指标: {indicator.name}',
        form=form,
        indicator=indicator
    ) 