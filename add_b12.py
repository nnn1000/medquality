import sqlite3
from datetime import datetime

def add_b12():
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    # 添加B12指标
    cursor.execute('''
        INSERT INTO indicators (
            code, name, definition, numerator_description, 
            denominator_description, calculation_formula, 
            data_source, unit, frequency, category_id, created_at
        ) VALUES (
            'B12', '危急值报告及时率', 
            '危急值报告及时数占同期危急值报告总数的比例',
            '危急值报告及时数',
            '同期危急值报告总数',
            '(危急值报告及时数 ÷ 同期危急值报告总数) × 100%',
            '医院填报',
            '%',
            '季度',
            2,
            ?
        )
    ''', (datetime.now(),))
    
    conn.commit()
    conn.close()
    print('已添加B12-危急值报告及时率指标。')

if __name__ == "__main__":
    add_b12() 