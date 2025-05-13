import sqlite3

def check_categories():
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    # 获取所有类别
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()
    
    print("所有类别：")
    for category in categories:
        print(category)
    
    conn.close()

if __name__ == "__main__":
    check_categories() 