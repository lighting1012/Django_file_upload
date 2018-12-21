# create database and a simple table
#   id  |   context
#   int     text
import sqlite3
import os
import re
from collections import defaultdict

sql_dict = defaultdict(str)
for filename in os.listdir():
    if filename.endswith('.txt'):
        print(filename)
        id = int(re.findall("\d+", filename)[-1])
        f = open(filename)
        context = f.read()
        f.close()
        sql_dict[id] = (filename, context)

conn = sqlite3.connect("test.db")
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS recommondation")
c.execute("CREATE TABLE recommondation (id int primary key,title text, context text)")
for i in range(1, max(sql_dict.keys())+1):
    c.execute("INSERT INTO recommondation VALUES(?,?,?)", [i, sql_dict[i][0], sql_dict[i][1]])

conn.commit()
conn.close()
