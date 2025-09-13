import functools

def log_queries(func):
    """
    Decorator to log SQL queries before executing them.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") if "query" in kwargs else (args[0] if args else None)
        if query:
            print(f"[LOG] Executing SQL Query: {query}")
        return func(*args, **kwargs)
    return wrapper

# Example usage
@log_queries
def execute_query(query, connection):
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results
