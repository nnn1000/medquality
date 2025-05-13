import sqlite3

def check_b_indicators():
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    # 获取所有B类指标
    cursor.execute('''
        SELECT code, name, category_id
        FROM indicators
        WHERE code LIKE 'B%'
        ORDER BY code
    ''')
    
    indicators = cursor.fetchall()
    
    print("B类指标列表：")
    print("-" * 80)
    
    # 检查是否有缺失的编号
    expected_codes = set(f'B{i:02d}' for i in range(1, 26))
    actual_codes = set(code for code, _, _ in indicators)
    missing_codes = expected_codes - actual_codes
    
    if missing_codes:
        print("\n缺失的指标代码：")
        for code in sorted(missing_codes):
            print(f"  - {code}")
    
    print("\n现有指标：")
    for code, name, category_id in indicators:
        print(f"  {code}: {name} (类别ID: {category_id})")
    
    conn.close()

if __name__ == "__main__":
    check_b_indicators() 