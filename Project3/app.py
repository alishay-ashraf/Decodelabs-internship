import sqlite3

# --- THE BRIDGE: Connection Setup ---
def get_connection():
    """Establishes a connection to the SQLite digital vault."""
    conn = sqlite3.connect('users .db')
    conn.row_factory = sqlite3.Row # Allows dictionary-like access to rows
    return conn

# --- THE ACTION: CRUD Operations ---

# 1. CREATE
def create_user(name, email):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Using ? placeholders acts as a shield for data integrity and security
        cursor.execute("INSERT INTO Users (Name, Email) VALUES (?, ?)", (name, email))
        conn.commit()
        print(f"Success: User '{name}' added to the database.")
    except sqlite3.IntegrityError:
        print(f"Error: Email '{email}' is already in use.")
    finally:
        conn.close()

# 2. READ
def read_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    conn.close()
    
    print("\n--- Current Users in Vault ---")
    for user in users:
        # ADD THIS DEBUG LINE:
        print("Available columns in this row:", user.keys()) 
        
        # Once you see the output, update the keys below to match!
        print(f"ID: {user['UserID']} | Name: {user['Name']} | Email: {user['Email']}")
    print("------------------------------\n")



# 3. UPDATE
def update_user_email(user_id, new_email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Users SET Email = ? WHERE UserID = ?", (new_email, user_id))
    conn.commit()
    
    if cursor.rowcount > 0:
        print(f"Success: UserID {user_id}'s email updated to {new_email}.")
    else:
        print(f"Error: UserID {user_id} not found.")
    conn.close()

# 4. DELETE
def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Users WHERE UserID = ?", (user_id,))
    conn.commit()
    
    if cursor.rowcount > 0:
        print(f"Success: UserID {user_id} deleted permanently.")
    else:
        print(f"Error: UserID {user_id} not found.")
    conn.close()

# --- EXECUTION ---
# --- EXECUTION ---
if __name__ == "__main__":
    print("Initializing Project 3 Backend...")
    
    # AUTOMATED FIX: Ensure the table exists before running operations
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Email TEXT UNIQUE NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    
    # Now run your test operations safely!
    # (If Alice and Bob already exist from a previous run, 
    # the code will gracefully print your custom error messages)
    create_user("Alice", "alice@email.com") 
    create_user("Bob", "bob@email.com")
    
    read_users()