import csv
import sqlite3


con = sqlite3.connect('db.sqlite3')
cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS titles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    year INT,
    category TEXT
)""")

with open('titles.csv', 'r', encoding="utf-8") as f:
    dr = csv.DictReader(f, delimiter=";")
    to_db = [(i['name'], i['year'], i['category']) for i in dr]
string = "INSERT INTO titles (name, year, category) VALUES (?, ?, ?);"

cur.executemany(string, to_db)
con.commit()
con.close()
