import sqlite3 as sql #for reading sql db
import pandas as pd
import sqlite3
import csv

df1 = pd.read_csv('./data/objects.csv')
df2 = pd.read_csv("./data/published_images.csv")
df3 = pd.read_csv("./data/locations.csv")
df1.columns = df1.columns.str.strip()

conn=sqlite3.connect('Art.db')
table1= df1.to_sql('objects', conn, if_exists='replace')
table2 = df2.to_sql('images', conn, if_exists='replace')
table3 = df3.to_sql('locations', conn, if_exists='replace')

cursor=conn.cursor()

cursor.execute("ALTER TABLE objects ADD COLUMN imageurl TEXT")
cursor.execute("ALTER TABLE objects ADD COLUMN site TEXT")
cursor.execute("UPDATE objects SET imageurl = (SELECT iiifthumburl FROM images WHERE objects.objectid = images.depictstmsobjectid), site = (SELECT site FROM locations WHERE objects.locationid = locations.locationid)")

conn.commit()
conn.close



