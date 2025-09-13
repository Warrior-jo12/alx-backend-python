import functools
import mysql.connector

# --- Reuse from previous task ---
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


# --- New transactional decorator ---
def transactional(func):
    """
    Decorator that manages database transactions.
    Commits if function succeeds, rolls back if an exception occurs.
    Requires the function to use 'connection' keyword arg from with_db_connection.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        connection = kwargs.get("connection")
        if connection is None:
            raise RuntimeError("transactional requires 'with_db_connection' to provide a connection.")

        try:
            result = func(*args, **kwargs)
            connection.commit()
            print("Transaction committed ✅")
            return result
        except Exception as e:
            connection.rollback()
            print(f"Transaction rolled back ❌ due to error: {e}")
            raise
    return wrapper


# ✅ Example usage
@with_db_connection
@transactional
def insert_user(name, email, age, connection=None):
    cursor = connection.cursor()
    query = "INSERT INTO user_data (user_id, name, email, age) VALUES (UUID(), %s, %s, %s)"
    cursor.execute(query, (name, email, age))
    cursor.close()
    return "User inserted successfully."
