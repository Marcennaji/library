"""Tests unitaires du use case BorrowBookUseCase."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import pytest
from datetime import datetime, timedelta
from application.usecases.borrow_book import BorrowBookUseCase
from domain.book import Book
from domain.member import Member
from tests.fixtures.in_memory_book_repository import InMemoryBookRepository
from tests.fixtures.in_memory_member_repository import InMemoryMemberRepository
from tests.fixtures.in_memory_loan_repository import InMemoryLoanRepository
from tests.fixtures.fixed_clock import FixedClock
from tests.fixtures.fixed_id_generator import FixedIDGenerator


def test_borrow_book_success():
    """Test : emprunt d'un livre avec succès."""
    # Arrange
    book_repo = InMemoryBookRepository()
    member_repo = InMemoryMemberRepository()
    loan_repo = InMemoryLoanRepository()
    fixed_time = datetime(2025, 1, 1, 10, 0, 0)
    clock = FixedClock(fixed_time)
    id_gen = FixedIDGenerator()
    
    # Créer un livre et un membre
    book = Book("B1", "1984", "Orwell", None, "available", fixed_time)
    member = Member("M1", "Alice", "alice@example.com", fixed_time)
    book_repo.save(book)
    member_repo.save(member)
    
    use_case = BorrowBookUseCase(book_repo, member_repo, loan_repo, id_gen, clock)
    
    # Act
    loan = use_case.execute("B1", "M1")
    
    # Assert
    assert loan.id == "TEST-L1"
    assert loan.book_id == "B1"
    assert loan.member_id == "M1"
    assert loan.borrowed_at == fixed_time
    assert loan.due_date == fixed_time + timedelta(days=14)
    
    # Vérifier que le livre est marqué comme emprunté
    borrowed_book = book_repo.get_by_id("B1")
    assert borrowed_book.status == "borrowed"


def test_borrow_book_not_found():
    """Test : emprunt d'un livre inexistant."""
    book_repo = InMemoryBookRepository()
    member_repo = InMemoryMemberRepository()
    loan_repo = InMemoryLoanRepository()
    clock = FixedClock(datetime(2025, 1, 1))
    id_gen = FixedIDGenerator()
    
    use_case = BorrowBookUseCase(book_repo, member_repo, loan_repo, id_gen, clock)
    
    with pytest.raises(ValueError, match="Livre non trouvé"):
        use_case.execute("B999", "M1")


def test_borrow_book_member_not_found():
    """Test : emprunt par un membre inexistant."""
    book_repo = InMemoryBookRepository()
    member_repo = InMemoryMemberRepository()
    loan_repo = InMemoryLoanRepository()
    clock = FixedClock(datetime(2025, 1, 1))
    id_gen = FixedIDGenerator()
    
    book = Book("B1", "1984", "Orwell", None, "available", clock.now())
    book_repo.save(book)
    
    use_case = BorrowBookUseCase(book_repo, member_repo, loan_repo, id_gen, clock)
    
    with pytest.raises(ValueError, match="Membre non trouvé"):
        use_case.execute("B1", "M999")


def test_borrow_book_not_available():
    """Test : emprunt d'un livre déjà emprunté."""
    book_repo = InMemoryBookRepository()
    member_repo = InMemoryMemberRepository()
    loan_repo = InMemoryLoanRepository()
    clock = FixedClock(datetime(2025, 1, 1))
    id_gen = FixedIDGenerator()
    
    book = Book("B1", "1984", "Orwell", None, "borrowed", clock.now())  # Déjà emprunté
    member = Member("M1", "Alice", "alice@example.com", clock.now())
    book_repo.save(book)
    member_repo.save(member)
    
    use_case = BorrowBookUseCase(book_repo, member_repo, loan_repo, id_gen, clock)
    
    with pytest.raises(ValueError, match="n'est pas disponible"):
        use_case.execute("B1", "M1")
