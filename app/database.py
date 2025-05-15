import sqlite3

def connect_db():
    conn = sqlite3.connect("data/remnants.db")
    return conn

def create_tables():
    conn = connect_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS remnants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            material TEXT,
            largura REAL,
            altura REAL,
            status TEXT,
            imagem_url TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS historico_uso (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            remnant_id INTEGER,
            projeto TEXT,
            data_uso TEXT
        )
    ''')
    conn.commit()
    conn.close()
