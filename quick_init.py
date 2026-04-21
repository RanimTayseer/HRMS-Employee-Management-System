# quick_init.py - Run this file directly

import sqlite3
import os

# Absolute path to database
db_path = r"C:\Users\LENOVO\Desktop\My Python\.vscode\Python\PersonnelManagementProgram\personnel.db"

# Ensure the folder exists
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create simple test table
cursor.execute('''
CREATE TABLE IF NOT EXISTS test_table (
    id INTEGER PRIMARY KEY,
    name TEXT
)
''')

# Insert data (with error handling)
try:
    cursor.execute("INSERT INTO test_table (id, name) VALUES (1, 'Test')")
    conn.commit()
    print("✅ Data inserted successfully!")
except sqlite3.IntegrityError:
    print("⚠️ Record already exists, skipping insert")
    conn.rollback()

# Verify data
cursor.execute("SELECT * FROM test_table")
results = cursor.fetchall()
print(f"📊 Records in test_table: {results}")

conn.close()

print("✅ Database created and tested successfully!")
print(f"📍 Location: {db_path}")