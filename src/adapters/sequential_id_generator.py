"""Adaptateur IDGenerator avec IDs courts séquentiels."""

from ports.id_generator import IDGenerator
from ports.book_repository import BookRepository
from ports.member_repository import MemberRepository
from ports.loan_repository import LoanRepository


class SequentialIDGenerator(IDGenerator):
    """Générateur d'IDs courts séquentiels (B1, M1, L1...)."""
    
    def __init__(self, book_repo: BookRepository, member_repo: MemberRepository, loan_repo: LoanRepository):
        self.book_repo = book_repo
        self.member_repo = member_repo
        self.loan_repo = loan_repo
    
    def generate_book_id(self) -> str:
        """Génère un ID pour un livre (B1, B2, B3...)."""
        count = self.book_repo.count()
        return f"B{count + 1}"
    
    def generate_member_id(self) -> str:
        """Génère un ID pour un membre (M1, M2, M3...)."""
        count = self.member_repo.count()
        return f"M{count + 1}"
    
    def generate_loan_id(self) -> str:
        """Génère un ID pour un emprunt (L1, L2, L3...)."""
        count = self.loan_repo.count()
        return f"L{count + 1}"
