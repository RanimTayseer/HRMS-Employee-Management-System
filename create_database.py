import sqlite3
import os

# Database path
db_path = "personnel.db"
schema_path = "database/schema.sql"

print("=" * 50)
print("Creating Database...")
print("=" * 50)

# Check if schema file exists
if not os.path.exists(schema_path):
    print(f"❌ Error: {schema_path} not found!")
    exit(1)

# Delete old database if exists
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"✅ Removed old database: {db_path}")

# Create new database
conn = sqlite3.connect(db_path)
print(f"✅ Created new database: {db_path}")

# Read and execute schema
with open(schema_path, "r", encoding="utf-8") as f:
    sql_script = f.read()
    print(f"✅ Read schema file ({len(sql_script)} characters)")

try:
    conn.executescript(sql_script)
    conn.commit()
    print("✅ Executed schema successfully!")
except Exception as e:
    print(f"❌ Error executing schema: {e}")
    conn.close()
    exit(1)

# Verify tables
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print("\n📊 Created tables:")
for table in tables:
    print(f"   - {table[0]}")

# Verify admin user
cursor.execute("SELECT * FROM users WHERE username = 'admin'")
admin = cursor.fetchone()

print("\n👤 Admin user:")
if admin:
    print(f"   Username: {admin[1]}")
    print(f"   Role: {admin[3]}")
    print(f"   Active: {admin[4]}")
else:
    print("   ❌ Admin user not found!")

# Verify departments
cursor.execute("SELECT * FROM departments")
depts = cursor.fetchall()

print("\n🏢 Departments:")
for dept in depts:
    print(f"   - {dept[1]}: {dept[2]}")

conn.close()

print("\n" + "=" * 50)
print("✅ Database setup complete!")
print("=" * 50)
print("Login with:")
print("   Username: admin")
print("   Password: admin123")