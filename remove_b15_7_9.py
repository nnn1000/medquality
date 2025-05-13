import sqlite3

def remove_b15_7_9():
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    # 删除B15.7和B15.9子指标
    cursor.execute('DELETE FROM indicators WHERE code IN ("B15.7", "B15.9")')
    deleted_count = cursor.rowcount
    
    conn.commit()
    conn.close()
    print(f'已删除{deleted_count}个子指标。')

if __name__ == "__main__":
    remove_b15_7_9() 