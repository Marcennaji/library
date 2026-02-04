"""
Point d'entrée principal - Composition Root.

Ce fichier est responsable de :
1. Instancier tous les adapters (implémentations concrètes)
2. Instancier les use cases en injectant leurs dépendances
3. Démarrer l'application
"""

import sys
from pathlib import Path

# Ajouter src/ au path pour les imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from adapters.db.init_db import init_database
from adapters.db.book_repository_sqlite import SQLiteBookRepository
from adapters.db.member_repository_sqlite import SQLiteMemberRepository
from adapters.db.loan_repository_sqlite import SQLiteLoanRepository
from adapters.system_clock import SystemClock
from adapters.sequential_id_generator import SequentialIDGenerator
from adapters.cli.cli_adapter import CLIAdapter

from application.usecases.create_book import CreateBookUseCase
from application.usecases.create_member import CreateMemberUseCase
from application.usecases.borrow_book import BorrowBookUseCase
from application.usecases.return_book import ReturnBookUseCase
from application.usecases.list_books import ListBooksUseCase
from application.usecases.list_members import ListMembersUseCase


def main():
    """Composition root - configure et démarre l'application."""
    print("Initialisation du système de bibliothèque...")
    
    # 1. Initialiser la base de données
    init_database()
    print("Base de données initialisée avec succès.")
    
    # 2. Instancier les adapters (implémentations des ports)
    book_repo = SQLiteBookRepository()
    member_repo = SQLiteMemberRepository()
    loan_repo = SQLiteLoanRepository()
    clock = SystemClock()
    id_generator = SequentialIDGenerator(book_repo, member_repo, loan_repo)
    
    # 3. Instancier les use cases avec injection de dépendances
    create_book_uc = CreateBookUseCase(book_repo, id_generator, clock)
    create_member_uc = CreateMemberUseCase(member_repo, id_generator, clock)
    borrow_book_uc = BorrowBookUseCase(book_repo, member_repo, loan_repo, id_generator, clock)
    return_book_uc = ReturnBookUseCase(book_repo, loan_repo, clock)
    list_books_uc = ListBooksUseCase(book_repo)
    list_members_uc = ListMembersUseCase(member_repo)
    
    # 4. Instancier l'adaptateur CLI
    cli = CLIAdapter(
        create_book_uc,
        create_member_uc,
        borrow_book_uc,
        return_book_uc,
        list_books_uc,
        list_members_uc
    )
    
    # 5. Lancer l'application
    cli.run()


if __name__ == "__main__":
    main()
