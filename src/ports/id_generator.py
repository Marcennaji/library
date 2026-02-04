"""Port IDGenerator - Interface pour la génération d'identifiants."""

from abc import ABC, abstractmethod


class IDGenerator(ABC):
    """Interface pour générer des identifiants."""
    
    @abstractmethod
    def generate_book_id(self) -> str:
        """Génère un ID pour un livre."""
        pass
    
    @abstractmethod
    def generate_member_id(self) -> str:
        """Génère un ID pour un membre."""
        pass
    
    @abstractmethod
    def generate_loan_id(self) -> str:
        """Génère un ID pour un emprunt."""
        pass
