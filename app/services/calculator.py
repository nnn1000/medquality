import pandas as pd
import numpy as np
from app import db
from app.models.data import RawData, Result, beijing_now
from app.models.indicator import Indicator
from app.models.hospital import Hospital
from app.models.report_period import ReportPeriod
from datetime import datetime, timedelta
import re

class IndicatorCalculator:
    """指标计算服务类"""
    
    @staticmethod
    def calculate_indicator(raw_data_id):
        """根据原始数据ID计算单个指标结果"""
        raw_data = RawData.query.get(raw_data_id)
        if not raw_data:
            print(f"错误: 找不到ID为{raw_data_id}的原始数据")
            return None
        
        # 获取指标
        indicator = Indicator.query.get(raw_data.indicator_id)
        if not indicator:
            print(f"错误: 找不到ID为{raw_data.indicator_id}的指标")
            return None
        
        print(f"开始计算: 指标={indicator.code}, 分子={raw_data.numerator}, 分母={raw_data.denominator}")
        
        # 计算结果
        calculated_value = IndicatorCalculator._compute_value(raw_data, indicator)
        
        print(f"计算结果: {calculated_value}")
        
        if calculated_value is None:
            print(f"警告: 指标{indicator.code}的计算结果为None")
            return None
            
        # 四舍五入到两位小数
        calculated_value = round(calculated_value, 2)
        
        # 判断是否达标
        target_achieved = IndicatorCalculator._check_target_achieved(calculated_value, indicator)
        
        # 检查是否已有计算结果，有则更新，无则创建
        result = Result.query.filter_by(raw_data_id=raw_data_id).first()
        if result:
            result.value = calculated_value
            result.target_achieved = target_achieved
            result.calculation_time = beijing_now()
            print(f"更新已有结果: {result.value}, 达标={result.target_achieved}")
        else:
            result = Result(
                indicator_id=raw_data.indicator_id,
                hospital_id=raw_data.hospital_id,
                period_id=raw_data.period_id,
                raw_data_id=raw_data_id,
                value=calculated_value,
                target_achieved=target_achieved
            )
            db.session.add(result)
            print(f"创建新结果: {result.value}, 达标={result.target_achieved}")
        
        db.session.commit()
        return result
    
    @staticmethod
    def calculate_for_period(period_id, hospital_id=None):
        """计算指定时间周期内的所有指标结果"""
        # 构建查询条件
        query = RawData.query.filter_by(period_id=period_id)
        if hospital_id:
            query = query.filter_by(hospital_id=hospital_id)
        
        raw_data_items = query.all()
        results = []
        
        for raw_data in raw_data_items:
            result = IndicatorCalculator.calculate_indicator(raw_data.id)
            if result:
                results.append(result)
        
        return results
    
    @staticmethod
    def calculate_for_indicator(indicator_id, period_id=None, hospital_id=None):
        """计算指定指标的结果"""
        # 构建查询条件
        query = RawData.query.filter_by(indicator_id=indicator_id)
        if period_id:
            query = query.filter_by(period_id=period_id)
        if hospital_id:
            query = query.filter_by(hospital_id=hospital_id)
        
        raw_data_items = query.all()
        results = []
        
        for raw_data in raw_data_items:
            result = IndicatorCalculator.calculate_indicator(raw_data.id)
            if result:
                results.append(result)
        
        return results
    
    @staticmethod
    def _check_target_achieved(value, indicator):
        """判断指标是否达标"""
        if indicator.target_value is None:
            # 如果没有目标值，则返回None而不是False
            return None
        
        # 提取目标值中的具体数值（如果有的话）
        # 例如从 "逐步降低，≤0.37%" 中提取 0.37
        numeric_match = re.search(r'[≤≥<>]?\s*(\d+(?:\.\d+)?)\s*(?:%|‰)?', indicator.target_value)
        target_number = float(numeric_match.group(1)) / 100 if numeric_match and '%' in indicator.target_value else None
        if target_number is not None:
            # 如果有具体数值目标，使用这个数值进行比较
            if '≤' in indicator.target_value or '<' in indicator.target_value:
                return value <= target_number
            elif '≥' in indicator.target_value or '>' in indicator.target_value:
                return value >= target_number
        
        # 获取指标代码前缀以确定指标类别
        category_prefix = indicator.code[0]
        
        # 根据指标单位和类别判断达标逻辑
        if indicator.unit == '%':
            # 百分比类指标通常是越高越好，除非特殊说明
            # 例如，B类中的输液使用率、D类指标中的不合格率等是越低越好
            if '降低' in indicator.target_value or '低于' in indicator.target_value:
                return True  # 降低类指标没有具体目标值时默认达标
            elif category_prefix == 'B' and re.search(r'输液使用率|不合格率', indicator.name):
                return True  # 这类指标需要降低，没有具体目标值时默认达标
            else:
                return True  # 提高类指标没有具体目标值时默认达标
                
        elif indicator.unit in ['分钟', '小时', '天', '床日', 'ml', '袋/瓶', '个数']:
            # 时间、用量类指标通常是越低越好
            return True  # 没有具体目标值时默认达标
            
        elif indicator.unit == '‰':
            # 千分比指标通常是越低越好（如感染率）
            return True  # 没有具体目标值时默认达标
            
        elif indicator.unit == '个':
            # 例如"开展日间医疗服务的医院占比"指标，值为1表示开展，为达标
            return True  # 没有具体目标值时默认达标
            
        else:
            # 其他类型指标默认以大于等于目标值为达标
            return True  # 没有具体目标值时默认达标
    
    @staticmethod
    def _compute_value(raw_data, indicator):
        """计算指标值，根据不同的指标类型应用不同的计算逻辑"""
        # 获取指标代码前缀以确定指标类别
        category_prefix = indicator.code[0]
        
        # A类 - 急诊和日间医疗质量相关指标
        if category_prefix == 'A':
            return IndicatorCalculator._compute_emergency_indicator(raw_data, indicator)
            
        # B类 - 医疗行为质量相关指标
        elif category_prefix == 'B':
            return IndicatorCalculator._compute_medical_behavior_indicator(raw_data, indicator)
            
        # C类 - 结果质量相关指标
        elif category_prefix == 'C':
            return IndicatorCalculator._compute_result_indicator(raw_data, indicator)
            
        # D类 - 病历质量相关指标
        elif category_prefix == 'D':
            return IndicatorCalculator._compute_medical_record_indicator(raw_data, indicator)
            
        # 默认计算逻辑：比例计算
        return IndicatorCalculator._compute_default(raw_data, indicator)
    
    @staticmethod
    def _compute_emergency_indicator(raw_data, indicator):
        """计算急诊和日间医疗质量相关指标"""
        if indicator.code == 'A01':  # 平均急救响应时间
            if raw_data.numerator is not None and raw_data.denominator is not None and raw_data.denominator > 0:
                return raw_data.numerator / raw_data.denominator
        
        elif indicator.code == 'A05':  # 开展日间医疗服务的医院占比
            # 这是一个是/否指标，直接返回分子值
            return raw_data.numerator
        
        # 其他A类指标默认为百分比计算
        return IndicatorCalculator._compute_default(raw_data, indicator)
    
    @staticmethod
    def _compute_medical_behavior_indicator(raw_data, indicator):
        """计算医疗行为质量相关指标"""
        # 获取指标基本代码
        base_code = indicator.code.split('.')[0] if '.' in indicator.code else indicator.code
        
        print(f"计算医疗行为指标: {indicator.code}, 基本代码: {base_code}, 分子: {raw_data.numerator}, 分母: {raw_data.denominator}")
        
        # 静脉输液相关指标 (B11、B11.1、B12、B13、B14等)
        if base_code in ['B11', 'B12', 'B13', 'B14']:
            # 确保分子和分母有值
            if raw_data.numerator is None:
                print(f"警告: 指标 {indicator.code} 的分子为空")
                return None
                
            if raw_data.denominator is None:
                print(f"警告: 指标 {indicator.code} 的分母为空")
                return None
                
            if raw_data.denominator <= 0:
                print(f"警告: 指标 {indicator.code} 的分母必须大于0，当前值: {raw_data.denominator}")
                return None
                
            try:
                # 特别注意：分子可以为0，表示没有对应的事件发生
                # B11和B11.1是百分比指标
                if base_code == 'B11' and indicator.unit == '%':
                    result = (raw_data.numerator / raw_data.denominator) * 100
                    print(f"B11系列百分比计算结果: {result}%")
                    return result
                else:
                    result = raw_data.numerator / raw_data.denominator
                    print(f"B系列比值计算结果: {result}")
                    return result
            except Exception as e:
                print(f"B类指标计算异常: {str(e)}")
                return None
        
        # 其他B类指标默认为百分比计算
        return IndicatorCalculator._compute_default(raw_data, indicator)
    
    @staticmethod
    def _compute_result_indicator(raw_data, indicator):
        """计算结果质量相关指标"""
        if indicator.code == 'C01':  # 医院CMI值
            # CMI值直接作为单一值，无需计算
            return raw_data.numerator
            
        elif indicator.code == 'C09':  # 血管内导管相关血流感染发生率（千分比）
            if raw_data.numerator is not None and raw_data.denominator is not None and raw_data.denominator > 0:
                return (raw_data.numerator / raw_data.denominator) * 1000
        
        # 其他C类指标默认为百分比计算
        return IndicatorCalculator._compute_default(raw_data, indicator)
    
    @staticmethod
    def _compute_medical_record_indicator(raw_data, indicator):
        """计算病历质量相关指标"""
        # D类指标默认为百分比计算
        return IndicatorCalculator._compute_default(raw_data, indicator)
    
    @staticmethod
    def _compute_default(raw_data, indicator):
        """默认的计算逻辑：通常是分子/分母的比例计算"""
        print(f"执行默认计算逻辑: 指标={indicator.code}, 分子={raw_data.numerator}, 分母={raw_data.denominator}")
        
        # 特殊情况：只有分子没有分母（如中位数指标或单一值指标）
        if raw_data.numerator is not None and raw_data.denominator is None:
            print(f"单值指标计算: 直接返回分子值 {raw_data.numerator}")
            return raw_data.numerator
        
        # 检查分子和分母是否为None
        if raw_data.numerator is None:
            print(f"错误：分子为None")
            return None
            
        if raw_data.denominator is None:
            print(f"错误：分母为None")
            return None
        
        # 检查分母是否为0（除数不能为0）
        if raw_data.denominator == 0:
            print(f"错误：分母为0，无法进行除法运算")
            return None
            
        try:
            # 基础情况：分子/分母比例计算
            # 根据指标类型决定计算公式
            if indicator.unit == '%':
                # 百分比指标
                result = (raw_data.numerator / raw_data.denominator) * 100
                print(f"百分比计算结果: {result}%")
                return result
            else:
                # 其他比例指标
                result = raw_data.numerator / raw_data.denominator
                print(f"比值计算结果: {result}")
                return result
        except Exception as e:
            print(f"计算过程中发生异常: {str(e)}")
            return None
    
    @staticmethod
    def get_results_dataframe(period_id, hospital_id=None, category_id=None):
        """获取指定条件下的结果数据框"""
        # 构建查询
        query = db.session.query(
            Result.id, 
            Result.value, 
            Result.target_achieved,
            Result.calculation_time,
            Indicator.code,
            Indicator.name.label('indicator_name'),
            Indicator.target_value,
            Indicator.unit,
            Hospital.name.label('hospital_name'),
            ReportPeriod.name.label('period_name'),
            RawData.numerator,
            RawData.denominator
        ).join(
            Indicator, Result.indicator_id == Indicator.id
        ).join(
            Hospital, Result.hospital_id == Hospital.id
        ).join(
            ReportPeriod, Result.period_id == ReportPeriod.id
        ).join(
            RawData, Result.raw_data_id == RawData.id, isouter=True
        ).filter(
            Result.period_id == period_id
        )
        
        if hospital_id:
            query = query.filter(Result.hospital_id == hospital_id)
        
        if category_id:
            query = query.filter(Indicator.category_id == category_id)
        
        # 执行查询并转换为pandas数据框
        results = query.all()
        if not results:
            # 返回一个空的数据框，但确保包含所有必需的列
            print("警告: 查询结果为空，返回空数据框")
            empty_df = pd.DataFrame(columns=[
                'id', 'value', 'target_achieved', 'calculation_time', 
                'code', 'indicator_name', 'target_value', 'unit',
                'hospital_name', 'period_name', 'numerator', 'denominator'
            ])
            return empty_df
        
        # 创建数据框
        df = pd.DataFrame(results, columns=[
            'id', 'value', 'target_achieved', 'calculation_time', 
            'code', 'indicator_name', 'target_value', 'unit',
            'hospital_name', 'period_name', 'numerator', 'denominator'
        ])
        
        # 确保分子分母列存在且有值（调试信息）
        print(f"DataFrame包含分子列: {'numerator' in df.columns}")
        print(f"DataFrame包含分母列: {'denominator' in df.columns}")
        print(f"分子非空值数量: {df['numerator'].count()}")
        print(f"分母非空值数量: {df['denominator'].count()}")
        
        return df 