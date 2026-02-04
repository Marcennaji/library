# 📊 Analyse du Refactoring - Comparaison Architecture

Ce document compare la structure problématique (branche `main`) avec la structure refactorée en architecture hexagonale (branche `refactored-hexagonal`).

---

## 🎯 Objectif pédagogique

Comprendre **concrètement** comment transformer du code "apparemment structuré" mais architecturalement problématique vers une architecture hexagonale propre.

---

## 📂 Vue d'ensemble des structures

### ❌ Structure problématique (main)

```
library/
├── models/          # Entités + persistance mélangées
│   ├── book.py
│   ├── member.py
│   └── loan.py
├── services/        # Service "god class" faisant tout
│   ├── library_service.py
│   └── validation.py
├── database/        # Infrastructure exposée
│   ├── db_connection.py
│   └── init_db.py
├── utils/           # Fonctions système non abstraites
│   ├── date_utils.py
│   └── id_generator.py
└── main.py          # Instanciation directe, pas d'injection
```

### ✅ Structure hexagonale (refactored-hexagonal)

```
src/
├── domain/          # Entités pures (logique métier uniquement)
│   ├── book.py
│   ├── member.py
│   └── loan.py
├── ports/           # Interfaces (contrats)
│   ├── book_repository.py
│   ├── member_repository.py
│   ├── loan_repository.py
│   ├── clock.py
│   └── id_generator.py
├── application/     # Use cases (orchestration)
│   └── usecases/
│       ├── create_book.py
│       ├── create_member.py
│       ├── borrow_book.py
│       ├── return_book.py
│       ├── list_books.py
│       └── list_members.py
├── adapters/        # Implémentations concrètes
│   ├── db/
│   │   ├── book_repository_sqlite.py
│   │   ├── member_repository_sqlite.py
│   │   ├── loan_repository_sqlite.py
│   │   └── init_db.py
│   ├── cli/
│   │   └── cli_adapter.py
│   ├── system_clock.py
│   └── sequential_id_generator.py
└── main.py          # Composition root (injection de dépendances)
```

---

## 🔍 Analyse problème par problème

### Problème 1 : Entités avec persistance

#### ❌ Code problématique (models/book.py)

```python
from database.db_connection import get_connection  # Import infrastructure

class Book:
    def save(self):
        """Sauvegarde le livre en base de données."""
        conn = get_connection()  # Accès direct à SQLite
        cursor = conn.cursor()
        cursor.execute("""INSERT OR REPLACE INTO books ...""")
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_by_id(book_id):
        """Récupère un livre par ID."""
        conn = get_connection()  # Encore SQLite dans l'entité
        # ...
```

**Pourquoi c'est mal ?**
- ✗ L'entité `Book` dépend de SQLite (couplage fort)
- ✗ Impossible de tester sans base de données
- ✗ Impossible de changer de DB sans modifier l'entité
- ✗ Violation du principe de responsabilité unique

#### ✅ Solution hexagonale

**domain/book.py** (entité pure)
```python
class Book:
    """Entité du domaine - AUCUNE dépendance externe."""
    
    def __init__(self, id: str, title: str, author: str, ...):
        # Validation (invariants du domaine)
        if not title or len(title) < 2:
            raise ValueError("...")
        self.id = id
        self.title = title
        # ...
    
    def mark_as_borrowed(self):
        """Logique métier pure (pas de DB)."""
        if not self.is_available():
            raise ValueError("...")
        self.status = "borrowed"
```

**ports/book_repository.py** (interface)
```python
from abc import ABC, abstractmethod

class BookRepository(ABC):
    @abstractmethod
    def save(self, book: Book) -> None:
        pass
    
    @abstractmethod
    def get_by_id(self, book_id: str) -> Book | None:
        pass
```

**adapters/db/book_repository_sqlite.py** (implémentation)
```python
class SQLiteBookRepository(BookRepository):
    def save(self, book: Book) -> None:
        conn = self._get_connection()
        # ... SQL ici, dans l'adaptateur
```

**Bénéfices :**
- ✓ `Book` ne dépend de rien (testable facilement)
- ✓ Changement de DB = nouveau repository (MongoDB, PostgreSQL...)
- ✓ Tests avec `InMemoryBookRepository` sans DB réelle

---

### Problème 2 : Service "god class"

#### ❌ Code problématique (services/library_service.py)

```python
from models.book import Book  # Dépend des modèles qui font du SQL
from models.member import Member
import uuid

class LibraryService:
    def create_book(self, title, author, isbn):
        book = Book(id=str(uuid.uuid4()), ...)  # Génération ID ici
        book.save()  # Appel à la méthode du modèle
        print(f"✅ Livre créé !")  # Affichage CLI dans le service
        return book
    
    def borrow_book(self, book_id, member_id):
        book = Book.get_by_id(book_id)  # Appel statique au modèle
        member = Member.get_by_id(member_id)
        # Logique métier + orchestration + affichage mélangés
        book.mark_as_borrowed()
        book.save()
        loan = Loan(id=str(uuid.uuid4()), ...)
        loan.save()
        print(f"✅ Emprunté !")  # CLI dans le service
        return loan
```

