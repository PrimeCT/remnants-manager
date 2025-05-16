
import sqlite3

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)
    return conn

def create_table(conn):
    try:
        sql_create_remnants_table = """
        CREATE TABLE IF NOT EXISTS remnants (
            id integer PRIMARY KEY,
            name text NOT NULL,
            material text,
            size text,
            location text,
            used_in text,
            photo_url text
        );
        """
        c = conn.cursor()
        c.execute(sql_create_remnants_table)
    except Exception as e:
        print(e)
    