import sqlite3

def delete_b19i():
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    # 删除B19I指标（不区分大小写）
    cursor.execute('DELETE FROM indicators WHERE UPPER(code) = "B19I"')
    
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    
    if rows_affected > 0:
        print(f'已删除B19I-医院感染发生率指标。')
    else:
        print('未找到B19I指标。')

if __name__ == "__main__":
    delete_b19i()

 