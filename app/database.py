import sqlite3
from typing import Any
from app.schemas import ShipmentCreate, ShipmentUpdate
from contextlib import contextmanager

class Database:
    # Create connection to the database 
    def connect_to_database(self):
        # Create connection and cursor
        self.conn = sqlite3.connect("database.db", check_same_thread=False)
        self.cur = self.conn.cursor()
    
    # Create table in the database
    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS shipment (
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
        self.cur.execute("""
            UPDATE shipment
            SET status =:status
            WHERE id =:id
        """,
        {"id" : id, **shipment.model_dump(exclude_none=True)}
        )
        self.conn.commit()
        return self.get(id)
    
    # Delete order
    def delete(self, id):
        self.cur.execute("""
            DELETE FROM shipment
            WHERE id =:id
        """,
        {"id": id}
        )
        self.conn.commit()   

    # To get the latest shipment
    def get_latest(self):
        self.cur.execute("""
            SELECT MAX(id) FROM shipment
        """)
        new_id = self.cur.fetchone()[0]
        return self.get(new_id)

    # Close the connection
    def close(self):
        self.conn.close()

    # # Enter method for context manager
    # def __enter__(self):
    #     self.connect_to_database()
    #     self.create_table()
    #     return self
    
    # # Exit method for context manager
    # def __exit__(self, *args):
    #     self.close()

# Adding Context manager using @contextmanager decorator
@contextmanager
def managed_db():
    db = Database()
    db.connect_to_database()
    db.create_table()

    yield db
    db.close

# Some random test
with managed_db() as db:
    print(db.get(12003))