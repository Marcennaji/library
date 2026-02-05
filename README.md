# 📚 Library Management System - Exercice d'analyse architecturale et de refactoring

> 🔧 **Exercice de refactoring : Du code problématique à l'architecture hexagonale**

## 🎯 Contexte

Ce projet est une application CLI de gestion de bibliothèque (emprunts de livres) qui **fonctionne** mais qui présente de nombreux **problèmes architecturaux**.

**Objectif pédagogique :** Diagnostiquer les problèmes, comprendre leurs impacts, et savoir comment refactoriser vers l'architecture hexagonale.

---

## 📖 Description fonctionnelle

L'application permet de :
- ✅ Enregistrer des livres dans la bibliothèque
- ✅ Inscrire des membres
- ✅ Emprunter un livre (si disponible)
- ✅ Retourner un livre emprunté
- ✅ Lister les livres disponibles

**Domaine métier :**
- **Book** : Livre avec titre, auteur, ISBN, statut (AVAILABLE/BORROWED)
- **Member** : Membre de la bibliothèque avec nom et email
- **Loan** : Emprunt d'un livre par un membre (dates d'emprunt et de retour)

---

## 🏗️ Architecture actuelle (branche main)

```
models/              
├── book.py
├── member.py
└── loan.py
services/            
├── library_service.py
└── validation.py
database/            
├── db_connection.py
└── init_db.py
utils/               
├── date_utils.py
└── id_generator.py
main.py              
```
---

## 🚀 Installation

```bash
# Cloner le repo
git clone https://github.com/Marcennaji/library.git
cd library

# Installer les dépendances
pip install -r requirements.txt

# Vous êtes sur la branche 'main' (code problématique)
```

## 🧪 Lancer l'application (branche main)

```bash
python main.py
```

Vous verrez un menu CLI pour gérer la bibliothèque. Testez les fonctionnalités :
- Créer des livres 
- Créer des membres 
- Emprunter/retourner des livres

**Note :** L'application fonctionne, mais analysez le code pour identifier les problèmes !

### 🧪 Tests sur le code problématique

Le code problématique a quelques tests. Lancez-les :

```bash
pytest tests/test_library_service.py -v
```

**❓ Questions pour réflexion :**
- Que pensez-vous de ces tests ?
- Sont-ils faciles à écrire et à maintenir ?
- Pourquoi y a-t-il autant de warnings ?
- Pourquoi tous les tests nécessitent-ils une base de données réelle ?

**⚠️ Ce que cette architecture rend difficile/impossible à tester :**
- ❌ **Tests unitaires** : Impossible d'isoler la logique métier de la DB
- ❌ **Dates contrôlables** : `datetime.now()` partout → scénarios temporels impossibles
- ❌ **Tests rapides** : Tous les tests font de l'I/O disque (lent)
- ❌ **Tests parallèles** : Tous modifient la même DB `library.db`
- ❌ **Scénarios complexes** : Difficile de tester les cas limites

---

## 🌟 Solution refactorisée (branche refactored-hexagonal)

Pour voir la version refactorisée en architecture hexagonale :

```bash
git checkout refactored-hexagonal
```

Cette branche contient :
- ✅ **Architecture hexagonale complète** (domain/ports/application/adapters)
- ✅ **Domain pur** (aucune dépendance externe)
- ✅ **Injection de dépendances** (composition root dans main.py)
- ✅ **23 tests qui passent** (21 unitaires + 2 intégration)
- ✅ **Testabilité démontrée** avec test doubles (InMemoryRepositories, FixedClock, FixedIDGenerator)
- ✅ **Documentation détaillée** (ANALYSE_REFACTORING.md + tests/COMPARAISON_TESTS.md)

**Lancer les tests :**
```bash
pytest tests/ -v
```

**Comparer avec les tests de la branche main :**
```bash
# Sur main : 4 tests lents avec DB
git checkout main
pytest tests/test_library_service.py -v

# Sur refactored : 23 tests rapides, 21 sans DB
git checkout refactored-hexagonal
pytest tests/ -v
```

**Utilisez-la pour comprendre le chemin de transformation !**

---

L'objectif est d'identifier les problèmes en appliquant les **principes architecturaux** :
- ✅ Le domaine est-il pur (sans dépendances externes) ?
- ✅ Les responsabilités sont-elles bien séparées ?
- ✅ Le code est-il testable ?
- ✅ Les dépendances sont-elles injectées ?

Les mêmes principes s'appliquent à TOUS les domaines métier (bibliothèque, ticketing, e-commerce, etc.).

---
