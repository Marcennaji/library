"""Use case : Emprunter un livre."""

from datetime import timedelta
from domain.loan import Loan
from ports.book_repository import BookRepository
from ports.member_repository import MemberRepository
from ports.loan_repository import LoanRepository
from ports.id_generator import IDGenerator
from ports.clock import Clock


class BorrowBookUseCase:
    """Cas d'usage pour emprunter un livre."""
    
    def __init__(self, book_repository: BookRepository, member_repository: MemberRepository,
                 loan_repository: LoanRepository, id_generator: IDGenerator, clock: Clock):
        self.book_repository = book_repository
        self.member_repository = member_repository
        self.loan_repository = loan_repository
        self.id_generator = id_generator
        self.clock = clock
    
    def execute(self, book_id: str, member_id: str) -> Loan:
        """Exécute l'emprunt d'un livre."""
        # Récupération des entités
        book = self.book_repository.get_by_id(book_id)
        if not book:
            raise ValueError("Livre non trouvé")
        
        member = self.member_repository.get_by_id(member_id)
        if not member:
            raise ValueError("Membre non trouvé")
        
        # Vérification business
        if not book.is_available():
            raise ValueError(f"Le livre '{book.title}' n'est pas disponible")
        
        # Modification du livre (logique métier)
        book.mark_as_borrowed()
        self.book_repository.save(book)
        
        # Création de l'emprunt
        loan_id = self.id_generator.generate_loan_id()
        borrowed_at = self.clock.now()
        due_date = borrowed_at + timedelta(days=14)
        
        loan = Loan(
            id=loan_id,
            book_id=book.id,
            member_id=member.id,
            borrowed_at=borrowed_at,
            due_date=due_date
        )
        
        self.loan_repository.save(loan)
        return loan
