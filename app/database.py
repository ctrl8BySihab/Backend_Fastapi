import sqlite3

# Create db connection and cursor

# Create connention for the database
connection = sqlite3.connect("database.db")
# Create cursor to execute SQL commands
cursor = connection.cursor()

# # Create the shipment table if it doesn't exist and insert some sample data
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS shipment (
#         id INTEGER,
#         weight REAL,
#         content TEXT,
#         destination INTEGER,
#         status TEXT
#     )
# """)

# # Insert sample data into the shipment table
# cursor.execute("""
# INSERT INTO shipment
# VALUES
#     (12001, 10.5, 'Books', 101, 'placed'),
#     (12002, 5.0, 'Clothing', 102, 'in_transit'),
#     (12003, 2.0, 'Electronics', 103, 'out_for_delivery'),
#     (12004, 15.0, 'Furniture', 104, 'delivered')
# """)
# # Commit the changes to the database
# connection.commit()

# # Display all shipments in the database
# cursor.execute("""
# SELECT * FROM shipment where id = 12002
# """)
# data = cursor.fetchall()
# print(data)

# # Update the status of a shipment
id = 12004  # This is a malicious input that could lead to SQL injection
status = "on_hold"
cursor.execute("""
UPDATE shipment SET status =:status WHERE id =:id
""", {"id": id, "status": status})
# Commit the changes to the database
connection.commit()

# Close the database connection
connection.close()