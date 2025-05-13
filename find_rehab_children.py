import sqlite3

def find_rehab_children():
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    # 首先找到早期康复介入率的主指标
    cursor.execute('SELECT id, code, name FROM indicators WHERE name LIKE "%早期康复介入率%" AND code NOT LIKE "%.%"')
    main = cursor.fetchone()
    
    if main:
        print(f"主指标信息：")
        print(f"ID: {main[0]}")
        print(f"代码: {main[1]}")
        print(f"名称: {main[2]}")
        print("-" * 80)
        
        # 查找所有子指标
        cursor.execute('''
            SELECT code, name, definition, numerator_description, denominator_description, calculation_formula, data_source, unit, frequency
            FROM indicators 
            WHERE code LIKE ? AND code LIKE "%.%"
            ORDER BY code
        ''', (f"{main[1]}.%",))
        
        children = cursor.fetchall()
        print(f"子指标列表（共{len(children)}个）：")
        print("-" * 80)
        print(f"{'指标代码':<10} {'指标名称':<30} {'监测频率':<10} {'单位':<10}")
        print("-" * 80)
        
        for child in children:
            code, name, definition, numerator, denominator, formula, source, unit, frequency = child
            print(f"{code:<10} {name:<30} {frequency:<10} {unit:<10}")
            print(f"定义: {definition}")
            print(f"分子: {numerator}")
            print(f"分母: {denominator}")
            print(f"计算公式: {formula}")
            print(f"数据来源: {source}")
            print("-" * 80)
    else:
        print("未找到早期康复介入率主指标！")
    
    conn.close()

if __name__ == "__main__":
    find_rehab_children() 