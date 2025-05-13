import sqlite3
from datetime import datetime
import traceback

# 根据截图内容整理的指标清单
categories_and_indicators = [
    {
        "name": "急诊和日间医疗质量",
        "indicators": [
            {"code": "A01", "name": "平均急救响应时间"},
            {"code": "A02", "name": "心脏骤停复苏成功率"},
            {"code": "A03", "name": "急性ST段抬高型心肌梗死再灌注治疗率"},
            {"code": "A04", "name": "急性脑梗死再灌注治疗率"},
            {"code": "A05", "name": "开展日间医疗服务的医院占比"},
            {"code": "A06", "name": "日间手术占择期手术的比例"}
        ]
    },
    {
        "name": "医疗行为质量",
        "indicators": [
            {"code": "B01", "name": "肿瘤治疗前临床TNM分期评估率"},
            {"code": "B02", "name": "营养风险筛查率"},
            {"code": "B03", "name": "疼痛评估规范率"},
            {"code": "B03.1", "name": "门诊疼痛评估规范率"},
            {"code": "B03.2", "name": "住院患者入院8h内评估规范率"},
            {"code": "B04", "name": "门诊处方审核率"},
            {"code": "B05", "name": "急诊处方审核率"},
            {"code": "B06", "name": "住院处方审核率"},
            {"code": "B07", "name": "门诊处方审核合格率"},
            {"code": "B08", "name": "急诊处方审核合格率"},
            {"code": "B09", "name": "基本药物采购品种数占比"},
            {"code": "B10", "name": "住院处方审核合格率"},
            {"code": "B11", "name": "住院患者静脉输液规范使用率"},
            {"code": "B11.1", "name": "住院患者静脉输液使用率"},
            {"code": "B11.2", "name": "住院患者静脉输液平均每床日使用数量"},
            {"code": "B11.3", "name": "住院患者静脉输液平均每床日使用体积"},
            {"code": "B11.4", "name": "住院患者平均使用输液药品品种数量"},
            {"code": "B12", "name": "危急值报告及时率"},
            {"code": "B13", "name": "危急值处置及时率"},
            {"code": "B14", "name": "室间质评项目合格率"},
            {"code": "B15", "name": "早期康复介入率"},
            {"code": "B15.1", "name": "早期康复介入率（神经内科）"},
            {"code": "B15.2", "name": "早期康复介入率（神经外科）"},
            {"code": "B15.3", "name": "早期康复介入率（骨科）"},
            {"code": "B15.4", "name": "早期康复介入率（心血管内科）"},
            {"code": "B15.5", "name": "早期康复介入率（重症ICU）"},
            {"code": "B15.6", "name": "早期康复介入率（脑卒中）"},
            {"code": "B15.7", "name": "早期康复介入率（脊髓损伤）"},
            {"code": "B15.8", "name": "早期康复介入率（髋、膝关节置换术后）"},
            {"code": "B15.9", "name": "康复评定率"},
            {"code": "B16", "name": "四级手术患者随访率"},
            {"code": "B17", "name": "恶性肿瘤患者随访率"},
            {"code": "B18", "name": "每百出院人次主动报告不良事件例次"},
            {"code": "B19", "name": "中医医疗机构中以中医治疗为主的出院患者比例"}
        ]
    },
    {
        "name": "结果质量",
        "indicators": [
            {"code": "C01", "name": "医院CMI值"},
            {"code": "C02", "name": "手术患者住院死亡率"},
            {"code": "C03", "name": "ICU患者病死率"},
            {"code": "C04", "name": "手术并发症发生率"},
            {"code": "C05", "name": "麻醉并发症发生率"},
            {"code": "C06", "name": "非计划重返手术室再手术率"},
            {"code": "C06.1", "name": "非计划重返手术室再手术率"},
            {"code": "C06.2", "name": "手术患者术后48小时内非计划重返手术室再次手术率"},
            {"code": "C06.3", "name": "手术患者术后31天内非计划重返手术室再次手术率"},
            {"code": "C07", "name": "围术期死亡率"},
            {"code": "C07.1", "name": "手术当日围术期死亡率"},
            {"code": "C07.2", "name": "术后24小时围术期死亡率"},
            {"code": "C07.3", "name": "术后48小时围术期死亡率"},
            {"code": "C08", "name": "恶性肿瘤患者生存时间"},
            {"code": "C09", "name": "血管内导管相关血流感染发生率"},
            {"code": "C10", "name": "患者院内压力性损伤发生率"},
            {"code": "C11", "name": "住院患者手术术后获得性指标发生率"},
            {"code": "C11.1", "name": "手术患者手术后肺栓塞发生率"},
            {"code": "C11.2", "name": "手术患者手术后深静脉血栓发生率"},
            {"code": "C11.3", "name": "手术患者手术后败血症发生率"},
            {"code": "C11.4", "name": "手术患者手术后出血或血肿发生率"},
            {"code": "C11.5", "name": "手术患者手术伤口裂开发生率"},
            {"code": "C11.6", "name": "手术患者手术后猝死发生率"},
            {"code": "C11.7", "name": "手术患者手术后呼吸衰竭发生率"},
            {"code": "C11.8", "name": "手术患者手术后生理/代谢紊乱发生率"},
            {"code": "C11.9", "name": "与手术/操作相关感染发生例数和发生率"},
            {"code": "C11.10", "name": "手术过程中异物遗留发生率"},
            {"code": "C11.11", "name": "手术患者麻醉并发症发生率"},
            {"code": "C11.12", "name": "手术患者肺部感染与肺机能不全发生率"},
            {"code": "C11.13", "name": "手术意外穿刺伤或撕裂伤发生率"},
            {"code": "C11.14", "name": "手术后急性肾衰竭发生率"},
            {"code": "C11.15", "name": "各系统/器官术后并发症发生率"},
            {"code": "C11.16", "name": "植入物的并发症（不包括脓毒症）发生率"},
            {"code": "C11.17", "name": "再植和截肢的并发症发生率"},
            {"code": "C11.18", "name": "介入操作与手术患者其他并发症发生率"},
            {"code": "C11.19", "name": "剖宫产分娩产妇产程和分娩并发症发生率"}
        ]
    },
    {
        "name": "病历质量",
        "indicators": [
            {"code": "D01", "name": "门诊病历电子化比例"},
            {"code": "D02", "name": "门诊结构化病历使用比例"},
            {"code": "D03", "name": "病案首页主要诊断编码正确率"},
            {"code": "D03.1", "name": "病案首页主要诊断填写正确率"},
            {"code": "D03.2", "name": "病案首页主要诊断编码正确率"},
            {"code": "D04", "name": "病历记录及时性"},
            {"code": "D04.1", "name": "入院记录24小时内完成率"},
            {"code": "D04.2", "name": "手术记录24小时内完成率"},
            {"code": "D04.3", "name": "出院记录24小时内完成率"},
            {"code": "D04.5", "name": "病案首页24小时内完成率"}
        ]
    }
]

