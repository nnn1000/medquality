from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, abort
from flask_login import login_required, current_user
from app import db
from app.models.indicator import Indicator, IndicatorCategory
from app.models.hospital import Hospital
from app.models.report_period import ReportPeriod
from app.models.data import Result
from app.forms import ReportGenerationForm
from app.services.report_generator import ReportGenerator
import os
from datetime import datetime
import re

# 创建报表蓝图
reports_bp = Blueprint('reports', __name__, url_prefix='/reports')

@reports_bp.route('/')
@login_required
def index():
    """显示报表生成页面"""
    form = ReportGenerationForm()
    
    # 获取已生成的报表文件列表
    reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'instance', 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    report_files = []
    for filename in os.listdir(reports_dir):
        if filename.endswith('.xlsx'):
            file_path = os.path.join(reports_dir, filename)
            file_stat = os.stat(file_path)
            created_time = datetime.fromtimestamp(file_stat.st_ctime)
            
            report_files.append({
                'name': filename,
                'path': file_path,
                'size': file_stat.st_size,
                'created': created_time
            })
    
    # 按时间倒序排序
    report_files.sort(key=lambda x: x['created'], reverse=True)
    
    return render_template(
        'reports/index.html',
        title='报表生成',
        form=form,
        report_files=report_files
    )

@reports_bp.route('/generate', methods=['POST'])
@login_required
def generate():
    """生成报表"""
    form = ReportGenerationForm()
    
    if form.validate_on_submit():
        period_id = form.period_id.data
        hospital_id = form.hospital_id.data if form.hospital_id.data != 0 else None
        report_type = form.report_type.data
        
        # 获取选择的报告周期
        period = ReportPeriod.query.get(period_id)
        
        if not period:
            flash('无效的报告周期，请重新选择', 'danger')
            return redirect(url_for('reports.index'))
        
        try:
            # 生成报表
            report_path = ReportGenerator.generate_excel_report(period_id, hospital_id, report_type)
            
            if report_path:
                filename = os.path.basename(report_path)
                flash(f'报表 {filename} 已成功生成', 'success')
            else:
                flash('报表生成失败，请确保有足够的数据', 'danger')
                
        except Exception as e:
            flash(f'报表生成出错: {str(e)}', 'danger')
        
        return redirect(url_for('reports.index'))
    
    # 表单验证失败
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{getattr(form, field).label.text}: {error}', 'danger')
            
    return redirect(url_for('reports.index'))

@reports_bp.route('/download/<filename>')
@login_required
def download(filename):
    """下载已生成的报表"""
    reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'instance', 'reports')
    file_path = os.path.join(reports_dir, filename)
    
    if not os.path.exists(file_path):
        abort(404)
    
    return send_file(file_path, as_attachment=True)

@reports_bp.route('/delete/<filename>')
@login_required
def delete(filename):
    """删除已生成的报表"""
    if not current_user.is_admin:
        flash('您没有权限删除报表文件', 'danger')
        return redirect(url_for('reports.index'))
    
    reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'instance', 'reports')
    file_path = os.path.join(reports_dir, filename)
    
    if os.path.exists(file_path):
        os.remove(file_path)
        flash(f'报表 {filename} 已删除', 'success')
    else:
        flash(f'报表 {filename} 不存在', 'danger')
    
    return redirect(url_for('reports.index'))

@reports_bp.route('/batch_delete', methods=['POST'])
@login_required
def batch_delete():
    """批量删除已生成的报表"""
    if not current_user.is_admin:
        flash('您没有权限删除报表文件', 'danger')
        return redirect(url_for('reports.index'))
    
    # 获取选中的文件列表
    selected_files = request.form.getlist('selected_files')
    
    if not selected_files:
        flash('未选择任何报表文件', 'warning')
        return redirect(url_for('reports.index'))
    
    reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'instance', 'reports')
    
    # 记录成功删除和失败的文件
    deleted_count = 0
    failed_count = 0
    
    for filename in selected_files:
        # 简单的安全检查，防止路径遍历攻击
        if '..' in filename or '/' in filename:
            continue
            
        file_path = os.path.join(reports_dir, filename)
        
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                deleted_count += 1
            except Exception:
                failed_count += 1
    
    if deleted_count > 0:
        flash(f'成功删除 {deleted_count} 个报表文件', 'success')
    
    if failed_count > 0:
        flash(f'有 {failed_count} 个报表文件删除失败', 'danger')
    
    return redirect(url_for('reports.index')) 