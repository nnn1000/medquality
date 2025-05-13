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
    # 使用2025年第1季度，ID为55
    test_period_id = 55
    test_period = ReportPeriod.query.get(test_period_id)
    if not test_period:
        print(f"找不到ID为{test_period_id}的报告周期")
    else:
        print(f"测试报告周期: {test_period.name} (ID: {test_period.id})")
        
        # 获取所有医院
        hospitals = Hospital.query.all()
        print(f"找到 {len(hospitals)} 家医院")
        
        # 获取全部数据
        print("获取所有数据...")
        df_all = IndicatorCalculator.get_results_dataframe(test_period.id)
        print(f"总数据条数: {len(df_all)}")
        
        # 查看哪些医院有数据
        if len(df_all) > 0:
            hospital_counts = df_all.groupby('hospital_name').size()
            print("\n各医院数据条数:")
            for hospital_name, count in hospital_counts.items():
                print(f"  {hospital_name}: {count}条")
        
        # 生成所有医院的报表
        print("\n生成各医院报表...")
        for hospital in hospitals:
            print(f"\n医院: {hospital.name} (ID: {hospital.id})")
            try:
                hospital_df = IndicatorCalculator.get_results_dataframe(test_period.id, hospital.id)
                print(f"  数据条数: {len(hospital_df)}")
                
                if len(hospital_df) > 0:
                    report_path = ReportGenerator.generate_excel_report(test_period.id, hospital.id)
                    print(f"  报表已生成: {report_path}")
                else:
                    print("  无数据，将生成空报表")
                    report_path = ReportGenerator._generate_standard_report(hospital_df, test_period, hospital)
                    if report_path:
                        print(f"  空报表已生成: {report_path}")
                    else:
                        print("  空报表生成失败")
            except Exception as e:
                print(f"  生成报表时出错: {str(e)}")
                import traceback
                traceback.print_exc()
        
        # 生成汇总报表
        print("\n生成汇总报表...")
        try:
            summary_report_path = ReportGenerator.generate_excel_report(test_period.id, report_type='summary')
            print(f"汇总报表已生成: {summary_report_path}")
        except Exception as e:
            print(f"生成汇总报表时出错: {str(e)}")
            import traceback
            traceback.print_exc() 