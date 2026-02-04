"""Modèle Member - Gère les membres."""

import sqlite3
from datetime import datetime
from database.db_connection import get_connection


class Member:
    """Représente un membre de la bibliothèque."""
    
    def __init__(self, id, name, email, registered_at=None):
        if not name or len(name) < 2:
            raise ValueError("Le nom doit contenir au moins 2 caractères")
        
        if not email or '@' not in email:
            raise ValueError("Adresse email invalide")
        
        self.id = id
        self.name = name
        self.email = email
        self.registered_at = registered_at or datetime.now()
    
    def save(self):
        """Sauvegarde le membre en base de données."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO members (id, name, email, registered_at)
            VALUES (?, ?, ?, ?)
        """, (self.id, self.name, self.email, self.registered_at))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_by_id(member_id):
        """Récupère un membre par son ID."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM members WHERE id = ?", (member_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Member(row[0], row[1], row[2], row[3])
        return None
