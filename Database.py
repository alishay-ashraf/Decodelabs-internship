import sqlite3
from datetime import datetime

# 1. Connect to database (creates user.db file if it doesn't exist)
conn = sqlite3.connect("user.db")
cursor = conn.cursor()

# 2. Enable foreign key support & create the User table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- SQLite auto-increments INTEGER IDs
    email TEXT NOT NULL UNIQUE,            -- Prevents duplicate entries
    age INTEGER CHECK(age >= 0),          -- Numeric range check constraint
    is_active BOOLEAN DEFAULT 1,          -- State flag (1 = True, 0 = False)
    created_at TEXT NOT NULL              -- Stored as text string in UTC ISO format
);
""")
conn.commit()

# 3. Securely Insert a User (Parameterized query to prevent SQL Injection)
def create_user(email, age):
    try:
        current_utc_time = datetime.utcnow().isoformat()
        cursor.execute("""
            INSERT INTO users (email, age, created_at) 
            VALUES (?, ?, ?)
        """, (email, age, current_utc_time))
        conn.commit()
        print("🎉 User successfully committed to non-volatile disk!")
    except sqlite3.IntegrityError as e:
        print(f"❌ Data Integrity Error: {e} (Likely a duplicate email or invalid age)")

# Test it out
create_user("intern@tech.com", 24)

# Always close the connection when done
conn.close()