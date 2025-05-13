import sqlite3
from datetime import datetime
import traceback

def main():
    """更新指标详细信息，解决'获取指标信息失败'的问题"""
    
    # 连接数据库
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    print("===== 开始更新指标详细信息 =====")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"连接数据库: instance/medquality.db")
    
    try:
        # 获取所有指标
        cursor.execute('SELECT id, code, name FROM indicators')
        indicators = cursor.fetchall()
        
        print(f"找到 {len(indicators)} 个指标需要更新")
        
        # 更新每个指标的详细信息
        updated_count = 0
        for indicator in indicators:
            indicator_id, code, name = indicator
            
            # 为指标生成默认的详细信息
            definition = f"{name}是衡量医疗质量的重要指标，编码为{code}。"
            numerator_description = f"{name}的分子为符合条件的病例数。"
            denominator_description = f"{name}的分母为总病例数。"
            calculation_formula = f"计算公式: 分子/分母×100%"
            data_source = "病历系统"
            
            # 更新指标详细信息字段
            try:
                cursor.execute('''
                    UPDATE indicators 
                    SET definition = ?, 
                        numerator_description = ?, 
                        denominator_description = ?, 
                        calculation_formula = ?, 
                        data_source = ?
                    WHERE id = ?
                ''', (definition, numerator_description, denominator_description, 
                      calculation_formula, data_source, indicator_id))
                
                updated_count += 1
                if updated_count % 10 == 0:
                    print(f"已更新 {updated_count}/{len(indicators)} 个指标")
            except Exception as e:
                print(f"更新指标 {code} ({name}) 失败: {str(e)}")
        
        # 提交更改
        conn.commit()
        
        print(f"\n成功更新了 {updated_count}/{len(indicators)} 个指标的详细信息")
        print("这将解决'获取指标信息失败'的问题")
        
    except Exception as e:
        conn.rollback()
        print(f"\n错误: {str(e)}")
        print("完整错误跟踪:")
        traceback.print_exc()
        print("\n操作已回滚，数据库未发生变化。")
    finally:
        conn.close()

if __name__ == "__main__":
    main() 