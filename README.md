# Library Management System - Exercice de Diagnostic Architectural

> **Un code qui fonctionne… mais qui cache de vrais problèmes : sauras-tu les identifier ?**

## Objectif

Application CLI de gestion de bibliothèque (emprunts de livres) qui **fonctionne** mais présente des **problèmes architecturaux majeurs**.

**Mission** : Diagnostiquer ces problèmes, comprendre leur impact concret sur la testabilité, et découvrir à quoi ressemble une architecture mieux structurée.

---

## Démarrage rapide

```bash
# Cloner et installer
git clone https://github.com/Marcennaji/library.git
cd library
pip install -r requirements.txt

# Lancer les tests
python -m pytest tests/ -v

# Lancer l'application
python main.py

```

**Fonctionnalités** : Créer livres/membres, emprunter/retourner des livres, consulter disponibilités.

---

## Aperçu du code

```bash
python -m pytest tests/ -v
# → 4 tests d'intégration, nécessitent tous SQLite + filesystem
```

---

## Exemple d'architecture améliorée

La branche `refactored-hexagonal` montre **UN exemple** d'amélioration (pas LA seule solution) :

```bash
git checkout refactored-hexagonal
python -m pytest tests/ -v
# → 23 tests (21 unitaires + 2 intégration) en <2s
```

**Différences clés** :
- Domain pur (sans dépendances infrastructure)
- Injection de dépendances
- Tests rapides avec test doubles (InMemoryRepositories, FixedClock)
- Interface remplaçable : le CLI est un simple adaptateur — on pourrait brancher une API REST ou une UI web sans toucher au domaine
- Documentation : ANALYSE_REFACTORING.md, tests/README.md

**Structure refactorisée** : `src/domain/`, `src/ports/`, `src/application/usecases/`, `src/adapters/`

---

## Démarche à suivre

### Pendant la séance (1h)

**Phase 1 : Diagnostic** (30 min)
1. **Expérimentation** (10 min) : Tentez d'écrire un test unitaire pour `borrow_book()` — sans DB réelle, sans filesystem, sans `datetime.now()`. Notez ce qui bloque.
2. **Analyse du code** (10 min) : Lisez `services/library_service.py`. Listez toutes les responsabilités que vous identifiez dans `borrow_book()`.
3. **Mise en commun + approfondissement** (10 min) : Consultez [VIOLATION_SRP.md](VIOLATION_SRP.md) — comparez avec ce que vous avez trouvé.

**Phase 2 : Comparaison** (30 min)

1. **Explorer la solution** (15 min) : Basculez sur `refactored-hexagonal`, lancez les 23 tests, explorez la structure (`src/domain/`, `src/ports/`, `src/adapters/`).
2. **Comprendre les différences clés** (10 min) : Comparez `borrow_book()` (main) avec `BorrowBookUseCase` (refactored). Pourquoi les tests unitaires deviennent-ils triviaux ?
3. **Réflexion individuelle** (5 min) : Pourquoi avez-vous été guidés vers une architecture hexagonale dès le début sur votre projet ticketing ? Que se serait-il passé si vous aviez commencé comme ce code ? Et si demain le client voulait une interface web plutôt que CLI — dans quelle version serait-ce plus simple ?

### Pour aller plus loin (travail en autonomie)

Pour refactoriser progressivement ce projet (ou un autre) :

1. **Suivez le guide méthodologique** : [GUIDE_REFACTORING.md](GUIDE_REFACTORING.md) présente une approche progressive en 3 phases (testable → séparé → inversé)
2. **Utilisez l'IA comme assistant** : Le guide contient des conseils et exemples de prompts pour utiliser efficacement l'IA
3. **Avancez par petits pas** : Testez en continu, commitez fréquemment
4. **Soyez patient** : C'est un travail itératif, n'essayez pas de tout faire d'un coup

### Principes clés à retenir

- **Testabilité = indicateur de qualité architecturale** : Un code difficile à tester est un code mal structuré
- **SRP** ([Single Responsibility Principle](../architecture-logicielle-BUT2-ressources/cm/annexe_04_principes_SOLID.md#-s---single-responsibility-principle-srp)) : Une responsabilité par classe/méthode
- **Refactoring progressif** : Petits pas + tests + commits fréquents
- **Architecture hexagonale** : Isoler le domaine métier des détails techniques
- **L'IA comme outil** : Puissant pour accélérer, mais nécessite compréhension et validation

---

## Documents de référence

> **Ne pas consulter avant d'avoir fait votre propre diagnostic** — ces documents contiennent l'analyse complète des problèmes et des pistes de solution.

- **[VIOLATION_SRP.md](VIOLATION_SRP.md)** : Analyse détaillée de `borrow_book()` — les 9 responsabilités mélangées et leur impact sur la testabilité. À consulter à l'**étape 3** de la Phase 1.

- **[GUIDE_REFACTORING.md](GUIDE_REFACTORING.md)** : Méthode de refactoring progressif en 3 phases (testable → séparé → inversé), avec conseils d'utilisation de l'IA. À consulter pour le **travail en autonomie**.

---
