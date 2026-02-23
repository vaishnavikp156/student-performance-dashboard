import sqlite3
import csv

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

with open("marks.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        name = row["Name"]
        marks = int(row["Marks"])

        cursor.execute(
            "INSERT OR REPLACE INTO students(name, marks) VALUES(?, ?)", (name, marks))

conn.commit()
conn.close()

print("All students imported successfully!")
