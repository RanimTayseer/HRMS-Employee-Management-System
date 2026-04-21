import sqlite3

conn = sqlite3.connect('personnel.db')
cursor = conn.cursor()

# Check if admin exists
cursor.execute("SELECT * FROM users WHERE username = 'admin'")
admin = cursor.fetchone()

if admin:
    print(f"Admin already exists: {admin}")
else:
    # Add admin user
    cursor.execute("""
        INSERT INTO users (username, password_hash, role, is_active)
        VALUES ('admin', 'admin123', 'admin', 1)
    """)
    conn.commit()
    print("✅ Admin user added successfully!")
    print("   Username: admin")
    print("   Password: admin123")

# Verify
cursor.execute("SELECT user_id, username, role FROM users")
all_users = cursor.fetchall()
print("\n📊 All users:")
for user in all_users:
    print(f"   ID: {user[0]}, Username: {user[1]}, Role: {user[2]}")

conn.close()