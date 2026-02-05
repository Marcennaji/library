"""Modèle Book - Gère les livres."""

import sqlite3
from datetime import datetime
from database.db_connection import get_connection


def _parse_datetime(value):
    """Convertit une string ISO en datetime."""
    if value is None:
        return None
    if isinstance(value, str):
        return datetime.fromisoformat(value)
    return value


class Book:
    """Représente un livre dans la bibliothèque."""
    
    def __init__(self, id, title, author, isbn, status="available", registered_at=None):
        if not title or len(title) < 2:
            raise ValueError("Le titre doit contenir au moins 2 caractères")
        
        if not author or len(author) < 2:
            raise ValueError("L'auteur doit contenir au moins 2 caractères")
        
        self.id = id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status
        self.registered_at = registered_at or datetime.now()
    
    def is_available(self):
        """Vérifie si le livre est disponible pour emprunt."""
        return self.status == "available"
    
    def mark_as_borrowed(self):
        """Marque le livre comme emprunté."""
        if not self.is_available():
            raise ValueError(f"Le livre n'est pas disponible (statut: {self.status})")
        self.status = "borrowed"
    
    def mark_as_returned(self):
        """Marque le livre comme retourné et disponible."""
        self.status = "available"
    
    def save(self):
        """Sauvegarde le livre en base de données."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO books (id, title, author, isbn, status, registered_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (self.id, self.title, self.author, self.isbn, self.status, self.registered_at.isoformat()))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_by_id(book_id):
        """Récupère un livre par son ID."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Book(row[0], row[1], row[2], row[3], row[4], _parse_datetime(row[5]))
        return None
    
    @staticmethod
    def list_all():
        """Liste tous les livres."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM books")
        rows = cursor.fetchall()
        conn.close()
        
        return [Book(row[0], row[1], row[2], row[3], row[4], _parse_datetime(row[5])) for row in rows]
    
    @staticmethod
    def list_available():
        """Liste tous les livres disponibles."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM books WHERE status = 'available'")
        rows = cursor.fetchall()
        conn.close()
        
        return [Book(r[0], r[1], r[2], r[3], r[4], _parse_datetime(r[5])) for r in rows]
