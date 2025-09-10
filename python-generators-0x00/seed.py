import mysql.connector
from mysql.connector import errorcode
import uuid
import csv

CSV_FILE = "user_data.csv"  # Make sure this file is in the same directory

# 1. Connect to MySQL server
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""  # replace with your MySQL password
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# 2. Create database
def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev ready.")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
    cursor.close()

# 3. Connect to ALX_prodev
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # replace with your MySQL password
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# 4. Create table
def create_table(connection):
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(5,2) NOT NULL,
        INDEX (user_id)
    )
    """
    try:
        cursor.execute(create_table_query)
        print("Table user_data ready.")
    except mysql.connector.Error as err:
        print(f"Failed creating table: {err}")
    cursor.close()

# 5. Insert data from CSV
def insert_data_from_csv(connection, csv_file):
    cursor = connection.cursor()
    try:
        with open(csv_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                user_id = str(uuid.uuid4())
                cursor.execute(
                    "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                    (user_id, row["name"], row["email"], float(row["age"]))
                )
        connection.commit()
        print("Data inserted successfully from CSV.")
    except FileNotFoundError:
        print(f"File {csv_file} not found.")
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
    cursor.close()

# 6. Generator to stream rows one by one
def stream_rows(connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield row
    cursor.close()

# ---- MAIN ----
if __name__ == "__main__":
    conn = connect_db()
    if conn:
        create_database(conn)
        conn.close()

    conn = connect_to_prodev()
    if conn:
        create_table(conn)
        insert_data_from_csv(conn, CSV_FILE)

        print("\nStreaming rows one by one:")
        for row in stream_rows(conn):
            print(row)

        conn.close()
