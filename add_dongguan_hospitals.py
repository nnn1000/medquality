#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# 添加项目根目录到系统路径，确保能够导入app包
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from flask import current_app
from app import create_app, db
from app.models.hospital import Hospital

def add_dongguan_hospitals():
    """添加东莞的医院数据到数据库"""
    
    # 创建应用上下文
    app = create_app()
    with app.app_context():
        # 东莞医院数据
        hospitals_data = [
            {'name': '东莞市人民医院', 'code': 'DGRMYY', 'type': '综合医院', 'level': '三级甲等'},
            {'name': '东莞市中医院', 'code': 'DGZYY', 'type': '中医（综合）医院', 'level': '三级甲等'},
            {'name': '东莞市妇幼保健院', 'code': 'DGFYBJY', 'type': '妇幼保健院', 'level': '三级甲等'},
            {'name': '东莞市松山湖中心医院', 'code': 'DGSSHLZXYY', 'type': '综合医院', 'level': '三级甲等'},
            {'name': '东莞市滨海湾中心医院', 'code': 'DGBHWZXYY', 'type': '综合医院', 'level': '三级甲等'},
            {'name': '东莞市第八人民医院', 'code': 'DGDBRMY', 'type': '儿童医院', 'level': '三级甲等'},
            {'name': '东莞市厚街医院', 'code': 'DGHJYY', 'type': '综合医院', 'level': '三级甲等'},
            {'name': '东莞东华医院', 'code': 'DGDHYY', 'type': '综合医院', 'level': '三级甲等'},
            {'name': '东莞康华医院', 'code': 'DGKHYY', 'type': '综合医院', 'level': '三级甲等'},
            {'name': '东莞市东部中心医院', 'code': 'DGDBZXYY', 'type': '综合医院', 'level': '三级未定等'},
            {'name': '东莞市东南部中心医院', 'code': 'DGDNBZXYY', 'type': '综合医院', 'level': '三级未定等'},
            {'name': '东莞市水乡中心医院', 'code': 'DGSXZXYY', 'type': '综合医院', 'level': '三级未定等'},
            {'name': '东莞市第六人民医院', 'code': 'DGDLRMY', 'type': '其他专科疾病防治院', 'level': '三级未定等'},
            {'name': '东莞市第七人民医院', 'code': 'DGDQRMY', 'type': '精神病医院', 'level': '三级未定等'},
            {'name': '东莞市第九人民医院', 'code': 'DGDJRMY', 'type': '综合医院', 'level': '三级未定等'},
            {'name': '东莞市中西医结合医院', 'code': 'DGZXYJHYY', 'type': '中西医结合医院', 'level': '三级未定等'},
            {'name': '东莞市大朗医院', 'code': 'DGDLYY', 'type': '综合医院', 'level': '三级未定等'},
            {'name': '东莞市长安医院', 'code': 'DGCAYY', 'type': '综合医院', 'level': '三级未定等'},
            {'name': '东莞市虎门医院', 'code': 'DGHMYY', 'type': '综合医院', 'level': '三级未定等'},
            {'name': '东莞松山湖东华医院', 'code': 'DGSSHLDHYY', 'type': '综合医院', 'level': '三级未定等'},
            {'name': '东莞常安医院', 'code': 'DGCAYY2', 'type': '综合医院', 'level': '三级未定等'},
            {'name': '东莞广济医院', 'code': 'DGGJYY', 'type': '综合医院', 'level': '三级未定等'},
            {'name': '东莞台心医院', 'code': 'DGTXYY', 'type': '综合医院', 'level': '三级未定等'},
            {'name': '东莞爱尔眼科医院', 'code': 'DGAEYKBYM', 'type': '眼科医院', 'level': '三级未定等'},
            {'name': '东莞光明眼科医院', 'code': 'DGGMYKYY', 'type': '眼科医院', 'level': '三级未定等'},
            {'name': '东莞华厦眼科医院', 'code': 'DGHXYKYY', 'type': '眼科医院', 'level': '三级未定等'},
            {'name': '东莞虎门爱尔眼科医院', 'code': 'DGHMAEYKYY', 'type': '眼科医院', 'level': '三级未定等'},
            {'name': '东莞市高埗医院', 'code': 'DGGBYY', 'type': '综合医院', 'level': '二级甲等'},
            {'name': '东莞市茶山医院', 'code': 'DGCSYY', 'type': '综合医院', 'level': '二级甲等'},
            {'name': '东莞市寮步医院', 'code': 'DGLBYY', 'type': '综合医院', 'level': '二级甲等'},
            {'name': '东莞市凤岗医院', 'code': 'DGFGYY', 'type': '综合医院', 'level': '二级甲等'},
            {'name': '东莞市石排医院', 'code': 'DGSPYY', 'type': '综合医院', 'level': '二级甲等'},
            {'name': '东莞市清溪医院', 'code': 'DGQXYY', 'type': '中西医结合医院', 'level': '二级甲等'},
            {'name': '东莞市沙田医院', 'code': 'DGSTYY', 'type': '综合医院', 'level': '二级甲等'},
            {'name': '东莞市石碣医院', 'code': 'DGSGYY', 'type': '综合医院', 'level': '二级甲等'},
            {'name': '东莞市横沥医院', 'code': 'DGHLYY', 'type': '综合医院', 'level': '二级甲等'},
            {'name': '东莞市东坑医院', 'code': 'DGDKYY', 'type': '综合医院', 'level': '二级甲等'},
            {'name': '东莞市谢岗医院', 'code': 'DGXGYY', 'type': '综合医院', 'level': '二级甲等'},
            {'name': '东莞市虎门中医院', 'code': 'DGHMZYY', 'type': '中医（综合）医院', 'level': '二级甲等'},
            {'name': '东莞市黄江医院', 'code': 'DGHJYY2', 'type': '综合医院', 'level': '二级甲等'},
            {'name': '东莞市桥头医院', 'code': 'DGQTYY', 'type': '综合医院', 'level': '二级未定等'},
            {'name': '东莞市莞城医院', 'code': 'DGGCYY', 'type': '综合医院', 'level': '二级未定等'},
            {'name': '东莞市企石医院', 'code': 'DGQSYY', 'type': '中西医结合医院', 'level': '二级未定等'},
            {'name': '东莞市中堂医院', 'code': 'DGZTYY', 'type': '中西医结合医院', 'level': '二级未定等'},
            {'name': '东莞市东城医院', 'code': 'DGDCYY', 'type': '综合医院', 'level': '二级未定等'},
            {'name': '东莞市南城医院', 'code': 'DGNCYY', 'type': '综合医院', 'level': '二级甲等'},
            {'name': '东莞市樟木头医院', 'code': 'DGZMTYY', 'type': '综合医院', 'level': '二级未定等'},
            {'name': '东莞市万江医院', 'code': 'DGWJYY', 'type': '综合医院', 'level': '二级未定等'},
            {'name': '东莞市道滘医院', 'code': 'DGDJYY', 'type': '综合医院', 'level': '二级未定等'},
            {'name': '东莞市望牛墩医院', 'code': 'DGWNDYY', 'type': '综合医院', 'level': '二级未定等'},
            {'name': '东莞市洪梅医院', 'code': 'DGHMYY2', 'type': '综合医院', 'level': '二级未定等'},
            {'name': '东莞三局医院', 'code': 'DGSJYY', 'type': '综合医院', 'level': '二级未定等'},
            {'name': '东莞仁康医院', 'code': 'DGRKYY', 'type': '综合医院', 'level': '二级甲等'},
            {'name': '东莞康怡医院', 'code': 'DGKYYY', 'type': '综合医院', 'level': '二级未定等'},
            {'name': '东莞长安新安医院', 'code': 'DGCAXAYY', 'type': '综合医院', 'level': '二级未定等'},
            {'name': '东莞市虎门镇南栅医院', 'code': 'DGHMZNZYY', 'type': '综合医院', 'level': '二级未定等'},
            {'name': '东莞曙光广华医院', 'code': 'DGSGGHYY', 'type': '综合医院', 'level': '二级未定等'},
            {'name': '东莞光华医院', 'code': 'DGGHYY', 'type': '综合医院', 'level': '二级未定等'},
            {'name': '东莞市康复医院', 'code': 'DGKFYY', 'type': '康复医院', 'level': '二级未定等'},
            {'name': '东莞同泰德康复医院', 'code': 'DGTTDKFYY', 'type': '康复医院', 'level': '二级未定等'}
        ]
            
        # 添加医院数据
        added_count = 0
        for hospital_data in hospitals_data:
            # 检查医院是否已存在
            existing = Hospital.query.filter_by(name=hospital_data['name']).first()
            if not existing:
                # 添加地址和联系人信息
                hospital_data['address'] = '广东省东莞市'
                hospital_data['contact_person'] = '管理员'
                hospital_data['contact_phone'] = '0769-xxxxxxxx'
                
                hospital = Hospital(**hospital_data)
                db.session.add(hospital)
                added_count += 1
            else:
                print(f"医院 '{hospital_data['name']}' 已存在，跳过添加。")
        
        # 提交到数据库
        if added_count > 0:
            db.session.commit()
            print(f"成功添加 {added_count} 家东莞医院")
        else:
            print("没有新医院需要添加")
        
        # 显示当前所有医院
        all_hospitals = Hospital.query.all()
        print(f"\n当前医院总数: {len(all_hospitals)}")
        
if __name__ == "__main__":
    add_dongguan_hospitals() 