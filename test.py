import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

connection = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE"),
)

cursor = connection.cursor()
cursor.execute(
"""
CREATE TABLE IF NOT EXISTS users(
    id SERIAL,
    name VARCHAR(100),
    age INT
)
"""
)

cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)",
               ("Alice", 25))
connection.commit()
print('row inserted')

cursor.execute("SELECT id, name, age FROM users")

for row in cursor.fetchall():
    print(row)