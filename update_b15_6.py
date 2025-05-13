import sqlite3

def update_b15_6():
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    # 更新B15.6的指标名称和相关信息
    cursor.execute('''
        UPDATE indicators 
        SET name = '早期康复介入率（脑卒中）',
            definition = '脑卒中患者早期康复介入人数占同期脑卒中患者总人数的比例',
            numerator_description = '脑卒中患者早期康复介入人数',
            denominator_description = '同期脑卒中患者总人数',
            calculation_formula = '(脑卒中患者早期康复介入人数 ÷ 同期脑卒中患者总人数) × 100%'
        WHERE code = 'B15.6'
    ''')
    
    conn.commit()
    conn.close()
    print('已更新B15.6为早期康复介入率（脑卒中）。')

if __name__ == "__main__":
    update_b15_6() 