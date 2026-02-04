"""Adaptateur SQLite pour LoanRepository."""

import sqlite3
from domain.loan import Loan
from ports.loan_repository import LoanRepository


class SQLiteLoanRepository(LoanRepository):
    """Implémentation SQLite du repository d'emprunts."""
    
    def __init__(self, db_path: str = "library.db"):
        self.db_path = db_path
    
    def _get_connection(self):
        """Crée une connexion à la base de données."""
        return sqlite3.connect(self.db_path)
    
    def save(self, loan: Loan) -> None:
        """Sauvegarde un emprunt en base de données."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO loans (id, book_id, member_id, borrowed_at, due_date, returned_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (loan.id, loan.book_id, loan.member_id, loan.borrowed_at, loan.due_date, loan.returned_at))
        
        conn.commit()
        conn.close()
    
    def find_active_loan(self, book_id: str) -> Loan | None:
        """Trouve un emprunt actif pour un livre."""
        conn = self._get_connection()
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
    
    def count(self) -> int:
        """Compte le nombre total d'emprunts."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM loans")
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
