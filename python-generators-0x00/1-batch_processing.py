import mysql.connector

# Connect to the ALX_prodev database
def connect_to_prodev():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # put your password here
        database="ALX_prodev"
    )

# Generator to fetch users in batches
def stream_users_in_batches(batch_size):
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    offset = 0
    while True:
        cursor.execute(f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset}")
        rows = cursor.fetchall()
        if not rows:
            break
        yield rows
        offset += batch_size
    cursor.close()
    connection.close()

# Process each batch to filter users over age 25
def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        # Loop over the batch and yield users over 25
        for user in batch:
            if user['age'] > 25:
                yield user

# Example usage
if __name__ == "__main__":
    for user in batch_processing(3):
        print(user)
