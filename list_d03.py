#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

conn = sqlite3.connect('instance/medquality.db')
cursor = conn.cursor()

cursor.execute("SELECT code, name FROM indicators WHERE code LIKE 'D03%' ORDER BY code")
rows = cursor.fetchall()

print('D03及其子指标:')
for code, name in rows:
    print(f'{code}: {name}')

conn.close() 