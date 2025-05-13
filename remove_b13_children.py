import sqlite3

def remove_b13_children():
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM indicators WHERE code LIKE "B13.%"')
    conn.commit()
    conn.close()
    print('B13子指标已删除。')

if __name__ == "__main__":
    remove_b13_children() 