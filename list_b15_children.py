import sqlite3

def list_b15_children():
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    # 查询B15的所有子指标
    cursor.execute('SELECT code, name FROM indicators WHERE code LIKE "B15.%" ORDER BY code')
    children = cursor.fetchall()
    
    print(f"B15子指标列表（共{len(children)}个）：")
    print("-" * 60)
    print(f"{'指标代码':<10} {'指标名称':<50}")
    print("-" * 60)
    
    for code, name in children:
        print(f"{code:<10} {name:<50}")
    
    conn.close()

if __name__ == "__main__":
    list_b15_children() 