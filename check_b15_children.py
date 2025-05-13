import sqlite3

def check_b15_children():
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    # 查询B15的所有子指标
    cursor.execute('SELECT code, name, target_value FROM indicators WHERE code LIKE "B15.%" ORDER BY code')
    children = cursor.fetchall()
    
    print(f"B15共有{len(children)}个子指标：")
    print("-" * 100)
    print(f"{'指标代码':<10} {'指标名称':<30} {'指标导向':<50}")
    print("-" * 100)
    
    for child in children:
        code, name, target_value = child
        print(f"{code:<10} {name:<30} {target_value if target_value else '无':<50}")
    
    conn.close()

if __name__ == "__main__":
    check_b15_children() 