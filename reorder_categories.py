import sqlite3
from datetime import datetime

def reorder_categories():
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    # 获取当前类别
    cursor.execute('SELECT id, name FROM indicator_categories ORDER BY id')
    categories = cursor.fetchall()
    
    # 打印当前顺序
    print("当前类别顺序：")
    for id, name in categories:
        print(f"ID {id}: {name}")
    
    # 更新类别顺序
    # 1. 急诊和日间医疗质量
    # 2. 医疗行为质量
    # 3. 结果质量
    # 4. 病历质量
    
    # 创建临时表，增加 description 字段
    cursor.execute('''
        CREATE TABLE temp_categories (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP
        )
    ''')
    
    # 新顺序及描述
    new_order = [
        (1, '急诊和日间医疗质量', '急诊和日间医疗相关指标'),
        (2, '医疗行为质量', '医疗行为相关指标'),
        (3, '结果质量', '结果相关指标'),
        (4, '病历质量', '病历相关指标')
    ]
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for id, name, description in new_order:
        cursor.execute('INSERT INTO temp_categories (id, name, description, created_at) VALUES (?, ?, ?, ?)',
                      (id, name, description, current_time))
    
    # 更新原表中的指标类别ID
    for old_id, new_id in [(2, 2), (3, 3), (4, 4)]:  # 保持ID不变，只更新顺序
        cursor.execute('UPDATE indicators SET category_id = ? WHERE category_id = ?',
                      (new_id, old_id))
    
    # 删除原表
    cursor.execute('DROP TABLE indicator_categories')
    
    # 重命名临时表
    cursor.execute('ALTER TABLE temp_categories RENAME TO indicator_categories')
    
    # 提交更改
    conn.commit()
    
    # 验证新顺序
    cursor.execute('SELECT id, name, description FROM indicator_categories ORDER BY id')
    print("\n更新后的类别顺序：")
    for id, name, description in cursor.fetchall():
        print(f"ID {id}: {name} - {description}")
    
    conn.close()

if __name__ == "__main__":
    reorder_categories() 