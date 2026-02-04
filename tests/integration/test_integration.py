"""Tests d'intégration avec SQLite."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import os
import pytest
from datetime import datetime
from adapters.db.init_db import init_database
from adapters.db.book_repository_sqlite import SQLiteBookRepository
from adapters.db.member_repository_sqlite import SQLiteMemberRepository
from adapters.db.loan_repository_sqlite import SQLiteLoanRepository
from adapters.system_clock import SystemClock
from adapters.sequential_id_generator import SequentialIDGenerator
from application.usecases.create_book import CreateBookUseCase
from application.usecases.create_member import CreateMemberUseCase
from application.usecases.borrow_book import BorrowBookUseCase
from application.usecases.return_book import ReturnBookUseCase


TEST_DB = "test_library.db"


def setup_function():
    """Prépare la DB de test avant chaque test."""
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    init_database(TEST_DB)


def teardown_function():
    """Nettoie la DB de test après chaque test."""
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def test_integration_full_workflow():
    """Test d'intégration : workflow complet (créer livre, membre, emprunter, retourner)."""
    # Arrange
    book_repo = SQLiteBookRepository(TEST_DB)
    member_repo = SQLiteMemberRepository(TEST_DB)
    loan_repo = SQLiteLoanRepository(TEST_DB)
    clock = SystemClock()
    id_gen = SequentialIDGenerator(book_repo, member_repo, loan_repo)
    
    create_book_uc = CreateBookUseCase(book_repo, id_gen, clock)
    create_member_uc = CreateMemberUseCase(member_repo, id_gen, clock)
    borrow_book_uc = BorrowBookUseCase(book_repo, member_repo, loan_repo, id_gen, clock)
    return_book_uc = ReturnBookUseCase(book_repo, loan_repo, clock)
    
    # Act & Assert
    
    # 1. Créer un livre
    book = create_book_uc.execute("1984", "George Orwell", "978-0451524935")
    assert book.id == "B1"
    assert book.title == "1984"
    assert book.status == "available"
    
    # 2. Créer un membre
    member = create_member_uc.execute("Alice Dupont", "alice@example.com")
    assert member.id == "M1"
    assert member.name == "Alice Dupont"
    
    # 3. Emprunter le livre
    loan = borrow_book_uc.execute("B1", "M1")
    assert loan.book_id == "B1"
    assert loan.member_id == "M1"
    
    # Vérifier que le livre est marqué comme emprunté
    book_after_borrow = book_repo.get_by_id("B1")
    assert book_after_borrow.status == "borrowed"
    
    # 4. Retourner le livre
    success, days_overdue = return_book_uc.execute("B1")
    assert success is True
    assert days_overdue == 0  # Pas de retard
    
    # Vérifier que le livre est de nouveau disponible
    book_after_return = book_repo.get_by_id("B1")
    assert book_after_return.status == "available"


def test_integration_multiple_books():
    """Test d'intégration : création de plusieurs livres."""
    book_repo = SQLiteBookRepository(TEST_DB)
    member_repo = SQLiteMemberRepository(TEST_DB)
    loan_repo = SQLiteLoanRepository(TEST_DB)
    clock = SystemClock()
    id_gen = SequentialIDGenerator(book_repo, member_repo, loan_repo)
    
    create_book_uc = CreateBookUseCase(book_repo, id_gen, clock)
    
    # Créer 3 livres
    book1 = create_book_uc.execute("1984", "Orwell", None)
    book2 = create_book_uc.execute("Le Meilleur des mondes", "Huxley", None)
    book3 = create_book_uc.execute("Fahrenheit 451", "Bradbury", None)
    
    assert book1.id == "B1"
    assert book2.id == "B2"
    assert book3.id == "B3"
    
    # Vérifier que tous sont en DB
    all_books = book_repo.list_all()
    assert len(all_books) == 3
    assert all([b.status == "available" for b in all_books])