**Pourquoi c'est mal ?**
- ✗ Le service fait TOUT (orchestration + logique + affichage)
- ✗ Dépend des modèles qui dépendent de SQLite
- ✗ Génération d'UUID dans le service (pas abstrait)
- ✗ `print()` dans le service (couplage au CLI)
- ✗ Impossible de tester sans DB et sans CLI

#### ✅ Solution hexagonale

**application/usecases/borrow_book.py** (use case)
```python
class BorrowBookUseCase:
    def __init__(self, book_repository: BookRepository, 
                 member_repository: MemberRepository,
                 loan_repository: LoanRepository,
                 id_generator: IDGenerator,
                 clock: Clock):
        # Injection de dépendances (interfaces seulement)
        self.book_repository = book_repository
        self.member_repository = member_repository
        self.loan_repository = loan_repository
        self.id_generator = id_generator
        self.clock = clock
    
    def execute(self, book_id: str, member_id: str) -> Loan:
        # Orchestration pure (pas de print, pas de SQL)
        book = self.book_repository.get_by_id(book_id)
        if not book:
            raise ValueError("Livre non trouvé")
        
        member = self.member_repository.get_by_id(member_id)
        if not member:
            raise ValueError("Membre non trouvé")
        
        if not book.is_available():
            raise ValueError(f"Le livre '{book.title}' n'est pas disponible")
        
        # Logique métier dans l'entité
        book.mark_as_borrowed()
        self.book_repository.save(book)
        
        # Création de l'emprunt
        loan_id = self.id_generator.generate_loan_id()
        borrowed_at = self.clock.now()
        due_date = borrowed_at + timedelta(days=14)
        
        loan = Loan(loan_id, book.id, member.id, borrowed_at, due_date)
        self.loan_repository.save(loan)
        
        return loan
```

**adapters/cli/cli_adapter.py** (affichage séparé)
```python
class CLIAdapter:
    def __init__(self, ..., borrow_book_uc: BorrowBookUseCase):
        self.borrow_book_uc = borrow_book_uc
    
    def borrow_book(self):
        book_id = input("ID du livre : ").strip()
        member_id = input("ID du membre : ").strip()
        
        try:
            loan = self.borrow_book_uc.execute(book_id, member_id)
            print(f"✅ Livre emprunté !")  # Affichage dans le CLI
        except ValueError as e:
            print(f"❌ {e}")
```

**Bénéfices :**
- ✓ Use case testable avec des mocks (pas de DB, pas de CLI)
- ✓ Logique métier isolée dans le domaine
- ✓ Affichage CLI séparé (peut être remplacé par API REST)
- ✓ Injection de dépendances (testabilité ++, flexibilité ++)

---

### Problème 3 : Dépendances non abstraites (datetime, uuid)

#### ❌ Code problématique

```python
from datetime import datetime
import uuid

class Book:
    def __init__(self, ...):
        self.registered_at = datetime.now()  # Couplage au temps système
        
class LibraryService:
    def create_book(self, ...):
        book = Book(id=str(uuid.uuid4()), ...)  # UUID non abstrait
```

**Pourquoi c'est mal ?**
- ✗ Tests impossibles avec une date fixe
- ✗ `datetime.now()` rend les tests non-déterministes
- ✗ Impossible de tester le comportement avec une date spécifique

#### ✅ Solution hexagonale

**ports/clock.py** (interface)
```python
from abc import ABC, abstractmethod
from datetime import datetime

class Clock(ABC):
    @abstractmethod
    def now(self) -> datetime:
        pass
```

**adapters/system_clock.py** (implémentation système)
```python
class SystemClock(Clock):
    def now(self) -> datetime:
        return datetime.now()
```

**tests/fixed_clock.py** (implémentation test)
```python
class FixedClock(Clock):
    def __init__(self, fixed_time: datetime):
        self.fixed_time = fixed_time
    
    def now(self) -> datetime:
        return self.fixed_time
```

**Usage dans le use case :**
```python
class CreateBookUseCase:
    def __init__(self, ..., clock: Clock):
        self.clock = clock  # Interface injectée
    
    def execute(self, ...):
        registered_at = self.clock.now()  # Abstrait !
        book = Book(..., registered_at=registered_at)
```

**Bénéfices :**
- ✓ Tests déterministes avec `FixedClock`
- ✓ Peut simuler n'importe quelle date/heure
- ✓ Respect du principe d'inversion de dépendances

---

### Problème 4 : Pas de composition root

#### ❌ Code problématique (main.py)

```python
from services.library_service import LibraryService
from database.init_db import init_database

def main():
    init_database()
    service = LibraryService()  # Instanciation directe
    
    while True:
        choice = input("...")
        if choice == "1":
            title = input("...")
            service.create_book(title, ...)  # Service instancié directement
```

**Pourquoi c'est mal ?**
- ✗ Pas d'injection de dépendances
- ✗ Couplage fort entre main et service
- ✗ Impossible de changer d'implémentation

#### ✅ Solution hexagonale (main.py)

