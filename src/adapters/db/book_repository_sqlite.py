"""Adaptateur SQLite pour BookRepository."""

import sqlite3
from typing import List
from domain.book import Book
from ports.book_repository import BookRepository


class SQLiteBookRepository(BookRepository):
    """Implémentation SQLite du repository de livres."""
    
    def __init__(self, db_path: str = "library.db"):
        self.db_path = db_path
    
    def _get_connection(self):
        """Crée une connexion à la base de données."""
        return sqlite3.connect(self.db_path)
    
    def save(self, book: Book) -> None:
        """Sauvegarde un livre en base de données."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO books (id, title, author, isbn, status, registered_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (book.id, book.title, book.author, book.isbn, book.status, book.registered_at))
        
        conn.commit()
        conn.close()
    
    def get_by_id(self, book_id: str) -> Book | None:
        """Récupère un livre par son ID."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Book(row[0], row[1], row[2], row[3], row[4], row[5])
        return None
    
    def list_all(self) -> List[Book]:
        """Liste tous les livres."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM books")
        rows = cursor.fetchall()
        conn.close()
        
        return [Book(r[0], r[1], r[2], r[3], r[4], r[5]) for r in rows]
    
    def list_available(self) -> List[Book]:
        """Liste les livres disponibles."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM books WHERE status = 'available'")
        rows = cursor.fetchall()
        conn.close()
        
        return [Book(r[0], r[1], r[2], r[3], r[4], r[5]) for r in rows]
    
    def count(self) -> int:
        """Compte le nombre total de livres."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM books")
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
