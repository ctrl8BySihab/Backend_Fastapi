import sqlite3

# Create db connection and cursor

# Create connention for the database
connection = sqlite3.connect("database.db")
# Create cursor to execute SQL commands
cursor = connection.cursor()

# Create the shipment table if it doesn't exist and insert some sample data
cursor.execute("""
CREATE TABLE IF NOT EXISTS shipment (
        id INTEGER,
        weight REAL,
        content TEXT,
        destination INTEGER,
        status TEXT
    )
""")

# Insert sample data into the shipment table
cursor.execute("""
INSERT INTO shipment
VALUES
    (12001, 10.5, 'Books', 101, 'placed'),
    (12002, 5.0, 'Clothing', 102, 'in_transit'),
    (12003, 2.0, 'Electronics', 103, 'out_for_delivery'),
    (12004, 15.0, 'Furniture', 104, 'delivered')
""")
# Commit the changes to the database
connection.commit()

# Close the database connection
connection.close()