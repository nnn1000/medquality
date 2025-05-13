import sqlite3
from datetime import datetime

def add_b15_8():
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    # 添加B15.8早期康复介入率（髋、膝关节置换术）
    cursor.execute('''
        INSERT INTO indicators (
            code, name, definition, numerator_description, denominator_description,
            calculation_formula, data_source, unit, frequency, category_id, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        'B15.8',
        '早期康复介入率（髋、膝关节置换术）',
        '髋、膝关节置换术患者早期康复介入人数占同期髋、膝关节置换术患者总人数的比例',
        '髋、膝关节置换术患者早期康复介入人数',
        '同期髋、膝关节置换术患者总人数',
        '(髋、膝关节置换术患者早期康复介入人数 ÷ 同期髋、膝关节置换术患者总人数) × 100%',
        '医院填报',
        '%',
        '季度',
        2,  # category_id
        datetime.now()
    ))
    
    conn.commit()
    conn.close()
    print('已添加B15.8早期康复介入率（髋、膝关节置换术）。')

if __name__ == "__main__":
    add_b15_8() 