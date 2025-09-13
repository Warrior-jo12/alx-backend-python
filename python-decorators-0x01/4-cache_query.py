import time
import sqlite3
import functools

query_cache = {}

# Assume with_db_connection is already defined
# from your previous task

def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Use the query string as the cache key
        query = kwargs.get('query') if 'query' in kwargs else args[1]  # args[0] is conn
        if query in query_cache:
            print("Returning cached result for query:", query)
            return query_cache[query]
        
        result = func(*args, **kwargs)
        query_cache[query] = result
        print("Caching result for query:", query)
        return result
    return wrapper

# Usage
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call caches the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call retrieves from cache
users_again = fetch_users_with_cache(query="SELECT * FROM users")
