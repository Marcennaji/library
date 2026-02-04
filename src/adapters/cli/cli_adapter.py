"""Adaptateur CLI - Interface en ligne de commande."""

from typing import List
from domain.book import Book
from domain.member import Member
from application.usecases.create_book import CreateBookUseCase
from application.usecases.create_member import CreateMemberUseCase
from application.usecases.borrow_book import BorrowBookUseCase
from application.usecases.return_book import ReturnBookUseCase
from application.usecases.list_books import ListBooksUseCase
from application.usecases.list_members import ListMembersUseCase


class CLIAdapter:
    """Adaptateur pour l'interface CLI."""
    
    def __init__(self, create_book_uc: CreateBookUseCase, create_member_uc: CreateMemberUseCase,
                 borrow_book_uc: BorrowBookUseCase, return_book_uc: ReturnBookUseCase,
                 list_books_uc: ListBooksUseCase, list_members_uc: ListMembersUseCase):
        self.create_book_uc = create_book_uc
        self.create_member_uc = create_member_uc
        self.borrow_book_uc = borrow_book_uc
        self.return_book_uc = return_book_uc
        self.list_books_uc = list_books_uc
        self.list_members_uc = list_members_uc
    
    def display_menu(self):
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
    
    def create_book(self):
        """Traite la création d'un livre."""
        title = input("Titre du livre : ").strip()
        author = input("Auteur : ").strip()
        isbn = input("ISBN (optionnel) : ").strip() or None
        
        try:
            book = self.create_book_uc.execute(title, author, isbn)
            print(f"✅ Livre '{title}' créé avec succès ! (ID: {book.id})")
        except ValueError as e:
            print(f"❌ Erreur : {e}")
    
    def create_member(self):
        """Traite l'enregistrement d'un membre."""
        name = input("Nom du membre : ").strip()
        email = input("Email : ").strip()
        
        try:
            member = self.create_member_uc.execute(name, email)
            print(f"✅ Membre '{name}' enregistré avec succès ! (ID: {member.id})")
        except ValueError as e:
            print(f"❌ Erreur : {e}")
    
    def borrow_book(self):
        """Traite l'emprunt d'un livre."""
        book_id = input("ID du livre : ").strip()
        member_id = input("ID du membre : ").strip()
        
        try:
            loan = self.borrow_book_uc.execute(book_id, member_id)
            book = self.list_books_uc.execute_all()  # Pour récupérer le titre
            book_title = next((b.title for b in book if b.id == book_id), "livre")
            member = self.list_members_uc.execute()
            member_name = next((m.name for m in member if m.id == member_id), "membre")
            
            print(f"✅ Livre '{book_title}' emprunté par {member_name} !")
            print(f"   Date de retour prévue : {loan.due_date.strftime('%d/%m/%Y')}")
        except ValueError as e:
            print(f"❌ {e}")
    
    def return_book(self):
        """Traite le retour d'un livre."""
        book_id = input("ID du livre : ").strip()
        
        try:
            success, days_overdue = self.return_book_uc.execute(book_id)
            books = self.list_books_uc.execute_all()
            book_title = next((b.title for b in books if b.id == book_id), "livre")
            
            if days_overdue > 0:
                print(f"⚠️  Le livre '{book_title}' avait {days_overdue} jour(s) de retard !")
            
            print(f"✅ Livre '{book_title}' retourné avec succès !")
        except ValueError as e:
            print(f"❌ {e}")
    
    def list_all_books(self):
        """Affiche tous les livres."""
        books = self.list_books_uc.execute_all()
        
        if not books:
            print("Aucun livre dans la bibliothèque.")
            return
        
        print(f"\n{'='*70}")
        print(f"{'ID':<5} {'Titre':<30} {'Auteur':<22} {'Statut':<10}")
        print(f"{'='*70}")
        for book in books:
            status_fr = "disponible" if book.status == "available" else "emprunté"
            print(f"{book.id:<5} {book.title:<30} {book.author:<22} {status_fr:<10}")
        print(f"{'='*70}\n")
    
    def list_available_books(self):
        """Affiche les livres disponibles."""
        books = self.list_books_uc.execute_available()
        
        if not books:
            print("Aucun livre disponible.")
            return
        
        print(f"\n{'='*70}")
        print(f"{'ID':<5} {'Titre':<30} {'Auteur':<32}")
        print(f"{'='*70}")
        for book in books:
            print(f"{book.id:<5} {book.title:<30} {book.author:<32}")
        print(f"{'='*70}\n")
    
    def list_all_members(self):
        """Affiche tous les membres."""
        members = self.list_members_uc.execute()
        
        if not members:
            print("Aucun membre enregistré.")
            return
        
        print(f"\n{'='*70}")
        print(f"{'ID':<5} {'Nom':<25} {'Email':<37}")
        print(f"{'='*70}")
        for member in members:
            print(f"{member.id:<5} {member.name:<25} {member.email:<37}")
        print(f"{'='*70}\n")
    
    def run(self):
        """Lance la boucle principale du CLI."""
        while True:
            self.display_menu()
            choice = input("\nChoisissez une option : ").strip()
            
            if choice == "1":
                self.create_book()
            elif choice == "2":
                self.create_member()
            elif choice == "3":
                self.borrow_book()
            elif choice == "4":
                self.return_book()
            elif choice == "5":
                self.list_all_books()
            elif choice == "6":
                self.list_available_books()
            elif choice == "7":
                self.list_all_members()
            elif choice == "0":
                print("Au revoir !")
                break
            else:
                print("Option invalide. Veuillez réessayer.")
