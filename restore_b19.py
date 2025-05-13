import sqlite3
from datetime import datetime

def restore_b19():
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    # Insert the B19 indicator
    cursor.execute('''
        INSERT INTO indicators (
            code, 
            name, 
            frequency, 
            target_value,
            definition,
            category_id,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        'B19',
        '中医医疗机构中以中医治疗为主的出院患者比例',
        '月度',
        None,  # target_value as NULL since it's a monitoring indicator
        '中医医疗机构中以中医治疗为主的出院患者比例指标',
        2,  # category_id for 医疗行为质量
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ))
    
    conn.commit()
    conn.close()
    print("B19 indicator has been added.")

if __name__ == "__main__":
    restore_b19() 