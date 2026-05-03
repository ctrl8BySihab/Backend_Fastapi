import sqlite3
from typing import Any
from app.schemas import ShipmentStatus, ShipmentRead, ShipmentCreate, ShipmentUpdate

conn = sqlite3.connect("database.db")
cur = conn.cursor()


class Database:
    def __init__(self):
        # Create connection and cursor
        self.conn = sqlite3.connect("database.db", check_same_thread=False)
        self.cur = self.conn.cursor()

        self.create_table()
    
    # Create table in the database
    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXIST shipment (
                        id INTEGER PRIMARY KEY, 
                        weight REAL, 
                        content TEXT,
                        status TEXT
                        )
        
        """)
        self.conn.commit()

    # To get the shipment using the id
    def get(self, id: int) -> dict[str, Any] | None:
        self.cur.execute("""
            SELECT * FROM shipment
            WHERE id =:id

        """,
        {"id" : id}
        )
        data = self.cur.fetchone()

        return {
            "id" : data[0],
            "weight" : data[1],
            "content" : data[2],
            "status" : data[3]
        } if data else None
    
    # Submitting new order
    def submit(self, shipment: ShipmentCreate) -> int:
        self.cur.execute("""
            SELECT MAX(id) FROM shipment
        """)
        new_id = self.cur.fetchone()[0] + 1
        
        self.cur.execute("""
            INSERT INTO shipment
            VALUES (:id, :weight, :content, :status)
        """,
        {
            "id": new_id,
            **shipment.model_dump(),
            "status": "placed"
        }
        )
        self.conn.commit()
        return new_id
    
    # Update order
    def update(self, id: int, shipment: ShipmentUpdate) -> dict[str, Any] | None:
        cur.execute("""
            UPDATE shipment
            SET status =:status
            WHERE id =:id
        """,
        {"id" : id, **shipment.model_dump()}
        )
        self.conn.commit()
        return self.get(id)
    
    
    def

    # Close the connection
    def close(self):
        self.conn.close()
