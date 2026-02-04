"""Repository Loan en mémoire pour les tests."""

from domain.loan import Loan
from ports.loan_repository import LoanRepository


class InMemoryLoanRepository(LoanRepository):
    """Implémentation en mémoire du repository d'emprunts (pour tests)."""
    
    def __init__(self):
        self._loans = {}
    
    def save(self, loan: Loan) -> None:
        """Sauvegarde un emprunt en mémoire."""
        self._loans[loan.id] = loan
    
    def find_active_loan(self, book_id: str) -> Loan | None:
        """Trouve un emprunt actif pour un livre."""
        for loan in self._loans.values():
            if loan.book_id == book_id and loan.returned_at is None:
                return loan
        return None
    
    def count(self) -> int:
        """Compte le nombre total d'emprunts."""
        return len(self._loans)
    
    def clear(self):
        """Vide le repository (utile entre les tests)."""
        self._loans.clear()
