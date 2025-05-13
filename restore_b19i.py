import sqlite3
from datetime import datetime

def restore_b19i():
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    # Insert the main B19I indicator
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
        'B19I',
        '医院感染发生率',
        '月度',
        None,  # target_value as NULL since it's a monitoring indicator
        '医院感染发生率指标',
        2,  # category_id for 医疗行为质量
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ))
    
    conn.commit()
    conn.close()
    print("B19I main indicator has been restored.")

if __name__ == "__main__":
    restore_b19i() 