import sqlite3
import pandas as pd
from datetime import datetime

def export_indicators():
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    # 获取表结构
    cursor.execute("PRAGMA table_info(indicators)")
    columns_info = cursor.fetchall()
    print("表结构：")
    for col in columns_info:
        print(f"列名: {col[1]}, 类型: {col[2]}")
    
    # 获取所有指标信息
    cursor.execute('''
        SELECT 
            code,
            name,
            definition,
            numerator_description,
            denominator_description,
            calculation_formula,
            data_source,
            target_value,
            unit,
            frequency,
            category_id,
            created_at
        FROM indicators
        ORDER BY code
    ''')
    
    # 获取列名
    columns = [description[0] for description in cursor.description]
    
    # 获取数据
    data = cursor.fetchall()
    
    # 创建DataFrame
    df = pd.DataFrame(data, columns=columns)
    
    # 格式化日期时间列（使用更灵活的解析方式）
    df['created_at'] = pd.to_datetime(df['created_at'], format='mixed').dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 生成文件名（包含时间戳）
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'indicators_export_{timestamp}.xlsx'
    
    # 创建Excel写入器
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    
    # 将数据写入Excel
    df.to_excel(writer, sheet_name='指标列表', index=False)
    
    # 获取workbook和worksheet对象
    workbook = writer.book
    worksheet = writer.sheets['指标列表']
    
    # 设置列宽
    worksheet.set_column('A:A', 10)  # 指标代码
    worksheet.set_column('B:B', 40)  # 指标名称
    worksheet.set_column('C:C', 50)  # 指标定义
    worksheet.set_column('D:D', 50)  # 分子描述
    worksheet.set_column('E:E', 50)  # 分母描述
    worksheet.set_column('F:F', 50)  # 计算公式
    worksheet.set_column('G:G', 30)  # 数据来源
    worksheet.set_column('H:H', 10)  # 目标值
    worksheet.set_column('I:I', 10)  # 单位
    worksheet.set_column('J:J', 15)  # 统计频率
    worksheet.set_column('K:K', 10)  # 类别ID
    worksheet.set_column('L:L', 20)  # 创建时间
    
    # 添加表头格式
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#D7E4BC',
        'border': 1
    })
    
    # 设置中文列名
    column_names = {
        'code': '指标代码',
        'name': '指标名称',
        'definition': '指标定义',
        'numerator_description': '分子描述',
        'denominator_description': '分母描述',
        'calculation_formula': '计算公式',
        'data_source': '数据来源',
        'target_value': '目标值',
        'unit': '单位',
        'frequency': '统计频率',
        'category_id': '类别ID',
        'created_at': '创建时间'
    }
    
    # 应用表头格式和中文列名
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, column_names.get(value, value), header_format)
    
    # 保存文件
    writer.close()
    
    print(f"\n指标列表已导出到文件：{filename}")
    
    conn.close()

if __name__ == "__main__":
    export_indicators() 