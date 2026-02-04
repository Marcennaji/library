"""Interface CLI - Système de gestion de bibliothèque."""

from services.library_service import LibraryService
from database.init_db import init_database


def display_menu():
    """Affiche le menu principal."""
    print("\n" + "="*50)
    print("📚 SYSTÈME DE GESTION DE BIBLIOTHÈQUE")
    print("="*50)
    print("1. Créer un nouveau livre")
    print("2. Enregistrer un nouveau membre")
    print("3. Emprunter un livre")
    print("4. Retourner un livre")
    print("5. Lister tous les livres")
    print("6. Lister les livres disponibles")
    print("7. Lister tous les membres")
    print("0. Quitter")
    print("="*50)


def main():
    """Point d'entrée principal."""
    print("Initialisation du système de bibliothèque...")
    init_database()
    
    service = LibraryService()
    
    while True:
        display_menu()
        choice = input("\nChoisissez une option : ").strip()
        
        if choice == "1":
            title = input("Titre du livre : ").strip()
            author = input("Auteur : ").strip()
            isbn = input("ISBN (optionnel) : ").strip() or None
            service.create_book(title, author, isbn)
        
        elif choice == "2":
            name = input("Nom du membre : ").strip()
            email = input("Email : ").strip()
            service.create_member(name, email)
        
        elif choice == "3":
            book_id = input("ID du livre : ").strip()
            member_id = input("ID du membre : ").strip()
            service.borrow_book(book_id, member_id)
        
        elif choice == "4":
            book_id = input("ID du livre : ").strip()
            service.return_book(book_id)
        
        elif choice == "5":
            service.list_all_books()
        
        elif choice == "6":
            service.list_available_books()
        
        elif choice == "7":
            service.list_all_members()
        
        elif choice == "0":
            print("Au revoir !")
            break
        
        else:
            print("Option invalide. Veuillez réessayer.")


if __name__ == "__main__":
    main()
