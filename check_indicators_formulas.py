import sqlite3
from collections import defaultdict

def analyze_formulas():
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    # 获取所有指标信息，包括计算公式
    cursor.execute('''
        SELECT code, name, calculation_formula, numerator_description, denominator_description
        FROM indicators
        ORDER BY code
    ''')
    
    indicators = cursor.fetchall()
    
    print("指标计算公式分析报告")
    print("=" * 80)
    
    # 1. 按指标类别分组分析
    print("\n1. 按指标类别分组分析：")
    print("-" * 40)
    
    code_patterns = defaultdict(list)
    for code, name, formula, numerator, denominator in indicators:
        prefix = ''.join(c for c in code if not c.isdigit())
        code_patterns[prefix].append((code, name, formula, numerator, denominator))
    
    for prefix, codes in code_patterns.items():
        print(f"\n{prefix}类指标：")
        for code, name, formula, numerator, denominator in codes:
            print(f"\n  {code}: {name}")
            print(f"  计算公式: {formula}")
            print(f"  分子: {numerator}")
            print(f"  分母: {denominator}")
    
    # 2. 检查公式格式一致性
    print("\n2. 公式格式一致性分析：")
    print("-" * 40)
    
    formula_patterns = defaultdict(list)
    for code, name, formula, _, _ in indicators:
        if formula:
            # 提取公式中的运算符
            operators = ''.join(c for c in formula if c in '+-*/()÷×')
            formula_patterns[operators].append((code, name, formula))
    
    print("\n公式模式分析：")
    for pattern, formulas in formula_patterns.items():
        print(f"\n使用运算符 {pattern} 的指标：")
        for code, name, formula in formulas:
            print(f"  - {code}: {name}")
            print(f"    公式: {formula}")
    
    # 3. 检查分子分母描述与公式的一致性
    print("\n3. 分子分母描述与公式一致性分析：")
    print("-" * 40)
    
    for code, name, formula, numerator, denominator in indicators:
        if formula and numerator and denominator:
            print(f"\n{code}: {name}")
            print(f"公式: {formula}")
            print(f"分子: {numerator}")
            print(f"分母: {denominator}")
            
            # 检查公式中是否包含分子分母描述
            if numerator in formula and denominator in formula:
                print("✓ 公式包含分子分母描述")
            else:
                print("! 公式与分子分母描述不完全匹配")
    
    conn.close()

if __name__ == "__main__":
    analyze_formulas() 