import sqlite3
from datetime import datetime

def add_b14():
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    # 添加B14指标
    cursor.execute('''
        INSERT INTO indicators (
            code, name, definition, numerator_description, 
            denominator_description, calculation_formula, 
            data_source, unit, frequency, category_id, created_at
        ) VALUES (
            'B14', '室间质评项目合格率', 
            '室间质评合格项目数占同期参加室间质评项目总数的比例',
            '室间质评合格项目数',
            '同期参加室间质评项目总数',
            '(室间质评合格项目数 ÷ 同期参加室间质评项目总数) × 100%',
            '医院填报',
            '%',
            '季度',
            2,
            ?
        )
    ''', (datetime.now(),))
    
    conn.commit()
    conn.close()
    print('已添加B14-室间质评项目合格率指标。')

if __name__ == "__main__":
    add_b14() 