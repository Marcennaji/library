"""
COMPARAISON : Tests difficiles vs Tests faciles

Ce document compare l'effort de test entre les deux architectures.

═══════════════════════════════════════════════════════════════════

📊 STATISTIQUES

Branche main (code problématique) :
- 5 tests d'intégration forcés
- Tous nécessitent une DB SQLite réelle
- Lents (~500ms avec I/O disque)
- Fragiles (dépendent de l'état de la DB)
- Difficiles à maintenir

Branche refactored-hexagonal (architecture propre) :
- 21 tests unitaires + 2 tests d'intégration
- Tests unitaires sans DB (in-memory)
- Rapides (~2s pour les 23 tests)
- Robustes (test doubles)
- Faciles à maintenir

═══════════════════════════════════════════════════════════════════

🔴 PROBLÈMES DES TESTS SUR LE CODE MAIN

1. COUPLAGE À LA BASE DE DONNÉES
   - Impossible de tester sans SQLite
   - Setup/teardown complexe (fixture test_db)
   - Effets de bord entre tests
   - Lenteur (I/O disque)

2. DATES SYSTÈME NON CONTRÔLABLES
   - datetime.now() partout dans le code
   - Impossible de tester des scénarios temporels précis
   - Tests non déterministes

3. IDS GÉNÉRÉS ALÉATOIREMENT
   - UUIDs imprévisibles
   - Parsing du print() pour récupérer les IDs (horrible !)
   - Tests dépendant de l'ordre d'exécution

4. PRINT() AU LIEU DE RETURN
   - Nécessite capsys.readouterr() pour vérifier
   - Impossible de tester la logique sans I/O
   - Couplage à l'implémentation CLI

5. TESTS D'INTÉGRATION FORCÉS
   - Impossible d'isoler un use case
   - Setup massif pour chaque test
   - Pas de tests unitaires possibles

═══════════════════════════════════════════════════════════════════

🟢 AVANTAGES DES TESTS SUR REFACTORED-HEXAGONAL

1. INJECTION DE DÉPENDANCES
   ✅ BookRepository → InMemoryBookRepository
   ✅ Clock → FixedClock(datetime(2024, 1, 15))
   ✅ IDGenerator → FixedIDGenerator()

2. TESTS UNITAIRES PURS
   ✅ Test de Book entity isolé
   ✅ Test de BorrowBookUseCase avec mocks
   ✅ Pas de DB, pas d'I/O

3. DÉTERMINISME COMPLET
   ✅ Dates fixes pour tester les retards
   ✅ IDs prédictibles (TEST-B1, TEST-M1)
   ✅ Résultats constants

4. RAPIDITÉ
   ✅ 21 tests unitaires en <1s
   ✅ Pas d'I/O disque
   ✅ Tout en mémoire

5. TESTABILITÉ = MAINTENABILITÉ
   ✅ Facile d'ajouter un test
   ✅ Tests documentent le comportement
   ✅ Refactoring sécurisé

═══════════════════════════════════════════════════════════════════

💡 LEÇON PRINCIPALE

"L'architecture hexagonale ne rend pas seulement le code 
mieux organisé, elle le rend TESTABLE."

Sans testabilité → pas de tests → pas de confiance → code figé

Avec testabilité → tests rapides → refactoring sûr → évolution
"""
