#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

conn = sqlite3.connect('instance/medquality.db')
cursor = conn.cursor()

cursor.execute('PRAGMA table_info(indicators)')
columns = cursor.fetchall()

print('indicators表字段:')
for col in columns:
    print(f'{col[1]}')

conn.close() 