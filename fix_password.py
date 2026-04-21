import sqlite3

conn = sqlite3.connect('personnel.db')
cursor = conn.cursor()

# Update admin password to plain text 'admin123'
cursor.execute("UPDATE users SET password_hash = 'admin123' WHERE username = 'admin'")

# Also update any other users
cursor.execute("UPDATE users SET password_hash = password_hash WHERE 1=1")

conn.commit()

# Verify
cursor.execute("SELECT user_id, username, password_hash, role FROM users")
users = cursor.fetchall()

print("=" * 50)
print("Users in database:")
print("=" * 50)
for user in users:
    print(f"ID: {user[0]}, Username: {user[1]}, Password: {user[2]}, Role: {user[3]}")

conn.close()
print("\n✅ Password updated successfully!")
print("Login with: admin / admin123")