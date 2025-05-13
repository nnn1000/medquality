import sqlite3

def check_b19i():
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT code, name
        FROM indicators 
        WHERE code = "B19I"
    ''')
    
    indicator = cursor.fetchone()
    
    if indicator:
        print("B19I仍然存在：")
        print(f"指标代码: {indicator[0]}")
        print(f"指标名称: {indicator[1]}")
    else:
        print("B19I已成功删除！")
    
    conn.close()

if __name__ == "__main__":
    check_b19i() 