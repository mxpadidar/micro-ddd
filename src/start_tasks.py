from workers.main import start_auth_cursor, start_storage_cursor

if __name__ == "__main__":
    start_auth_cursor.delay()
    start_storage_cursor.delay()
