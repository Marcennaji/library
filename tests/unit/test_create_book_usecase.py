"""Tests unitaires du use case CreateBookUseCase."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from datetime import datetime
from application.usecases.create_book import CreateBookUseCase
from tests.fixtures.in_memory_book_repository import InMemoryBookRepository
from tests.fixtures.fixed_clock import FixedClock
from tests.fixtures.fixed_id_generator import FixedIDGenerator


def test_create_book_success():
    """Test : création d'un livre avec succès."""
    # Arrange
    book_repo = InMemoryBookRepository()
    fixed_time = datetime(2025, 1, 1, 10, 0, 0)
    clock = FixedClock(fixed_time)
    id_gen = FixedIDGenerator()
    
    use_case = CreateBookUseCase(book_repo, id_gen, clock)
    
    # Act
    book = use_case.execute("1984", "George Orwell", "978-0451524935")
    
    # Assert
    assert book.id == "TEST-B1"
    assert book.title == "1984"
    assert book.author == "George Orwell"
    assert book.isbn == "978-0451524935"
    assert book.status == "available"
    assert book.registered_at == fixed_time
    
    # Vérifier que le livre est bien sauvegardé
    saved_book = book_repo.get_by_id("TEST-B1")
    assert saved_book is not None
    assert saved_book.title == "1984"


def test_create_book_without_isbn():
    """Test : création d'un livre sans ISBN."""
    book_repo = InMemoryBookRepository()
    clock = FixedClock(datetime(2025, 1, 1))
    id_gen = FixedIDGenerator()
    
    use_case = CreateBookUseCase(book_repo, id_gen, clock)
    book = use_case.execute("Le Petit Prince", "Saint-Exupéry", None)
    
    assert book.isbn is None
    assert book.title == "Le Petit Prince"
