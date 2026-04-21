import sqlite3
import os

# Set current project folder path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Set full path to schema.sql file
schema_path = os.path.join(BASE_DIR, "database", "schema.sql")

print("Path used:", schema_path)

conn = sqlite3.connect("personnel.db")

with open(schema_path, "r", encoding="utf-8") as f:
    conn.executescript(f.read())

conn.commit()
conn.close()

print("✅ Database created successfully!")