import sqlite3

def list_b15_codes():
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    # 查询B15的所有子指标代码
    cursor.execute('SELECT code FROM indicators WHERE code LIKE "B15.%" ORDER BY code')
    codes = cursor.fetchall()
    
    print(f"B15子指标代码列表（共{len(codes)}个）：")
    print("-" * 20)
    for code in codes:
        print(code[0])
    
    conn.close()

if __name__ == "__main__":
    list_b15_codes() 