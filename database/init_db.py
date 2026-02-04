"""Initialisation de la base de données."""

from database.db_connection import get_connection


def init_database():
    """Initialise le schéma de la base de données."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT,
            status TEXT DEFAULT 'available',
            registered_at TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            registered_at TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS loans (
            id TEXT PRIMARY KEY,
            book_id TEXT NOT NULL,
            member_id TEXT NOT NULL,
            borrowed_at TIMESTAMP,
            due_date TIMESTAMP,
            returned_at TIMESTAMP,
            FOREIGN KEY (book_id) REFERENCES books (id),
            FOREIGN KEY (member_id) REFERENCES members (id)
        )
    """)
    
    conn.commit()
    conn.close()
    print("Base de données initialisée avec succès.")
