"""Repository Book en mémoire pour les tests."""

from typing import List
from domain.book import Book
from ports.book_repository import BookRepository


class InMemoryBookRepository(BookRepository):
    """Implémentation en mémoire du repository de livres (pour tests)."""
    
    def __init__(self):
        self._books = {}
    
    def save(self, book: Book) -> None:
        """Sauvegarde un livre en mémoire."""
        self._books[book.id] = book
    
    def get_by_id(self, book_id: str) -> Book | None:
        """Récupère un livre par son ID."""
        return self._books.get(book_id)
    
    def list_all(self) -> List[Book]:
        """Liste tous les livres."""
        return list(self._books.values())
    
    def list_available(self) -> List[Book]:
        """Liste les livres disponibles."""
        return [b for b in self._books.values() if b.is_available()]
    
    def count(self) -> int:
        """Compte le nombre total de livres."""
        return len(self._books)
    
    def clear(self):
        """Vide le repository (utile entre les tests)."""
        self._books.clear()
