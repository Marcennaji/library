"""Entité Loan - Domaine pur."""

from datetime import datetime, timedelta


class Loan:
    """Représente un emprunt de livre (entité du domaine)."""
    
    def __init__(self, id: str, book_id: str, member_id: str, 
                 borrowed_at: datetime, due_date: datetime, 
                 returned_at: datetime | None = None):
        self.id = id
        self.book_id = book_id
        self.member_id = member_id
        self.borrowed_at = borrowed_at
        self.due_date = due_date
        self.returned_at = returned_at
    
    def is_overdue(self, current_time: datetime) -> bool:
        """Vérifie si l'emprunt est en retard (logique métier avec Clock injecté)."""
        if self.returned_at:
            return False
        return current_time > self.due_date
    
    def mark_as_returned(self, return_time: datetime):
        """Marque l'emprunt comme retourné (logique métier)."""
        self.returned_at = return_time
