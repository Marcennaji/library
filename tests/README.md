# Tests

Ce dossier contient les tests de l'application refactorée en architecture hexagonale.

## Structure

```
tests/
├── fixtures/                    # Doubles de test (mocks, in-memory repos)
│   ├── fixed_clock.py          # Clock avec date/heure fixe
│   ├── fixed_id_generator.py   # Générateur d'IDs prévisibles
│   ├── in_memory_book_repository.py
│   ├── in_memory_member_repository.py
│   └── in_memory_loan_repository.py
├── unit/                        # Tests unitaires (sans dépendances externes)
│   ├── test_book.py            # Tests de l'entité Book
│   ├── test_member.py          # Tests de l'entité Member
│   ├── test_loan.py            # Tests de l'entité Loan
│   ├── test_create_book_usecase.py
│   └── test_borrow_book_usecase.py
└── integration/                 # Tests d'intégration (avec SQLite)
    └── test_integration.py     # Workflow complet
```

## Lancer les tests

### Tous les tests
```bash
pytest tests/
```

### Tests unitaires seulement
```bash
pytest tests/unit/
```

### Tests d'intégration seulement
```bash
pytest tests/integration/
```

### Avec couverture
```bash
pytest --cov=src tests/
```

## Philosophie des tests

### Tests unitaires
- **Entités du domaine** : Testées sans aucune dépendance externe
- **Use cases** : Testés avec des doubles (in-memory repositories, fixed clock)
- **Rapides** : Exécution en millisecondes
- **Déterministes** : Résultats toujours identiques

### Tests d'intégration
- Testent le système complet avec SQLite réel
- Vérifient que les adapters fonctionnent correctement
- Base de données de test créée/supprimée pour chaque test

## Avantages de l'architecture hexagonale pour les tests

1. **Domaine testable sans infrastructure** : Les entités Book, Member, Loan n'ont aucune dépendance
2. **Use cases testables avec mocks** : Injection de dépendances permet de remplacer SQLite par InMemory
3. **Clock injectable** : Tests avec dates/heures fixées (pas de `datetime.now()` dans le code métier)
4. **ID Generator injectable** : Tests avec IDs prévisibles (TEST-B1, TEST-M1...)

## Comparer avec la version problématique

Dans la branche `main` (structure problématique), les tests sont **impossibles** :
- `Book.save()` appelle SQLite directement → Impossible de tester sans DB
- `datetime.now()` partout → Tests non-déterministes
- `uuid.uuid4()` → IDs imprévisibles dans les assertions
- Service god class → Impossible d'isoler la logique métier

**Architecture hexagonale = testabilité++**
