"""
Tests du LibraryService - VERSION DIFFICILE À TESTER

⚠️  ATTENTION : Ces tests sont INTENTIONNELLEMENT mauvais !

Ils démontrent les problèmes du code mal architecturé :
- ❌ Impossible d'isoler la DB (chemin hardcodé dans get_connection())
- ❌ Tous les tests modifient la même DB "library.db"
- ❌ Dates système non contrôlables
- ❌ Tests interdépendants (effets de bord)
- ❌ Tests fragiles et lents

COMPARAISON :
- Branche main : 4 tests difficiles, tous avec DB réelle
- Branche refactored-hexagonal : 23 tests faciles, dont 21 sans DB

L'objectif pédagogique est de montrer POURQUOI l'architecture importe.
"""
import os
import pytest
from services.library_service import LibraryService
from database.init_db import init_database


def setup_function():
    """
    Prépare la DB avant chaque test.
    
    PROBLÈME : On est forcé d'utiliser library.db (hardcodé)
    et on ne peut pas l'isoler entre les tests.
    """
    db_path = "library.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Initialiser la DB
    init_database()


def teardown_function():
    """Nettoie la DB après chaque test."""
    db_path = "library.db"
    if os.path.exists(db_path):
        os.remove(db_path)


def test_create_book(capsys):
    """
    Test de création de livre.
    
    PROBLÈMES :
    - ✗ Nécessite une vraie DB SQLite
    - ✗ Le service fait des print() qu'on doit capturer
    - ✗ L'ID est généré séquentiellement (dépend de l'ordre des tests)
    - ✗ Impossible de mocker la DB (chemin hardcodé)
    """
    service = LibraryService()
    service.create_book("Le Petit Prince", "Antoine de Saint-Exupéry", "978-2-07-061275-8")
    
    captured = capsys.readouterr()
    assert "créé avec succès" in captured.out  # Fragile : dépend du texte exact


def test_create_member(capsys):
    """
    Test de création de membre.
    
    PROBLÈMES :
    - ✗ Couplé à la DB
    - ✗ print() à capturer
    - ✗ ID imprévisible
    """
    service = LibraryService()
    service.create_member("Alice Dupont", "alice@example.com")
    
    captured = capsys.readouterr()
    assert "enregistré avec succès" in captured.out  # Fragile : dépend du texte exact


def test_borrow_book_integration(capsys):
    """
    Test d'emprunt de livre (test d'intégration forcé).
    
    PROBLÈMES MAJEURS :
    - ✗ Test d'intégration obligatoire (impossible de mocker)
    - ✗ Dépend de l'ordre d'exécution (IDs séquentiels)
    - ✗ datetime.now() non contrôlable (dates imprévisibles)
    - ✗ DB réelle nécessaire
    - ✗ Effets de bord multiples
    """
    service = LibraryService()
    
    # Créer un livre
    service.create_book("1984", "George Orwell", "")  # ISBN optionnel mais obligatoire
    capsys.readouterr()
    book_id = "B1"  # On suppose que c'est le premier
    
    # Créer un membre
    service.create_member("Bob Martin", "bob@example.com")
    capsys.readouterr()
    member_id = "M1"
    
    # Emprunter le livre
    service.borrow_book(book_id, member_id)
    captured = capsys.readouterr()
    assert "emprunté" in captured.out  # Fragile
    
    # Vérifier qu'on ne peut pas emprunter deux fois
    service.borrow_book(book_id, member_id)
    captured = capsys.readouterr()
    assert "n'est pas disponible" in captured.out


def test_return_book_integration(capsys):
    """
    Test de retour de livre.
    
    PROBLÈMES :
    - ✗ Dépend du test précédent (setup complexe)
    - ✗ Nécessite de créer livre + membre + emprunt
    - ✗ Dates non contrôlables
    """
    service = LibraryService()
    
    # Setup complet nécessaire
    service.create_book("Le Seigneur des Anneaux", "J.R.R. Tolkien", "")
    capsys.readouterr()
    book_id = "B1"
    
    service.create_member("Charlie Brown", "charlie@example.com")
    capsys.readouterr()
    member_id = "M1"
    
    service.borrow_book(book_id, member_id)
    capsys.readouterr()
    
    # Enfin, le test du retour
    service.return_book(book_id)
    captured = capsys.readouterr()
    assert "retourné avec succès" in captured.out  # Fragile
