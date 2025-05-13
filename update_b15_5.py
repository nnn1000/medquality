import sqlite3

def update_b15_5():
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    # 更新B15.5的指标名称和相关信息
    cursor.execute('''
        UPDATE indicators 
        SET name = '早期康复介入率（重症ICU）',
            definition = '重症ICU患者早期康复介入人数占同期重症ICU患者总人数的比例',
            numerator_description = '重症ICU患者早期康复介入人数',
            denominator_description = '同期重症ICU患者总人数',
            calculation_formula = '(重症ICU患者早期康复介入人数 ÷ 同期重症ICU患者总人数) × 100%'
        WHERE code = 'B15.5'
    ''')
    
    conn.commit()
    conn.close()
    print('已更新B15.5为早期康复介入率（重症ICU）。')

if __name__ == "__main__":
    update_b15_5() 