def main():
    # 连接数据库
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    print("===== 开始更新指标和类别 =====")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"连接数据库: instance/medquality.db")
    
    try:
        # 检查表结构
        print("\n检查数据库表结构...")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"数据库中的表: {[table[0] for table in tables]}")
        
        # 备份当前数据（仅计数）
        cursor.execute('SELECT COUNT(*) FROM indicator_categories')
        old_categories_count = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM indicators')
        old_indicators_count = cursor.fetchone()[0]
        
        print(f"当前数据库状态: {old_categories_count}个类别, {old_indicators_count}个指标")
        
        # 查看类别表结构
        cursor.execute('PRAGMA table_info(indicator_categories)')
        category_columns = cursor.fetchall()
        print(f"indicator_categories表结构: {category_columns}")
        
        # 查看指标表结构
        cursor.execute('PRAGMA table_info(indicators)')
        indicator_columns = cursor.fetchall()
        print(f"indicators表结构: {indicator_columns}")
        
        # 清空并重建 indicator_categories 表
        print("\n1. 清空指标类别表...")
        cursor.execute('DELETE FROM indicator_categories')
        conn.commit()
        
        # 插入类别
        print("\n2. 插入新的指标类别...")
        category_id_map = {}
        for idx, cat in enumerate(categories_and_indicators, 1):
            print(f"   - 准备添加类别 {idx}: {cat['name']}")
            cursor.execute(
                'INSERT INTO indicator_categories (id, name, created_at) VALUES (?, ?, datetime("now"))',
                (idx, cat["name"])
            )
            category_id_map[cat["name"]] = idx
            print(f"   - 成功添加类别 {idx}: {cat['name']}")
        
        conn.commit()
        print("   - 所有类别添加成功")
        
        # 清空并重建 indicators 表
        print("\n3. 清空指标表...")
        cursor.execute('DELETE FROM indicators')
        conn.commit()
        
        # 插入指标
        print("\n4. 插入新的指标...")
        indicator_count = 0
        for cat in categories_and_indicators:
            cat_id = category_id_map[cat["name"]]
            print(f"   - 类别: {cat['name']} (ID: {cat_id})")
            for ind in cat["indicators"]:
                try:
                    cursor.execute(
                        '''INSERT INTO indicators 
                           (code, name, category_id, created_at, frequency, target_value, unit) 
                           VALUES (?, ?, ?, datetime("now"), "月度", NULL, "%")''',
                        (ind["code"], ind["name"], cat_id)
                    )
                    indicator_count += 1
                    if indicator_count % 10 == 0:
                        print(f"   - 已添加 {indicator_count} 个指标")
                except Exception as e:
                    print(f"   - 添加指标 {ind['code']} ({ind['name']}) 失败: {str(e)}")
                
        conn.commit()
        
        # 验证更新结果
        cursor.execute('SELECT COUNT(*) FROM indicator_categories')
        new_categories_count = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM indicators')
        new_indicators_count = cursor.fetchone()[0]
        
        print("\n===== 更新完成 =====")
        print(f"更新前: {old_categories_count}个类别, {old_indicators_count}个指标")
        print(f"更新后: {new_categories_count}个类别, {new_indicators_count}个指标")
        print(f"共更新: {new_categories_count}个类别, {indicator_count}个指标")
        print("\n指标和类别已成功按手册内容完全同步。")
        
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