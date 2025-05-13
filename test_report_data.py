import sqlite3
import pandas as pd
from app import create_app
from app.services.calculator import IndicatorCalculator
from app.services.report_generator import ReportGenerator
from app.models.report_period import ReportPeriod
from app.models.hospital import Hospital
from app.models.data import RawData, Result

app = create_app()
with app.app_context():
    # 直接使用2025年第1季度，ID为55
    test_period_id = 55
    test_period = ReportPeriod.query.get(test_period_id)
    if not test_period:
        print(f"找不到ID为{test_period_id}的报告周期")
    else:
        print(f"测试报告周期: {test_period.name} (ID: {test_period.id})")
        
        # 获取该周期的原始数据条目
        raw_data_items = RawData.query.filter_by(period_id=test_period.id).all()
        print(f"该周期的原始数据条目数: {len(raw_data_items)}")
        
        # 检查分子分母数据情况
        if raw_data_items:
            has_numerator = sum(1 for item in raw_data_items if item.numerator is not None)
            has_denominator = sum(1 for item in raw_data_items if item.denominator is not None)
            print(f"有分子数据的条目数: {has_numerator}/{len(raw_data_items)}")
            print(f"有分母数据的条目数: {has_denominator}/{len(raw_data_items)}")
            
            # 检查原始数据中的分子分母示例
            if has_numerator > 0 or has_denominator > 0:
                print("\n原始数据示例:")
                for i, item in enumerate(raw_data_items[:5]):  # 只显示前5条
                    indicator = item.indicator
                    print(f"数据 {i+1}: 指标 {indicator.code} ({indicator.name}), 分子: {item.numerator}, 分母: {item.denominator}")
        
        # 检查与结果表的关联
        results = Result.query.filter_by(period_id=test_period.id).all()
        if results:
            linked_results = sum(1 for r in results if r.raw_data_id is not None)
            print(f"该周期的结果条目数: {len(results)}")
            print(f"有关联原始数据的结果条目数: {linked_results}/{len(results)}")
        
        # 使用Calculator获取数据框
        print("\n使用Calculator获取数据...")
        df = IndicatorCalculator.get_results_dataframe(test_period.id)
        print("\n数据框信息:")
        print(f"行数: {len(df)}")
        if len(df) > 0:
            print(f"列: {df.columns.tolist()}")
            if 'numerator' in df.columns and 'denominator' in df.columns:
                print(f"分子非空值数量: {df['numerator'].count()}/{len(df)}")
                print(f"分母非空值数量: {df['denominator'].count()}/{len(df)}")
                
                # 显示部分数据以供查看
                print("\n数据示例 (前5行):")
                sample_df = df[['code', 'indicator_name', 'numerator', 'denominator', 'value']].head()
                print(sample_df)
                
                # 生成测试报表
                print("\n生成报表...")
                hospitals = Hospital.query.all()
                if hospitals:
                    test_hospital = hospitals[0]
                    print(f"测试医院: {test_hospital.name} (ID: {test_hospital.id})")
                    
                    # 直接使用ReportGenerator中的方法，更好地捕获错误
                    try:
                        # 获取特定医院的数据框
                        hospital_df = IndicatorCalculator.get_results_dataframe(test_period.id, test_hospital.id)
                        print(f"该医院数据条数: {len(hospital_df)}")
                        
                        # 直接使用标准报告生成方法
                        from app.services.report_generator import ReportGenerator
                        report_path = ReportGenerator._generate_standard_report(hospital_df, test_period, test_hospital)
                        
                        if report_path:
                            print(f"报表已生成: {report_path}")
                        else:
                            print("报表生成失败")
                    except Exception as e:
                        print(f"生成报表时出错: {str(e)}")
                        import traceback
                        traceback.print_exc()
                else:
                    print("未找到医院数据")
            else:
                print("数据框中没有分子或分母列")
        else:
            print("数据框为空，无法生成报表")