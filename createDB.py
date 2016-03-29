#!/usr/bin/python3
import sqlite3
from contextlib import closing

con = None
DROP1 = "DROP TABLE IF EXISTS \"apcd_last_onbattery\""
DROP2 = "DROP TABLE IF EXISTS \"apcd_offbattery\""
DROP3 = "DROP TABLE IF EXISTS \"apcd_onbattery\""
table1 = "CREATE TABLE \"apcd_last_onbattery\" (\"last_onbattery\" INTEGER)"
table2 = "CREATE TABLE \"apcd_offbattery\" (\"ID\" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE , \"offbattery\" DATETIME)"
table3 = "CREATE TABLE \"apcd_onbattery\" (\"ID\" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE , \"onbattery\" DATETIME)"
initdata = "INSERT INTO \"apcd_last_onbattery\" (\"last_onbattery\") VALUES (\"1\")"

con = sqlite3.connect("apcupsd.sqlite")
with closing(con.cursor()) as cur:
    cur.execute(DROP1)
    cur.execute(DROP2)
    cur.execute(DROP3)
    cur.execute(table1)
    cur.execute(table2)
    cur.execute(table3)
    cur.execute(initdata)
con.commit()  
