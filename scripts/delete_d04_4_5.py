#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# 添加项目根目录到系统路径，确保能够导入app包
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import current_app
from app import create_app, db
from app.models.indicator import Indicator

def delete_d04_4_5():
    """删除 D04.4 和 D04.5 指标"""
    
    # 创建应用上下文
    app = create_app()
    with app.app_context():
        # 删除 D04.4
        indicator_4 = Indicator.query.filter_by(code='D04.4').first()
        if indicator_4:
            db.session.delete(indicator_4)
            print("已删除 D04.4 指标")
        else:
            print("D04.4 指标不存在")
            
        # 删除 D04.5
        indicator_5 = Indicator.query.filter_by(code='D04.5').first()
        if indicator_5:
            db.session.delete(indicator_5)
            print("已删除 D04.5 指标")
        else:
            print("D04.5 指标不存在")
            
        # 提交更改
        db.session.commit()
        print("完成指标删除操作")

if __name__ == "__main__":
    delete_d04_4_5() 