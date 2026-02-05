# 🚨 Violation Massive du SRP (Single Responsibility Principle): La méthode `borrow_book()`

> 📚 Consultez l'[Annexe SOLID](../architecture-logicielle-BUT2-ressources/cm/annexe_04_principes_SOLID.md) pour comprendre en détail le principe SRP et les autres principes SOLID.

## Le problème

La méthode `borrow_book()` dans [services/library_service.py](services/library_service.py) viole **massivement** le SRP.

### ❌ Responsabilités mélangées (9 au total !)

```python
def borrow_book(self, book_id, member_id):
    # 1. Validation métier
    # 2. Mise à jour base de données (emprunt)
    # 3. Calcul de statistiques
    # 4. Requêtes analytics (emprunts du mois, total, livres similaires)
    # 5. Génération d'ID séquentiel
    # 6. Logging dans un fichier
    # 7. Génération de recommandations
    # 8. Simulation d'envoi d'email
    # 9. Affichage console
```

## 🔥 Pourquoi c'est catastrophique ?

### 1. **Impossible à tester unitairement**

Pour tester **uniquement** la logique métier (livre disponible → créer emprunt), vous êtes **forcé** de :
- ✗ Créer une vraie base de données SQLite
- ✗ Avoir un système de fichiers (logs/)
- ✗ Mocker print() pour capturer l'output
- ✗ Nettoyer les fichiers après chaque test
- ✗ Gérer les effets de bord (fichiers, DB modifiée)

**Résultat** : Test d'intégration lent et fragile au lieu de test unitaire rapide.

### 2. **Couplage fort**

La méthode dépend de :
- `Book`, `Member`, `Loan` (modèles avec accès DB)
- `database.db_connection` (infrastructure)
- Système de fichiers (`os`, `open()`)
- Console (`print()`)
- Datetime système (`datetime.now()`)

**Impossible de remplacer une dépendance sans tout casser.**

### 3. **Code non maintenable**

Si vous voulez :
- Changer le format du log → modifier `borrow_book()`
- Changer le système d'email → modifier `borrow_book()`
- Changer les statistiques → modifier `borrow_book()`
- Ajouter une notification → modifier `borrow_book()`

**Violation du Open/Closed Principle** : la méthode doit être modifiée pour chaque nouvelle fonctionnalité.

### 4. **Effets de bord cachés**

Appeler `borrow_book()` a des effets invisibles :
- Crée/modifie `logs/borrows.log`
- Crée/modifie `logs/emails_sent.log`
- Modifie la DB
- Affiche dans la console

**Impossible de prévoir ce qui va se passer sans lire tout le code.**

## 🎯 Testabilité : Comparaison

### Code actuel (branche main) - **Impossible**

```python
def test_borrow_book():
    # On doit tout mettre en place !
    setup_database()
    create_logs_directory()
    service = LibraryService()
    
    # Test mélange tout
    loan = service.borrow_book("B1", "M1")
    
    # Vérifications difficiles
    assert loan is not None
    assert os.path.exists("logs/borrows.log")  # Effet de bord
    assert os.path.exists("logs/emails_sent.log")  # Effet de bord
    # Impossible de tester JUSTE la logique métier
```

**Problèmes** :
- ❌ Pas un test unitaire (nécessite DB + filesystem)
- ❌ Lent (~500ms avec I/O)
- ❌ Fragile (dépend de l'état du filesystem)
- ❌ Teste TOUT en même temps (on ne sait pas ce qui casse)

### Architecture hexagonale (branche refactored-hexagonal) - **Facile**

```python
def test_borrow_book_use_case():
    # Arrange : Mocks purs (pas de DB, pas de fichiers)
    book_repo = InMemoryBookRepository()
    member_repo = InMemoryMemberRepository()
    loan_repo = InMemoryLoanRepository()
    clock = FixedClock(datetime(2024, 1, 15))
    id_gen = FixedIDGenerator()
    
    book_repo.save(Book("B1", "1984", "Orwell", available=True))
    member_repo.save(Member("M1", "Alice", "alice@test.com"))
    
    # Act : Test JUSTE la logique métier
    use_case = BorrowBookUseCase(book_repo, member_repo, loan_repo, clock, id_gen)
    loan = use_case.execute("B1", "M1")
    
    # Assert : Vérifications précises
    assert loan.book_id == "B1"
    assert loan.member_id == "M1"
    assert book_repo.get_by_id("B1").is_available() == False
```

**Avantages** :
- ✅ Test unitaire pur (100% en mémoire)
- ✅ Rapide (<1ms)
- ✅ Robuste (pas d'I/O, pas d'effets de bord)
- ✅ Teste UNE responsabilité : la logique métier

## 📚 Principe SRP appliqué

Dans l'architecture hexagonale, chaque classe a UNE responsabilité :

| Classe | Responsabilité unique |
|--------|----------------------|
| `BorrowBookUseCase` | Orchestrer l'emprunt (logique métier) |
| `BookRepository` | Gérer la persistance des livres |
| `LoanRepository` | Gérer la persistance des emprunts |
| `EmailService` | Envoyer des emails |
| `LoggingService` | Écrire dans les logs |
| `StatisticsService` | Calculer les statistiques |
| `Clock` | Fournir la date/heure |

**Résultat** : Chaque classe est **facilement testable** car elle n'a qu'une seule raison de changer.

## 🔍 Questions de réflexion

1. **Testabilité** : Comment tester que le calcul des statistiques est correct sans créer de DB ?
2. **Modification** : Si on veut changer le format de l'email, combien de classes faut-il modifier ?
3. **Réutilisation** : Peut-on réutiliser la logique de calcul de statistiques ailleurs ?
4. **Responsabilités** : Listez toutes les raisons pour lesquelles cette méthode pourrait changer.

## ✅ Conclusion

**Le SRP n'est pas qu'une question d'organisation du code, c'est une question de TESTABILITÉ.**

Une méthode avec 9 responsabilités = 9 dépendances = impossible à tester unitairement = code figé.

→ Comparez avec la branche `refactored-hexagonal` pour voir la différence !
