import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        # Open the database connection
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Commit changes if no exception, rollback otherwise
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        # Close the connection
        self.conn.close()
        # Suppress exception propagation
        return False

# Usage example
with DatabaseConnection("airbnb.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    for user in users:
        print(user)
