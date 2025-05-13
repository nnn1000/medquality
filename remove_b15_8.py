import sqlite3

def remove_b15_8():
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    # 删除B15.8子指标
    cursor.execute('DELETE FROM indicators WHERE code = "B15.8"')
    deleted_count = cursor.rowcount
    
    conn.commit()
    conn.close()
    print(f'已删除{deleted_count}个子指标。')

if __name__ == "__main__":
    remove_b15_8() 