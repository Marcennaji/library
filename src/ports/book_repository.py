"""Port BookRepository - Interface pour la persistance des livres."""

from abc import ABC, abstractmethod
from typing import List
from domain.book import Book


class BookRepository(ABC):
    """Interface définissant les opérations de persistance pour Book."""
    
    @abstractmethod
    def save(self, book: Book) -> None:
        """Sauvegarde un livre."""
        pass
    
    @abstractmethod
    def get_by_id(self, book_id: str) -> Book | None:
        """Récupère un livre par son ID."""
        pass
    
    @abstractmethod
    def list_all(self) -> List[Book]:
        """Liste tous les livres."""
        pass
    
    @abstractmethod
    def list_available(self) -> List[Book]:
        """Liste les livres disponibles."""
        pass
    
    @abstractmethod
    def count(self) -> int:
        """Compte le nombre total de livres."""
        pass
