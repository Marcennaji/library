"""Modèle Loan - Gère les emprunts."""

import sqlite3
from datetime import datetime, timedelta
from database.db_connection import get_connection


class Loan:
    """Représente un emprunt de livre."""
    
    def __init__(self, id, book_id, member_id, borrowed_at=None, due_date=None, returned_at=None):
        self.id = id
        self.book_id = book_id
        self.member_id = member_id
        self.borrowed_at = borrowed_at or datetime.now()
        self.due_date = due_date or (self.borrowed_at + timedelta(days=14))
        self.returned_at = returned_at
    
    def is_overdue(self):
        """Vérifie si l'emprunt est en retard."""
        if self.returned_at:
            return False
        return datetime.now() > self.due_date
    
    def mark_as_returned(self):
        """Marque l'emprunt comme retourné."""
        self.returned_at = datetime.now()
    
    def save(self):
        """Sauvegarde l'emprunt en base de données."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO loans (id, book_id, member_id, borrowed_at, due_date, returned_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (self.id, self.book_id, self.member_id, self.borrowed_at, self.due_date, self.returned_at))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def find_active_loan(book_id):
        """Trouve un emprunt actif pour un livre."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM loans 
            WHERE book_id = ? AND returned_at IS NULL
        """, (book_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Loan(row[0], row[1], row[2], row[3], row[4], row[5])
        return None
