#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

conn = sqlite3.connect('instance/medquality.db')
cursor = conn.cursor()

cursor.execute('SELECT code, name, target_value FROM indicators LIMIT 20')
rows = cursor.fetchall()

print('部分指标的目标值:')
for row in rows:
    print(row)

conn.close() 