```python
def main():
    """Composition root - configure et démarre l'application."""
    
    # 1. Initialiser la base de données
    init_database()
    
    # 2. Instancier les adapters (implémentations des ports)
    book_repo = SQLiteBookRepository()
    member_repo = SQLiteMemberRepository()
    loan_repo = SQLiteLoanRepository()
    clock = SystemClock()
    id_generator = SequentialIDGenerator(book_repo, member_repo, loan_repo)
    
    # 3. Instancier les use cases avec injection de dépendances
    create_book_uc = CreateBookUseCase(book_repo, id_generator, clock)
    borrow_book_uc = BorrowBookUseCase(book_repo, member_repo, loan_repo, 
                                        id_generator, clock)
    # ...
    
    # 4. Instancier l'adaptateur CLI
    cli = CLIAdapter(create_book_uc, borrow_book_uc, ...)
    
    # 5. Lancer l'application
    cli.run()
```

**Bénéfices :**
- ✓ Toutes les dépendances créées et injectées au démarrage
- ✓ Changement d'implémentation = modifier main.py uniquement
- ✓ Pour passer en REST API : remplacer `CLIAdapter` par `FastAPIAdapter`
- ✓ Point central de configuration

---

## 📊 Tableau récapitulatif des transformations

| Concept | ❌ Structure problématique | ✅ Structure hexagonale |
|---------|---------------------------|------------------------|
| **Entités** | Contiennent save(), get_by_id() avec SQL | Pures, uniquement logique métier |
| **Persistance** | Dans les entités (models/) | Repositories (adapters/db/) |
| **Interfaces** | Aucune abstraction | Ports/ avec interfaces ABC |
| **Use cases** | Service god class faisant tout | Use cases séparés et ciblés |
| **Temps système** | datetime.now() partout | Clock (port) injecté |
| **IDs** | uuid.uuid4() dans le code | IDGenerator (port) injecté |
| **CLI** | print() dans les services | CLIAdapter séparé |
| **Injection** | Instanciations directes | Composition root (main.py) |
| **Tests** | Impossibles sans DB réelle | Faciles avec mocks |
| **Changement de DB** | Modifier toutes les entités | Nouveau repository |
| **Changement de CLI→API** | Réécriture complète | Nouveau adaptateur |

---

## 🎓 Points clés pour les étudiants

### Ce qui SEMBLE bien mais NE L'EST PAS :
1. ✗ **Séparer en dossiers** (models/, services/, database/) ≠ bonne architecture
2. ✗ **Avoir un "service"** qui centralise tout ≠ découpage propre
3. ✗ **Mettre save() dans Book** car "c'est le livre qui se sauvegarde" = mauvaise analogie

### Ce qui EST vraiment bien :
1. ✓ **Domaine pur** : entités sans dépendances externes
2. ✓ **Ports (interfaces)** : contrats entre couches
3. ✓ **Use cases** : un cas d'usage = une classe
4. ✓ **Adapters** : implémentations concrètes remplaçables
5. ✓ **Composition root** : injection de toutes les dépendances
6. ✓ **Inversion de dépendances** : le domaine ne dépend de RIEN

---

## 🧪 Avantages testabilité

### Tests impossibles dans la version problématique :
```python
# Comment tester create_book() sans :
# - Créer une vraie base SQLite ?
# - Voir les print() s'afficher ?
# - Avoir une date/heure fixe ?
service = LibraryService()
book = service.create_book("Title", "Author", None)  # 😱 Crée vraiment en DB
```

### Tests faciles dans la version hexagonale :
```python
# Test unitaire propre
book_repo_mock = Mock(spec=BookRepository)
id_gen_mock = Mock(spec=IDGenerator)
clock_mock = FixedClock(datetime(2025, 1, 1))

use_case = CreateBookUseCase(book_repo_mock, id_gen_mock, clock_mock)
book = use_case.execute("Title", "Author", None)

# Vérifications
assert book.title == "Title"
book_repo_mock.save.assert_called_once()
assert book.registered_at == datetime(2025, 1, 1)
```

---

## 🚀 Pour aller plus loin

### Questions de réflexion :
1. Pourquoi models/ + services/ + database/ n'est PAS une architecture hexagonale ?
2. Quel est le rôle du "composition root" ?
3. Pourquoi abstraire datetime.now() et uuid.uuid4() ?
4. Comment ajouter un adaptateur REST API sans toucher au domaine ?
5. Qu'est-ce que le principe d'inversion de dépendances ?

### Exercices pratiques :
1. Créer un `InMemoryBookRepository` pour les tests
2. Créer un `FastAPIAdapter` pour remplacer le CLI
3. Ajouter un use case `SearchBooksByAuthor`
4. Créer un `FixedIDGenerator` pour les tests (IDs prévisibles)

---

## 📚 Ressources

- **Architecture hexagonale** : Alistair Cockburn (2005)
- **Clean Architecture** : Robert C. Martin
- **Dependency Inversion Principle** : SOLID

---

*Document créé pour l'exercice pédagogique TD4b - Architecture Logicielle BUT2*
