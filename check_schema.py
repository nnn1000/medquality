import sqlite3

def check_schema():
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    # 获取表结构
    cursor.execute("PRAGMA table_info(indicators)")
    columns = cursor.fetchall()
    
    print("indicators表结构：")
    for col in columns:
        print(col)
    
    conn.close()

if __name__ == "__main__":
    check_schema() 