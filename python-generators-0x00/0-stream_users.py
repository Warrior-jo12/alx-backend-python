import mysql.connector

def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    return mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="ALX_prodev"
    )

def stream_users():
    """
    Generator function that streams rows from the user_data table one by one
    using fetchone(), ideal for very large datasets.
    """
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    row = cursor.fetchone()
    while row:
        yield row
        row = cursor.fetchone()  # fetch the next row

    cursor.close()
    connection.close()


# Example usage:
if __name__ == "__main__":
    for user in stream_users():
        print(user)
