import pandas as pd
import os
from datetime import datetime
from app.services.calculator import IndicatorCalculator
from app.models.indicator import Indicator, IndicatorCategory
from app.models.hospital import Hospital
from app.models.report_period import ReportPeriod
from flask import current_app

class ReportGenerator:
    """报表生成服务类"""
    
    @staticmethod
    def generate_excel_report(period_id, hospital_id=None, report_type='standard'):
        """
        生成Excel格式的报表
        
        参数:
        - period_id: 报告周期ID
        - hospital_id: 医院ID（可选，如果不提供则生成所有医院的报告）
        - report_type: 报告类型，可选值: 'standard'(标准报告), 'detailed'(详细报告), 'summary'(汇总报告)
        
        返回值:
        - 生成的Excel文件路径
        """
        # 获取报告周期信息
        period = ReportPeriod.query.get(period_id)
        if not period:
            raise ValueError("无效的报告周期ID")
            
        # 验证报告周期是否有效
        if not period.start_date or not period.end_date:
            raise ValueError("报告周期缺少起止日期")
            
        # 获取医院信息
        hospital = None
        if hospital_id:
            hospital = Hospital.query.get(hospital_id)
            if not hospital:
                raise ValueError("无效的医院ID")
        
        # 获取结果数据
        df = IndicatorCalculator.get_results_dataframe(period_id, hospital_id)
        if df.empty:
            return None
        
        # 根据报告类型调用不同的报告生成函数
        if report_type == 'standard':
            return ReportGenerator._generate_standard_report(df, period, hospital)
        elif report_type == 'detailed':
            return ReportGenerator._generate_detailed_report(df, period, hospital)
        elif report_type == 'summary':
            return ReportGenerator._generate_summary_report(df, period)
        else:
            return None
    
    @staticmethod
    def _generate_standard_report(df, period, hospital=None):
        """生成标准报告"""
        try:
            # 打印数据框信息用于调试
            print("报表生成 - 数据框信息:")
            print(f"数据框列: {df.columns.tolist()}")
            print(f"数据框行数: {len(df)}")
            
            # 检查数据框是否为空
            if len(df) == 0:
                print("警告: 数据框为空，将生成空报表")
            
            # 检查是否有必要的列
            required_columns = ['code', 'indicator_name', 'value', 'target_value', 'unit', 'target_achieved']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                print(f"警告: 数据框缺少以下必要列: {missing_columns}")
                print("将使用默认值填充")
                for col in missing_columns:
                    df[col] = None
            
            # 检查分子分母列
            if 'numerator' not in df.columns:
                print("警告: 数据框中没有分子列，将添加空列")
                df['numerator'] = None
            
            if 'denominator' not in df.columns:
                print("警告: 数据框中没有分母列，将添加空列")
                df['denominator'] = None
            
            print(f"分子列缺失值比例: {df['numerator'].isna().mean() * 100:.2f}%")
            print(f"分母列缺失值比例: {df['denominator'].isna().mean() * 100:.2f}%")
            
            # 设置Excel Writer
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            file_name = f"医疗质量指标报告_{period.name}"
            if hospital:
                file_name += f"_{hospital.name}"
            file_name += f"_{timestamp}.xlsx"
            
            # 创建报告保存目录
            reports_dir = os.path.join(current_app.instance_path, 'reports')
            os.makedirs(reports_dir, exist_ok=True)
            file_path = os.path.join(reports_dir, file_name)
            
            # 创建Excel writer
            writer = pd.ExcelWriter(file_path, engine='openpyxl')
            
            # 按指标类别分组
            # 获取所有指标类别
            categories = IndicatorCategory.query.all()
            
            # 添加汇总表，使用安全的方式获取列
            if len(df) > 0:
                df_summary = df[['code', 'indicator_name', 'numerator', 'denominator', 'value', 'target_value', 'unit', 'target_achieved']]
                df_summary = df_summary.rename(columns={
                    'code': '指标编码',
                    'indicator_name': '指标名称',
                    'numerator': '分子',
                    'denominator': '分母',
                    'value': '指标值',
                    'target_value': '目标值',
                    'unit': '单位',
                    'target_achieved': '是否达标'
                })
                # 确保是否达标列有值，并处理None值
                df_summary['是否达标'] = df_summary['是否达标'].map({True: '是', False: '否', None: '/'})
            else:
                # 创建一个空的数据框，但包含所有必要的列
                df_summary = pd.DataFrame(columns=[
                    '指标编码', '指标名称', '分子', '分母', '指标值', '目标值', '单位', '是否达标'
                ])
            
            df_summary.to_excel(writer, sheet_name='汇总', index=False)
            
            # 设置列宽
            worksheet = writer.sheets['汇总']
            worksheet.column_dimensions['A'].width = 12  # 指标编码
            worksheet.column_dimensions['B'].width = 40  # 指标名称
            worksheet.column_dimensions['C'].width = 15  # 分子
            worksheet.column_dimensions['D'].width = 15  # 分母
            worksheet.column_dimensions['E'].width = 12  # 指标值
            worksheet.column_dimensions['F'].width = 15  # 目标值
            worksheet.column_dimensions['G'].width = 8   # 单位
            worksheet.column_dimensions['H'].width = 10  # 是否达标
            
            # 为每个类别创建工作表
            for category in categories:
                # 获取当前类别的指标ID
                indicators = Indicator.query.filter_by(category_id=category.id).order_by(*Indicator.numeric_code_order()).all()
                indicator_ids = [ind.id for ind in indicators]
                
                # 过滤数据框中的相关指标
                if len(df) > 0 and 'code' in df.columns:
                    try:
                        category_df = df[df['code'].str.startswith(category.name[0])]
                    except (AttributeError, KeyError) as e:
                        print(f"警告: 过滤类别 {category.name} 时出错: {str(e)}")
                        category_df = pd.DataFrame(columns=df.columns)
                else:
                    # 空数据框情况
                    category_df = pd.DataFrame(columns=df.columns)
                
                if not category_df.empty:
                    # 按照正确的数字顺序排序子类别
                    try:
                        category_df['sort_key'] = category_df['code'].apply(
                            lambda x: float(x.split('.')[-1]) if '.' in x else 0
                        )
                        category_df = category_df.sort_values(['code', 'sort_key'])
                        category_df = category_df.drop('sort_key', axis=1)
                    except Exception as e:
                        print(f"警告: 排序类别 {category.name} 时出错: {str(e)}")
                    
                    # 整理数据
                    category_df = category_df[['code', 'indicator_name', 'numerator', 'denominator', 'value', 'target_value', 'unit', 'target_achieved']]
                    category_df = category_df.rename(columns={
                        'code': '指标编码',
                        'indicator_name': '指标名称',
                        'numerator': '分子',
                        'denominator': '分母',
                        'value': '指标值',
                        'target_value': '目标值',
                        'unit': '单位',
                        'target_achieved': '是否达标'
                    })
                    category_df['是否达标'] = category_df['是否达标'].map({True: '是', False: '否', None: '/'})
                else:
                    # 创建一个空的数据框，但包含所有必要的列
                    category_df = pd.DataFrame(columns=[
                        '指标编码', '指标名称', '分子', '分母', '指标值', '目标值', '单位', '是否达标'
                    ])
                
                # 保存到Excel
                category_df.to_excel(writer, sheet_name=category.name, index=False)
                
                # 设置列宽
                worksheet = writer.sheets[category.name]
                worksheet.column_dimensions['A'].width = 12  # 指标编码
                worksheet.column_dimensions['B'].width = 40  # 指标名称
                worksheet.column_dimensions['C'].width = 15  # 分子
                worksheet.column_dimensions['D'].width = 15  # 分母
                worksheet.column_dimensions['E'].width = 12  # 指标值
                worksheet.column_dimensions['F'].width = 15  # 目标值
                worksheet.column_dimensions['G'].width = 8   # 单位
                worksheet.column_dimensions['H'].width = 10  # 是否达标
            
            # 保存文件
            writer.close()
            
            print(f"报表已成功生成: {file_path}")
            return file_path
        except Exception as e:
            print(f"生成报表时出错: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    @staticmethod
    def _generate_detailed_report(df, period, hospital=None):
        """生成详细报告，包含更多分析信息"""
        # 这里可以添加更详细的分析逻辑
        # 为简化示例，暂时沿用标准报告的实现
        return ReportGenerator._generate_standard_report(df, period, hospital)
    
    @staticmethod
    def _generate_summary_report(df, period):
        """生成汇总报告，比较多家医院的指标结果"""
        # 设置Excel Writer
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"医疗质量指标汇总报告_{period.name}_{timestamp}.xlsx"
        
        # 创建报告保存目录
        reports_dir = os.path.join(current_app.instance_path, 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        file_path = os.path.join(reports_dir, file_name)
        
        # 创建Excel writer
        writer = pd.ExcelWriter(file_path, engine='openpyxl')
        
        # 数据透视处理，按医院和指标分组
        pivot_df = df.pivot_table(
            values='value',
            index=['code', 'indicator_name', 'unit', 'target_value'],
            columns=['hospital_name'],
            aggfunc='first'
        ).reset_index()
        
        pivot_df = pivot_df.rename(columns={
            'code': '指标编码',
            'indicator_name': '指标名称',
            'unit': '单位',
            'target_value': '目标值'
        })
        
        # 保存到Excel
        pivot_df.to_excel(writer, sheet_name='医院指标对比', index=False)
        
        # 添加分子数据表
        numerator_df = df.pivot_table(
            values='numerator',
            index=['code', 'indicator_name'],
            columns=['hospital_name'],
            aggfunc='first'
        ).reset_index()
        
        numerator_df = numerator_df.rename(columns={
            'code': '指标编码',
            'indicator_name': '指标名称'
        })
        
        numerator_df.to_excel(writer, sheet_name='分子数据对比', index=False)
        
        # 设置分子表列宽
        worksheet = writer.sheets['分子数据对比']
        worksheet.column_dimensions['A'].width = 12  # 指标编码
        worksheet.column_dimensions['B'].width = 40  # 指标名称
        # 医院列从C列开始
        for col_idx, _ in enumerate(numerator_df.columns[2:], 3):
            col_letter = chr(64 + col_idx)  # A的ASCII码是65，所以从C(67)开始
            worksheet.column_dimensions[col_letter].width = 15
        
        # 添加分母数据表
        denominator_df = df.pivot_table(
            values='denominator',
            index=['code', 'indicator_name'],
            columns=['hospital_name'],
            aggfunc='first'
        ).reset_index()
        
        denominator_df = denominator_df.rename(columns={
            'code': '指标编码',
            'indicator_name': '指标名称'
        })
        
        denominator_df.to_excel(writer, sheet_name='分母数据对比', index=False)
        
        # 设置分母表列宽
        worksheet = writer.sheets['分母数据对比']
        worksheet.column_dimensions['A'].width = 12  # 指标编码
        worksheet.column_dimensions['B'].width = 40  # 指标名称
        # 医院列从C列开始
        for col_idx, _ in enumerate(denominator_df.columns[2:], 3):
            col_letter = chr(64 + col_idx)  # A的ASCII码是65，所以从C(67)开始
            worksheet.column_dimensions[col_letter].width = 15
        
        # 添加达标情况表
        target_df = df.pivot_table(
            values='target_achieved',
            index=['code', 'indicator_name'],
            columns=['hospital_name'],
            aggfunc='first'
        ).reset_index()
        
        target_df = target_df.rename(columns={
            'code': '指标编码',
            'indicator_name': '指标名称'
        })
        
        # 将布尔值转换为是/否
        for col in target_df.columns:
            if col not in ['指标编码', '指标名称']:
                target_df[col] = target_df[col].map({True: '是', False: '否'})
        
        target_df.to_excel(writer, sheet_name='达标情况对比', index=False)
        
        # 保存文件
        writer.close()
        
        return file_path 