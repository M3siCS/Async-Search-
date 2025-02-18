import sqlite3

# Connect to the database
conn = sqlite3.connect("search.db")
cursor = conn.cursor()

# Check if the 'items' table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='items';")
table_exists = cursor.fetchone()

if table_exists:
    # Fetch all rows from the 'items' table
    cursor.execute("SELECT * FROM items;")
    rows = cursor.fetchall()

    # Print results
    if rows:
        print("Database contains:")
        for row in rows:
            print(row)
    else:
        print("No data found in the items table.")
else:
    print("The 'items' table does not exist. Try running `populate_db.py` first.")

# Close connection
conn.close()

