#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from app import create_app, db
from app.models.data import Result

def update_results_precision():
    """更新数据库中的所有结果值为两位小数"""
    print("开始更新结果精度为两位小数...")
    
    # 创建应用上下文
    app = create_app()
    with app.app_context():
        # 获取所有结果
        results = Result.query.all()
        count = 0
        
        # 更新每个结果
        for result in results:
            if result.value is not None:
                original_value = result.value
                result.value = round(result.value, 2)
                count += 1
                print(f"更新 ID={result.id}: {original_value} -> {result.value}")
        
        # 提交更改
        db.session.commit()
        
        print(f"更新完成！共更新了 {count} 条结果记录。")

if __name__ == "__main__":
    update_results_precision() 