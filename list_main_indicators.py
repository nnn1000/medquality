#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

conn = sqlite3.connect('instance/medquality.db')
cursor = conn.cursor()

cursor.execute('SELECT code, name FROM indicators WHERE instr(code, ".")=0 ORDER BY code')
rows = cursor.fetchall()

print('主指标列表:')
for code, name in rows:
    print(f'{code}: {name}')

conn.close() 