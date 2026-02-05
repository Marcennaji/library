# 📚 Library Management System - Exercice de Refactoring

> 🔧 **Du code problématique à l'architecture maintenable : exercice de refactoring progressif**

## 🎯 Objectif

Application CLI de gestion de bibliothèque (emprunts de livres) qui **fonctionne** mais présente des **problèmes architecturaux**.

**Mission** : Diagnostiquer les problèmes, comprendre leur impact sur la testabilité, et apprendre à refactoriser progressivement.

---

## 🚀 Démarrage rapide

```bash
# Cloner et installer
git clone https://github.com/Marcennaji/library.git
cd library
pip install -r requirements.txt

# Lancer l'application
python main.py

# Lancer les tests
pytest tests/test_library_service.py -v
```

**Fonctionnalités** : Créer livres/membres, emprunter/retourner des livres, consulter disponibilités.

---

## 🔍 Analyse des problèmes

### 📋 Documents d'analyse

- **[VIOLATION_SRP.md](VIOLATION_SRP.md)** : Analyse de `borrow_book()` - 9 responsabilités mélangées → impossible à tester unitairement

- **[GUIDE_REFACTORING.md](GUIDE_REFACTORING.md)** : Méthode de refactoring progressif (priorisation, petites étapes, tests continus)

### 🧪 Tests actuels

```bash
pytest tests/test_library_service.py -v
# → 4 tests d'intégration, 11 warnings, nécessitent tous SQLite + filesystem
```

**Questions** : Pourquoi tant de warnings ? Pourquoi impossible de tester sans DB ? Que se passe-t-il si on veut tester juste la logique métier ?

---

## 🌟 Exemple d'architecture améliorée

La branche `refactored-hexagonal` montre **UN exemple** d'amélioration (pas LA seule solution) :

```bash
git checkout refactored-hexagonal
pytest tests/ -v
# → 23 tests (21 unitaires + 2 intégration), pas de warnings
```

**Différences clés** :
- Domain pur (sans dépendances infrastructure)
- Injection de dépendances
- Tests rapides avec test doubles (InMemoryRepositories, FixedClock)
- Documentation : ANALYSE_REFACTORING.md, tests/COMPARAISON_TESTS.md

```bash
# Comparer les structures
git diff main refactored-hexagonal --stat
```

---

## 🎓 Utilisation pédagogique

### 📖 Documents à utiliser

**Pendant la séance (1h encadrée)** :
- Ce README pour comprendre le contexte
- [VIOLATION_SRP.md](VIOLATION_SRP.md) pour analyser le problème concret
- Branche `refactored-hexagonal` pour voir une solution possible

**Après la séance (travail autonome)** :
- [GUIDE_REFACTORING.md](GUIDE_REFACTORING.md) pour refactoriser progressivement (avec aide de l'IA)

### ⏱️ Déroulement de la séance (60 min)

**Phase 1 : Diagnostic** (25 min)
1. **Expérimentation** (10 min) : Tentez d'écrire un test unitaire pour `borrow_book()` → constatez la difficulité
2. **Analyse du code** (10 min) : Lire `services/library_service.py` et identifier les problèmes
3. **Lecture** (5 min) : [VIOLATION_SRP.md](VIOLATION_SRP.md) - les 9 responsabilités mélangées

**Phase 2 : Comparaison** (20 min)
4. **Explorer la solution** (15 min) : Basculer sur `refactored-hexagonal`, lancer les 23 tests, comprendre la structure
5. **Discussion** (5 min) : Qu'est-ce qui a changé ? Pourquoi 23 tests au lieu de 4 ?

**Phase 3 : Application** (15 min)
6. **Lien avec votre projet** (10 min) : Identifier des problèmes similaires dans votre code
7. **Plan d'action** (5 min) : Définir les premiers refactorings à faire

### 🏠 Travail en autonomie (après la séance)

Pour refactoriser progressivement ce projet (ou le vôtre) :
1. Suivez le [GUIDE_REFACTORING.md](GUIDE_REFACTORING.md) en commençant par la Phase 0
2. Utilisez l'IA pour vous aider (voir section dédiée dans le guide)
3. Avancez par petites étapes, testez en continu, commitez fréquemment
4. N'essayez pas de tout faire d'un coup : c'est un travail itératif

**Principes à retenir** :
- Testabilité = indicateur de qualité architecturale
- SRP = une responsabilité par classe
- Refactoring progressif = petits pas + tests
- Architecture hexagonale = domaine isolé
- L'IA peut aider mais doit être utilisée intelligemment

---

## 📊 En chiffres

| Métrique | main | refactored |
|----------|------|------------|
| Fichiers Python | 14 | 30+ |
| Tests | 4 (intégration) | 23 (21 unit + 2 integ) |
| `borrow_book()` | 9 responsabilités | Use case avec 1 responsabilité |
| Testable sans DB ? | ❌ | ✅ |

---
