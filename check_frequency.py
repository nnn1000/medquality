#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

conn = sqlite3.connect('instance/medquality.db')
cursor = conn.cursor()

cursor.execute('SELECT DISTINCT frequency FROM indicators')
results = cursor.fetchall()

print('frequency字段所有不同取值:')
for row in results:
    print(row[0])

conn.close() 