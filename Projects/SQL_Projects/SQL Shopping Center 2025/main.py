import sqlite3 
import sys
from getpass import getpass
from salesperson import *
from customers import *

def main():
    global FILENAME
    
    # Get database filename from command line argument
    if len(sys.argv) < 2:
        print("Usage: python script.py <database_name>")
        print("Example: python script.py ecommerce.db")
        sys.exit(1)
    
    FILENAME = sys.argv[1]
    # Add .db extension if not provided
    if not FILENAME.endswith('.db'):
        FILENAME += '.db'
    set_FILENAMEsales(FILENAME)
    set_FILENAME(FILENAME)

    while True:
        r = menu()
        user = None
        match r:
            case 1:
                user = login()
            case 2:
                user = register()
            case 3:
                print("\nThank you for visiting!")
                exit()

        if user:
            if user['role'] == 'customer':
                customer_menu(user)
            elif user['role'] == 'sales':
                sales_menu(user)


def menu():
    print("""
Welcome! Please select an action:
    1. Login 
    2. Register
    3. Exit
    """)

    while True:
        try:
            response = int(input("> "))
            if response in {1, 2, 3}:
                return response
            else:
                print("Invalid choice. Please select 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def login():
    """user login

    Returns:
        user: dict with keys 'uid' and 'role' if successful, else None
    """
    print("\n--- LOGIN ---")
    uid = input("Enter User ID: ").strip()
    password = getpass("Enter Password: ")

    
    conn = sqlite3.connect(FILENAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT uid, role FROM users WHERE uid = ? AND pwd = ?", 
                   (uid, password))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        print(f"\nLogin successful! Welcome User {result[0]}")
        return {'uid': result[0], 'role': result[1]}
    else:
        print("\nLogin failed. Invalid User ID or Password.")
        return None
    
def register():
    """user registration, makes new user entry in database if none with the same email exists

    Returns:
        user: dict with keys 'uid' and 'role' if successful, else None
    """
    print("\n--- REGISTER ---")
    name = input("Enter your name: ").strip()
    email = input("Enter your email: ").strip()
    password = getpass("Enter Password: ")
    
    if not name or not email or not password:
        print("\nAll fields are required!")
        return None
    
    conn = sqlite3.connect(FILENAME)
    cursor = conn.cursor()
    
    # Check if email already exists
    cursor.execute("SELECT email FROM customers WHERE email = ?", (email,))
    if cursor.fetchone():
        print("\nEmail already registered!")
        conn.close()
        return None
    
    # Insert into users table
    cursor.execute("SELECT MAX(uid) FROM users")
    max_uid = cursor.fetchone()[0]
    uid = 1 if max_uid is None else max_uid + 1
    
    # Insert into users table
    cursor.execute("INSERT INTO users (uid, pwd, role) VALUES (?, ?, 'customer')", 
                    (uid, password))
    
    # Insert into customers table using uid from previous insert
    cursor.execute("INSERT INTO customers (cid, name, email) VALUES (?, ?, ?)", 
                    (uid, name, email))
    
    conn.commit()
    conn.close()

    print(f"\nRegistration successful! Your User ID is: {uid}")

    return {'uid': uid, 'role': 'customer'}


if __name__ == "__main__":
    main()