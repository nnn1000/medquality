import sqlite3

def update_b15_4():
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    # 更新B15.4的指标名称和相关信息
    cursor.execute('''
        UPDATE indicators 
        SET name = '早期康复介入率（心血管内科）',
            definition = '心血管内科患者早期康复介入人数占同期心血管内科患者总人数的比例',
            numerator_description = '心血管内科患者早期康复介入人数',
            denominator_description = '同期心血管内科患者总人数',
            calculation_formula = '(心血管内科患者早期康复介入人数 ÷ 同期心血管内科患者总人数) × 100%'
        WHERE code = 'B15.4'
    ''')
    
    conn.commit()
    conn.close()
    print('已更新B15.4为早期康复介入率（心血管内科）。')

if __name__ == "__main__":
    update_b15_4() 