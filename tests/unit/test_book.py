"""Tests unitaires de l'entité Book."""

import pytest
from datetime import datetime
from domain.book import Book


def test_book_creation_valid():
    """Test : création d'un livre valide."""
    book = Book(
        id="B1",
        title="1984",
        author="George Orwell",
        isbn="978-0451524935",
        status="available",
        registered_at=datetime(2025, 1, 1)
    )
    
    assert book.id == "B1"
    assert book.title == "1984"
    assert book.author == "George Orwell"
    assert book.isbn == "978-0451524935"
    assert book.status == "available"


def test_book_creation_invalid_title():
    """Test : création d'un livre avec titre invalide."""
    with pytest.raises(ValueError, match="au moins 2 caractères"):
        Book("B1", "A", "Auteur", None)


def test_book_creation_invalid_author():
    """Test : création d'un livre avec auteur invalide."""
    with pytest.raises(ValueError, match="au moins 2 caractères"):
        Book("B1", "Titre", "A", None)


def test_book_is_available():
    """Test : vérification de disponibilité."""
    book = Book("B1", "Titre", "Auteur", None, status="available")
    assert book.is_available() is True
    
    book.status = "borrowed"
    assert book.is_available() is False


def test_book_mark_as_borrowed():
    """Test : marquer un livre comme emprunté."""
    book = Book("B1", "Titre", "Auteur", None, status="available")
    book.mark_as_borrowed()
    
    assert book.status == "borrowed"
    assert book.is_available() is False


def test_book_mark_as_borrowed_when_not_available():
    """Test : impossible d'emprunter un livre déjà emprunté."""
    book = Book("B1", "Titre", "Auteur", None, status="borrowed")
    
    with pytest.raises(ValueError, match="n'est pas disponible"):
        book.mark_as_borrowed()


def test_book_mark_as_returned():
    """Test : marquer un livre comme retourné."""
    book = Book("B1", "Titre", "Auteur", None, status="borrowed")
    book.mark_as_returned()
    
    assert book.status == "available"
    assert book.is_available() is True
