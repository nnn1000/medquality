import sqlite3
from datetime import datetime

def add_b15_9():
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    # 添加B15.9康复评定率
    cursor.execute('''
        INSERT INTO indicators (
            code, name, definition, numerator_description, denominator_description,
            calculation_formula, data_source, unit, frequency, category_id, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        'B15.9',
        '康复评定率',
        '康复评定的住院患者人数占同期住院患者总人数的比例',
        '康复评定的住院患者人数',
        '同期住院患者总人数',
        '(康复评定的住院患者人数 ÷ 同期住院患者总人数) × 100%',
        '医院填报',
        '%',
        '季度',
        2,  # category_id
        datetime.now()
    ))
    
    conn.commit()
    conn.close()
    print('已添加B15.9康复评定率。')

if __name__ == "__main__":
    add_b15_9() 