import sqlite3

def check_b15():
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    # 查询B15主指标
    cursor.execute('SELECT * FROM indicators WHERE code = "B15"')
    main = cursor.fetchone()
    
    if main:
        print("B15主指标信息：")
        print("-" * 100)
        print(f"指标代码: {main[0]}")
        print(f"指标名称: {main[1]}")
        print(f"指标导向: {main[2] if main[2] else '无'}")
        print(f"监测频率: {main[3] if main[3] else '无'}")
        print(f"是否有子指标: {main[4]}")
        print("-" * 100)
    else:
        print("未找到B15主指标！")
    
    # 查询B15的所有子指标
    cursor.execute('SELECT * FROM indicators WHERE code LIKE "B15.%" ORDER BY code')
    children = cursor.fetchall()
    
    print(f"\nB15共有{len(children)}个子指标：")
    print("-" * 100)
    print(f"{'指标代码':<10} {'指标名称':<30} {'指标导向':<50} {'监测频率':<10} {'是否有子指标':<10}")
    print("-" * 100)
    
    for child in children:
        code, name, target_value, frequency, has_children = child
        print(f"{code:<10} {name:<30} {target_value if target_value else '无':<50} {frequency if frequency else '无':<10} {has_children:<10}")
    
    conn.close()

if __name__ == "__main__":
    check_b15()

 