"""Adaptateur SQLite pour MemberRepository."""

import sqlite3
from typing import List
from domain.member import Member
from ports.member_repository import MemberRepository


class SQLiteMemberRepository(MemberRepository):
    """Implémentation SQLite du repository de membres."""
    
    def __init__(self, db_path: str = "library.db"):
        self.db_path = db_path
    
    def _get_connection(self):
        """Crée une connexion à la base de données."""
        return sqlite3.connect(self.db_path)
    
    def save(self, member: Member) -> None:
        """Sauvegarde un membre en base de données."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO members (id, name, email, registered_at)
            VALUES (?, ?, ?, ?)
        """, (member.id, member.name, member.email, member.registered_at))
        
        conn.commit()
        conn.close()
    
    def get_by_id(self, member_id: str) -> Member | None:
        """Récupère un membre par son ID."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM members WHERE id = ?", (member_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Member(row[0], row[1], row[2], row[3])
        return None
    
    def list_all(self) -> List[Member]:
        """Liste tous les membres."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM members")
        rows = cursor.fetchall()
        conn.close()
        
        return [Member(r[0], r[1], r[2], r[3]) for r in rows]
    
    def count(self) -> int:
        """Compte le nombre total de membres."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM members")
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
