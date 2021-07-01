import requests
import mysql.connector
import json



mydb = mysql.connector.connect(
  host="spelldb.clmnjdaevaow.ap-southeast-2.rds.amazonaws.com",
  user="admin",
  password="Ajensen3!",
  database="spelldb"
)



db = mydb.cursor()

print("this is a test for dev version")

db.execute("SHOW KEYS FROM spells WHERE key_name = 'id'")
output = db.fetchall()
for x in output:
  print(x)

