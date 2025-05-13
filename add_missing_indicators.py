from app import create_app, db
from app.models.indicator import Indicator, IndicatorCategory
import sqlite3
from datetime import datetime

# 创建应用上下文
app = create_app()
app.app_context().push()

# 获取医疗行为质量指标类别ID
category = IndicatorCategory.query.filter_by(name='医疗行为质量').first()
if not category:
    print("错误：找不到医疗行为质量指标类别！")
    exit(1)

category_id = category.id
print(f"医疗行为质量类别ID: {category_id}")

# 定义缺失的医疗行为质量指标数据
indicators_data = [
    {
        'code': 'B17',
        'name': '门急诊患者预防性使用抗菌药物比例',
        'definition': '门（急）诊患者预防性使用抗菌药物处方数占同期门（急）诊患者开具抗菌药物处方总数的比例',
        'calculation_formula': '(门（急）诊患者预防性使用抗菌药物处方数 ÷ 同期门（急）诊患者开具抗菌药物处方总数) × 100%',
        'numerator_description': '门（急）诊患者预防性使用抗菌药物处方数',
        'denominator_description': '同期门（急）诊患者开具抗菌药物处方总数',
        'data_source': '医院填报',
        'unit': '%',
        'target_value': None,
        'frequency': '季度',
        'category_id': category_id
    },
    {
        'code': 'B18',
        'name': '住院患者预防性使用抗菌药物比例',
        'definition': '住院患者预防性使用抗菌药物人次数占同期住院患者使用抗菌药物总人次数的比例',
        'calculation_formula': '(住院患者预防性使用抗菌药物人次数 ÷ 同期住院患者使用抗菌药物总人次数) × 100%',
        'numerator_description': '住院患者预防性使用抗菌药物人次数',
        'denominator_description': '同期住院患者使用抗菌药物总人次数',
        'data_source': '医院填报',
        'unit': '%',
        'target_value': None,
        'frequency': '季度',
        'category_id': category_id
    },
    {
        'code': 'B19',
        'name': '特殊监控微生物检出变化率',
        'definition': '本季度特殊监控微生物检出率与上季度相比较的变化率',
        'calculation_formula': '[(本季度特殊监控微生物检出率 - 上季度特殊监控微生物检出率) ÷ 上季度特殊监控微生物检出率] × 100%',
        'numerator_description': '本季度特殊监控微生物检出率与上季度特殊监控微生物检出率的差值',
        'denominator_description': '上季度特殊监控微生物检出率',
        'data_source': '医院填报',
        'unit': '%',
        'target_value': None,
        'frequency': '季度',
        'category_id': category_id
    }
]

# 导入指标数据
indicators_count = 0
for indicator_data in indicators_data:
    # 检查指标是否已存在
    existing = Indicator.query.filter_by(code=indicator_data['code']).first()
    if not existing:
        indicator = Indicator(**indicator_data)
        db.session.add(indicator)
        indicators_count += 1
        print(f"添加指标: {indicator_data['code']} - {indicator_data['name']}")
    else:
        print(f"指标已存在: {indicator_data['code']} - {indicator_data['name']}")

# 提交更改
db.session.commit()

# 再次检查是否所有指标都存在
missing = []
for code in ['B17', 'B18', 'B19']:
    if not Indicator.query.filter_by(code=code).first():
        missing.append(code)

if missing:
    print(f"警告：仍有指标缺失：{', '.join(missing)}")
else:
    print("所有缺失的指标已成功添加！")

print(f"成功导入 {indicators_count} 个缺失的医疗质量指标")
print("所有40个指标导入已全部完成")

def add_missing_indicators():
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    # 准备要添加的指标数据
    new_indicators = [
        ('B20', '住院患者抗菌药物使用率', '住院患者使用抗菌药物的例次数/同期住院患者总例次数×100%', 
         '住院患者使用抗菌药物的例次数', '同期住院患者总例次数', '住院患者使用抗菌药物的例次数÷同期住院患者总例次数×100%',
         '病案首页', 0.0, '%', '月度', 2),
        
        ('B21', '住院患者抗菌药物使用强度', '住院患者抗菌药物使用强度（DDDs）=抗菌药物消耗量（累计DDD数）/同期收治患者人天数×100',
         '抗菌药物消耗量（累计DDD数）', '同期收治患者人天数', '抗菌药物消耗量（累计DDD数）÷同期收治患者人天数×100',
         '病案首页', 0.0, 'DDDs/100人天', '月度', 2),
        
        ('B22', '门诊患者抗菌药物使用率', '门诊患者使用抗菌药物的例次数/同期门诊患者总例次数×100%',
         '门诊患者使用抗菌药物的例次数', '同期门诊患者总例次数', '门诊患者使用抗菌药物的例次数÷同期门诊患者总例次数×100%',
         '门诊处方', 0.0, '%', '月度', 2),
        
        ('B23', '急诊患者抗菌药物使用率', '急诊患者使用抗菌药物的例次数/同期急诊患者总例次数×100%',
         '急诊患者使用抗菌药物的例次数', '同期急诊患者总例次数', '急诊患者使用抗菌药物的例次数÷同期急诊患者总例次数×100%',
         '急诊处方', 0.0, '%', '月度', 2),
        
        ('B24', '住院患者抗菌药物使用前微生物送检率', '住院患者使用抗菌药物前微生物送检的例次数/同期住院患者使用抗菌药物的例次数×100%',
         '住院患者使用抗菌药物前微生物送检的例次数', '同期住院患者使用抗菌药物的例次数', '住院患者使用抗菌药物前微生物送检的例次数÷同期住院患者使用抗菌药物的例次数×100%',
         '病案首页', 0.0, '%', '月度', 2),
        
        ('B25', '住院患者抗菌药物使用前微生物送检率（限制使用级）', '住院患者使用限制使用级抗菌药物前微生物送检的例次数/同期住院患者使用限制使用级抗菌药物的例次数×100%',
         '住院患者使用限制使用级抗菌药物前微生物送检的例次数', '同期住院患者使用限制使用级抗菌药物的例次数', '住院患者使用限制使用级抗菌药物前微生物送检的例次数÷同期住院患者使用限制使用级抗菌药物的例次数×100%',
         '病案首页', 0.0, '%', '月度', 2)
    ]
    
    # 添加新指标
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for indicator in new_indicators:
        cursor.execute('''
            INSERT INTO indicators (
                code, name, definition, numerator_description, denominator_description,
                calculation_formula, data_source, target_value, unit, frequency,
                category_id, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', indicator + (current_time,))
    
    # 提交更改
    conn.commit()
    
    print("已添加以下指标：")
    for code, name, *_ in new_indicators:
        print(f"  - {code}: {name}")
    
    conn.close()

if __name__ == "__main__":
    add_missing_indicators() 