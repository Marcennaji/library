"""Tests unitaires de l'entité Loan."""

from datetime import datetime, timedelta
from domain.loan import Loan


def test_loan_creation():
    """Test : création d'un emprunt."""
    borrowed_at = datetime(2025, 1, 1)
    due_date = datetime(2025, 1, 15)
    
    loan = Loan(
        id="L1",
        book_id="B1",
        member_id="M1",
        borrowed_at=borrowed_at,
        due_date=due_date
    )
    
    assert loan.id == "L1"
    assert loan.book_id == "B1"
    assert loan.member_id == "M1"
    assert loan.borrowed_at == borrowed_at
    assert loan.due_date == due_date
    assert loan.returned_at is None


def test_loan_is_not_overdue():
    """Test : emprunt pas en retard."""
    borrowed_at = datetime(2025, 1, 1)
    due_date = datetime(2025, 1, 15)
    current_time = datetime(2025, 1, 10)  # Avant la date limite
    
    loan = Loan("L1", "B1", "M1", borrowed_at, due_date)
    
    assert loan.is_overdue(current_time) is False


def test_loan_is_overdue():
    """Test : emprunt en retard."""
    borrowed_at = datetime(2025, 1, 1)
    due_date = datetime(2025, 1, 15)
    current_time = datetime(2025, 1, 20)  # Après la date limite
    
    loan = Loan("L1", "B1", "M1", borrowed_at, due_date)
    
    assert loan.is_overdue(current_time) is True


def test_loan_not_overdue_when_returned():
    """Test : emprunt retourné n'est jamais en retard."""
    borrowed_at = datetime(2025, 1, 1)
    due_date = datetime(2025, 1, 15)
    returned_at = datetime(2025, 1, 20)  # Retourné en retard
    current_time = datetime(2025, 1, 25)
    
    loan = Loan("L1", "B1", "M1", borrowed_at, due_date, returned_at)
    
    assert loan.is_overdue(current_time) is False


def test_loan_mark_as_returned():
    """Test : marquer un emprunt comme retourné."""
    return_time = datetime(2025, 1, 10)
    
    loan = Loan("L1", "B1", "M1", datetime(2025, 1, 1), datetime(2025, 1, 15))
    loan.mark_as_returned(return_time)
    
    assert loan.returned_at == return_time
