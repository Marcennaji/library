"""Use case : Retourner un livre."""

from ports.book_repository import BookRepository
from ports.loan_repository import LoanRepository
from ports.clock import Clock


class ReturnBookUseCase:
    """Cas d'usage pour retourner un livre."""
    
    def __init__(self, book_repository: BookRepository, loan_repository: LoanRepository, clock: Clock):
        self.book_repository = book_repository
        self.loan_repository = loan_repository
        self.clock = clock
    
    def execute(self, book_id: str) -> tuple[bool, int]:
        """
        Exécute le retour d'un livre.
        Retourne (succès, jours_de_retard).
        """
        # Récupération du livre
        book = self.book_repository.get_by_id(book_id)
        if not book:
            raise ValueError("Livre non trouvé")
        
        # Récupération de l'emprunt actif
        loan = self.loan_repository.find_active_loan(book_id)
        if not loan:
            raise ValueError(f"Aucun emprunt actif trouvé pour '{book.title}'")
        
        # Retour du livre (logique métier)
        return_time = self.clock.now()
        book.mark_as_returned()
        self.book_repository.save(book)
        
        loan.mark_as_returned(return_time)
        self.loan_repository.save(loan)
        
        # Calcul du retard éventuel
        days_overdue = 0
        if loan.is_overdue(return_time):
            days_overdue = (return_time - loan.due_date).days
        
        return True, days_overdue
