import functools
import time
from datetime import datetime

def log_queries(func):
    """
    Decorator to log SQL queries with timestamp and execution duration.
    Logs are stored in db_queries.log
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Detect query from args/kwargs
        query = kwargs.get("query") if "query" in kwargs else (args[0] if args else None)
        if query:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] Executing SQL Query: {query}\n"
            print(log_entry.strip())

            # Write initial log
            with open("db_queries.log", "a") as logfile:
                logfile.write(log_entry)

        # Start timer
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = (time.time() - start_time) * 1000  # ms

        # Log duration
        if query:
            duration_entry = f"    └─ Query executed in {duration:.2f} ms\n"
            print(duration_entry.strip())
            with open("db_queries.log", "a") as logfile:
                logfile.write(duration_entry)

        return result
    return wrapper


# Example usage
@log_queries
def execute_query(query, connection):
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results
