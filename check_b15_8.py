import sqlite3

def check_b15_8():
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT code, name, definition, numerator_description, denominator_description,
               calculation_formula, data_source, unit, frequency
        FROM indicators 
        WHERE code = "B15.8"
    ''')
    
    indicator = cursor.fetchone()
    
    if indicator:
        print("B15.8详细信息：")
        print("-" * 80)
        print(f"指标代码: {indicator[0]}")
        print(f"指标名称: {indicator[1]}")
        print(f"定义: {indicator[2]}")
        print(f"分子: {indicator[3]}")
        print(f"分母: {indicator[4]}")
        print(f"计算公式: {indicator[5]}")
        print(f"数据来源: {indicator[6]}")
        print(f"单位: {indicator[7]}")
        print(f"监测频率: {indicator[8]}")
    else:
        print("未找到B15.8！")
    
    conn.close()

if __name__ == "__main__":
    check_b15_8() 