from app import create_app
from app.models.data import RawData, Result
from app.models.indicator import Indicator
from app.services.calculator import IndicatorCalculator
import sys

print("开始测试分子为0的计算...")

app = create_app()
with app.app_context():
    try:
        # 查找第一个B11系列的指标
        indicator = Indicator.query.filter(Indicator.code.like('B11%')).first()
        if not indicator:
            print("错误: 找不到B11系列指标")
            sys.exit(1)
            
        print(f"找到指标: {indicator.code} - {indicator.name}")
        
        # 获取该指标的一条已有数据
        raw_data = RawData.query.filter_by(indicator_id=indicator.id).first()
        if raw_data:
            print(f"找到现有数据: ID={raw_data.id}, 分子={raw_data.numerator}, 分母={raw_data.denominator}")
        else:
            print("未找到现有数据，将创建测试数据")
            
        # 设置分子为0的测试数据
        if not raw_data:
            # 如果没有找到数据，我们需要创建测试数据
            from app.models.hospital import Hospital
            from app.models.report_period import ReportPeriod
            from flask_login import current_user
            
            # 获取第一个医院和报告周期
            hospital = Hospital.query.first()
            period = ReportPeriod.query.first()
            
            if not hospital or not period:
                print("错误: 找不到医院或报告周期")
                sys.exit(1)
                
            raw_data = RawData(
                indicator_id=indicator.id,
                hospital_id=hospital.id,
                period_id=period.id,
                numerator=0,  # 设置分子为0
                denominator=100,  # 设置分母为100
                submitter_id=1,  # 假设ID为1的用户
                note="测试分子为0的情况"
            )
            print(f"创建测试数据: 分子=0, 分母=100")
        else:
            # 如果找到了数据，直接修改它
            raw_data.numerator = 0
            print(f"修改现有数据: ID={raw_data.id}, 设置分子=0")
            
        # 保存数据
        from app import db
        db.session.add(raw_data)
        db.session.commit()
        print(f"保存数据成功: ID={raw_data.id}")
        
        # 尝试计算
        print("开始计算...")
        result = IndicatorCalculator.calculate_indicator(raw_data.id)
        
        if result:
            print(f"计算成功! 结果: {result.value} {indicator.unit}")
            print(f"达标情况: {result.target_achieved}")
        else:
            print("计算失败!")
            print("详细调试信息:")
            print(f"原始数据ID: {raw_data.id}")
            print(f"指标: {indicator.code} - {indicator.name}")
            print(f"分子: {raw_data.numerator}")
            print(f"分母: {raw_data.denominator}")
            
    except Exception as e:
        import traceback
        print(f"测试过程中发生异常: {e}")
        traceback.print_exc()

print("测试完成.") 