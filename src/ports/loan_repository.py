"""Port LoanRepository - Interface pour la persistance des emprunts."""

from abc import ABC, abstractmethod
from domain.loan import Loan


class LoanRepository(ABC):
    """Interface définissant les opérations de persistance pour Loan."""
    
    @abstractmethod
    def save(self, loan: Loan) -> None:
        """Sauvegarde un emprunt."""
        pass
    
    @abstractmethod
    def find_active_loan(self, book_id: str) -> Loan | None:
        """Trouve un emprunt actif pour un livre."""
        pass
    
    @abstractmethod
    def count(self) -> int:
        """Compte le nombre total d'emprunts."""
        pass
