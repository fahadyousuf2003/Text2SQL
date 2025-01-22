import sqlite3

# Connect to the database file
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# Get table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

# Query data from a table
table_name = input("\nEnter your table name ")  # Replace with your table name
cursor.execute(f"SELECT * FROM {table_name} LIMIT 10;")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close connection
conn.close()
