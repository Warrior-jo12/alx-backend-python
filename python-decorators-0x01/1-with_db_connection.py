import functools
import mysql.connector

def with_db_connection(func):
    """
    Decorator that opens and closes a database connection automatically.
    The connection is passed to the decorated function as a keyword argument 'connection'.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        connection = None
        try:
            # Open connection
            connection = mysql.connector.connect(
                host="localhost",
                user="your_username",
                password="your_password",
                database="ALX_prodev"
            )
            kwargs["connection"] = connection  # Pass to function
            result = func(*args, **kwargs)
            return result
        finally:
            # Close connection safely
            if connection is not None and connection.is_connected():
                connection.close()
                print("Database connection closed.")
    return wrapper


# ✅ Example usage
@with_db_connection
def fetch_users(connection=None):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")
    rows = cursor.fetchall()
    cursor.close()
    return rows
