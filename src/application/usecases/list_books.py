"""Use case : Lister les livres."""

from typing import List
from domain.book import Book
from ports.book_repository import BookRepository


class ListBooksUseCase:
    """Cas d'usage pour lister les livres."""
    
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository
    
    def execute_all(self) -> List[Book]:
        """Liste tous les livres."""
        return self.book_repository.list_all()
    
    def execute_available(self) -> List[Book]:
        """Liste les livres disponibles."""
        return self.book_repository.list_available()
