import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    name TEXT PRIMARY KEY,
    marks INTEGER
)
""")

conn.commit()
conn.close()

print("Database created successfully!")