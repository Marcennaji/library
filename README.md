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

# Lancer les tests
python -m pytest tests/ -v

# Lancer l'application
python main.py

```

**Fonctionnalités** : Créer livres/membres, emprunter/retourner des livres, consulter disponibilités.

---

## 🔍 Analyse des problèmes

### 📋 Documents d'analyse

- **[VIOLATION_SRP.md](VIOLATION_SRP.md)** : Analyse d'un des problèmes majeurs - la méthode `borrow_book()` contient 9 responsabilités mélangées → impossible à tester unitairement

- **[GUIDE_REFACTORING.md](GUIDE_REFACTORING.md)** : Méthode de refactoring progressif pour corriger ces problèmes (priorisation, petites étapes, tests continus)

### 🧪 Tests actuels

```bash
python -m pytest tests/ -v
# → 4 tests d'intégration, nécessitent tous SQLite + filesystem
```

<details>
<summary><b>❓ Pourquoi seulement 4 tests ?</b></summary>

Avec cette architecture, il est très difficile d'écrire plus de tests. Chaque test nécessite :
- Une vraie base de données SQLite
- Le système de fichiers (pour les logs/)
- La gestion des dates système
- La capture de `print()` avec `capsys`

**Conséquence** : Les tests sont lents (~500ms pour 4 tests), complexes à écrire, et testent tout en même temps (logique métier + infrastructure).

**Comparaison** : La branche `refactored-hexagonal` contient 23 tests dont 21 unitaires qui s'exécutent en <2s au total.
</details>

<details>
<summary><b>❓ Pourquoi impossible de tester sans DB ?</b></summary>

Les entités (`Book`, `Member`, `Loan`) contiennent des méthodes `.save()` qui font des requêtes SQL directes. Le service `LibraryService` utilise `get_connection()` qui retourne toujours une connexion vers `library.db`.

**Conséquence** : Impossible de tester la logique métier isolément - chaque test doit créer/nettoyer une vraie base de données.

**Solution** : Séparer les entités (domaine pur) des repositories (persistance), puis injecter les repositories.
</details>

<details>
<summary><b>❓ Que se passe-t-il si on veut tester juste la logique métier ?</b></summary>

C'est impossible actuellement. La logique métier est mélangée avec :
- Base de données (SQL)
- Système de fichiers (logs/)
- Date système (`datetime.now()`)
- Affichage console (`print()`)

Pour tester un comportement métier simple (ex: "un livre emprunté n'est plus disponible"), il faut gérer toutes ces dépendances.

**Résultat** : Tests lents, fragiles (dépendent de l'état du filesystem/DB), difficiles à maintenir.
</details>

---

## 🌟 Exemple d'architecture améliorée

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
- Documentation : ANALYSE_REFACTORING.md, tests/README.md

**Structure refactorisée** : `src/domain/`, `src/ports/`, `src/application/usecases/`, `src/adapters/`

---

## � Démarche proposée

### ⏱️ Pendant la séance (50 min)

**Phase 1 : Diagnostic** (30 min)
1. **Expérimentation** (15 min) : Tentez d'écrire un test unitaire pour `borrow_book()` → constatez la difficulté
2. **Analyse du code** (10 min) : Lisez `services/library_service.py` et identifiez les problèmes
3. **Approfondissement** (5 min) : Consultez [VIOLATION_SRP.md](VIOLATION_SRP.md) pour l'analyse détaillée des 9 responsabilités mélangées

**Phase 2 : Comparaison** (20 min)
4. **Explorer une solution possible** (20 min) : Basculez sur `refactored-hexagonal`, lancez les 23 tests, comprenez la structure (domain/, ports/, adapters/), comparez avec main

**💭 Réflexion individuelle** : Pourquoi avez-vous été guidés vers une architecture hexagonale dès le début sur votre projet ticketing ? Que se serait-il passé si vous aviez commencé comme ce code ?

### 🏠 Pour aller plus loin (travail en autonomie)

Pour refactoriser progressivement ce projet (ou le vôtre) :

1. **Suivez le guide méthodologique** : [GUIDE_REFACTORING.md](GUIDE_REFACTORING.md) présente une approche progressive en 3 phases (testable → séparé → inversé)
2. **Utilisez l'IA comme assistant** : Le guide contient des conseils et exemples de prompts pour utiliser efficacement l'IA
3. **Avancez par petits pas** : Testez en continu, commitez fréquemment
4. **Soyez patient** : C'est un travail itératif, n'essayez pas de tout faire d'un coup

### 💡 Principes clés à retenir

- **Testabilité = indicateur de qualité architecturale** : Un code difficile à tester est un code mal structuré
- **SRP** ([Single Responsibility Principle](../architecture-logicielle-BUT2-ressources/cm/annexe_04_principes_SOLID.md#-s---single-responsibility-principle-srp)) : Une responsabilité par classe/méthode
- **Refactoring progressif** : Petits pas + tests + commits fréquents
- **Architecture hexagonale** : Isoler le domaine métier des détails techniques
- **L'IA comme outil** : Puissant pour accélérer, mais nécessite compréhension et validation

---
