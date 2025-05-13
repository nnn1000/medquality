import sqlite3

def check_b15_raw():
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    # 获取表结构
    cursor.execute("PRAGMA table_info(indicators)")
    columns = cursor.fetchall()
    print("表结构：")
    print("-" * 100)
    for col in columns:
        print(f"列名: {col[1]}, 类型: {col[2]}")
    print("-" * 100)
    
    # 查询B15主指标
    cursor.execute('SELECT * FROM indicators WHERE code = "B15"')
    main = cursor.fetchone()
    
    if main:
        print("\nB15主指标原始数据：")
        print("-" * 100)
        for i, col in enumerate(columns):
            print(f"{col[1]}: {main[i]}")
        print("-" * 100)
    
    # 查询B15的所有子指标
    cursor.execute('SELECT * FROM indicators WHERE code LIKE "B15.%"')
    children = cursor.fetchall()
    
    print(f"\nB15子指标原始数据（共{len(children)}个）：")
    for child in children:
        print("-" * 100)
        for i, col in enumerate(columns):
            print(f"{col[1]}: {child[i]}")
    
    conn.close()

if __name__ == "__main__":
    check_b15_raw() 