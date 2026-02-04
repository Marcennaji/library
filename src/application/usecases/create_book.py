"""Use case : Créer un nouveau livre."""

from domain.book import Book
from ports.book_repository import BookRepository
from ports.id_generator import IDGenerator
from ports.clock import Clock


class CreateBookUseCase:
    """Cas d'usage pour créer un nouveau livre."""
    
    def __init__(self, book_repository: BookRepository, id_generator: IDGenerator, clock: Clock):
        self.book_repository = book_repository
        self.id_generator = id_generator
        self.clock = clock
    
    def execute(self, title: str, author: str, isbn: str | None = None) -> Book:
        """Crée et sauvegarde un nouveau livre."""
        book_id = self.id_generator.generate_book_id()
        registered_at = self.clock.now()
        
        book = Book(
            id=book_id,
            title=title,
            author=author,
            isbn=isbn,
            status="available",
            registered_at=registered_at
        )
        
        self.book_repository.save(book)
        return book
