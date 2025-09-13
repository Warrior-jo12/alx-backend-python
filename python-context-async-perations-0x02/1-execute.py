import sqlite3

class ExecuteQuery:
    def __init__(self, query, params=None, db_path=":memory:"):
        self.query = query
        self.params = params or ()
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        # Open database connection
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        # Execute query with parameters
        self.cursor.execute(self.query, self.params)
        self.result = self.cursor.fetchall()
        return self.result

    def __exit__(self, exc_type, exc_value, traceback):
        # Close cursor and connection
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        # Propagate exception if any
        return False

# Example usage
query = "SELECT * FROM users WHERE age > ?"
with ExecuteQuery(query, (25,)) as results:
    print(results)
