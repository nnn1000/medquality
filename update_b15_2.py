import sqlite3

def update_b15_2():
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    # 更新B15.2的指标名称和相关信息
    cursor.execute('''
        UPDATE indicators 
        SET name = '早期康复介入率（神经外科）',
            definition = '神经外科患者早期康复介入人数占同期神经外科患者总人数的比例',
            numerator_description = '神经外科患者早期康复介入人数',
            denominator_description = '同期神经外科患者总人数',
            calculation_formula = '(神经外科患者早期康复介入人数 ÷ 同期神经外科患者总人数) × 100%'
        WHERE code = 'B15.2'
    ''')
    
    conn.commit()
    conn.close()
    print('已更新B15.2为早期康复介入率（神经外科）。')

if __name__ == "__main__":
    update_b15_2() 