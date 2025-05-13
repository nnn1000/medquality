import sqlite3
from collections import defaultdict

def analyze_indicators():
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    # 获取所有指标信息
    cursor.execute('''
        SELECT code, name, category_id
        FROM indicators
        ORDER BY code
    ''')
    
    indicators = cursor.fetchall()
    
    # 按类别分组
    category_groups = defaultdict(list)
    for code, name, category_id in indicators:
        category_groups[category_id].append((code, name))
    
    print("指标逻辑关系分析报告")
    print("=" * 80)
    
    # 1. 检查指标代码命名规则
    print("\n1. 指标代码命名规则分析：")
    print("-" * 40)
    code_patterns = defaultdict(list)
    for code, name, _ in indicators:
        prefix = ''.join(c for c in code if not c.isdigit())
        code_patterns[prefix].append((code, name))
    
    for prefix, codes in code_patterns.items():
        print(f"\n{prefix}类指标：")
        for code, name in codes:
            print(f"  - {code}: {name}")
    
    # 2. 检查指标分类
    print("\n2. 指标分类分析：")
    print("-" * 40)
    for category_id, indicators in category_groups.items():
        print(f"\n类别ID {category_id} 的指标：")
        for code, name in indicators:
            print(f"  - {code}: {name}")
    
    # 3. 检查相关指标
    print("\n3. 相关指标分析：")
    print("-" * 40)
    
    # 检查手术相关指标
    surgery_indicators = [ind for ind in indicators if "手术" in ind[1]]
    if surgery_indicators:
        print("\n手术相关指标：")
        for code, name, _ in surgery_indicators:
            print(f"  - {code}: {name}")
    
    # 检查感染相关指标
    infection_indicators = [ind for ind in indicators if "感染" in ind[1]]
    if infection_indicators:
        print("\n感染相关指标：")
        for code, name, _ in infection_indicators:
            print(f"  - {code}: {name}")
    
    # 检查死亡率相关指标
    mortality_indicators = [ind for ind in indicators if "死亡" in ind[1]]
    if mortality_indicators:
        print("\n死亡率相关指标：")
        for code, name, _ in mortality_indicators:
            print(f"  - {code}: {name}")
    
    conn.close()

if __name__ == "__main__":
    analyze_indicators() 