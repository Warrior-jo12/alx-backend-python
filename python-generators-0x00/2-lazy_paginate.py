import mysql.connector

# Connect to the ALX_prodev database
def connect_to_prodev():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="ALX_prodev"
    )

# Function to fetch a single page of users
def paginate_users(page_size, offset):
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
    cursor.execute(query, (page_size, offset))
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

# Generator function for lazy pagination
def lazy_paginate(page_size):
    offset = 0
    while True:
        rows = paginate_users(page_size, offset)
        if not rows:
            break
        yield rows
        offset += page_size

# Example usage
if __name__ == "__main__":
    page_size = 2
    for page in lazy_paginate(page_size):
        print("New Page:")
        for user in page:
            print(user)
