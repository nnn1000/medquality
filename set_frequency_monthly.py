#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

conn = sqlite3.connect('instance/medquality.db')
cursor = conn.cursor()

try:
    cursor.execute('BEGIN TRANSACTION')
    cursor.execute("UPDATE indicators SET frequency = '月度'")
    conn.commit()
    print('所有frequency字段已改为月度')
except Exception as e:
    conn.rollback()
    print(f'错误: {str(e)}')
finally:
    conn.close() 