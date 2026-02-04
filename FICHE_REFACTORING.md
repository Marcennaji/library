# 🔧 Fiche de Refactoring - De la Boule de Boue à l'Hexagonale

**Exercice pratique (non noté)** - Consolidation des apprentissages

**Nom :** ______________________  
**Date :** ______________________  
**Binôme (optionnel) :** ______________________

---

## 🎯 Objectif

Vous avez un code qui **fonctionne** (`library.py`, ~300 lignes) mais qui est structuré comme un **"big ball of mud"**.

**Mission :** Diagnostiquer les problèmes et proposer un refactoring vers l'architecture hexagonale.

**⏱️ Temps total : 40-45 minutes**

---

## 📖 Contexte fonctionnel (2 min de lecture)

L'application CLI permet de :
- Créer des livres et enregistrer des membres
- Emprunter et retourner des livres
- Lister les livres disponibles

**Structure actuelle :**
```
library/
├── models/         # Book, Member, Loan (avec persistance incluse ❌)
├── services/       # LibraryService (fait tout ❌)
├── database/       # Connexion DB et init
├── utils/          # Date utils, ID generator
└── main.py         # CLI principal
```

**Prenez 2 minutes pour lancer l'application et la tester :**
```bash
python main.py
# Créez un livre, un membre, faites un emprunt
```

---

## Phase 1 : Diagnostic des problèmes (15 minutes)

### 1.1 Lecture du code (5 min)

Parcourez rapidement les fichiers (commencez par `models/book.py` et `services/library_service.py`).

**Ce que vous observez :**
- [ ] Code séparé en dossiers (models/, services/, database/, utils/)
- [ ] Les classes "modèles" contiennent save(), get_by_id() → mélange avec DB
- [ ] Le "service" fait de la logique + print() + appels DB
- [ ] datetime.now() et uuid.uuid4() partout (pas d'abstraction)
- [ ] Autre : _______________________________________________

**Question :** Est-ce que séparer en dossiers suffit pour avoir une bonne architecture ?

Réponse : _________________________________________________________________

---

### 1.2 Problèmes d'aFichier | Ligne(s) | Principe violé |
|------------------|---------|----------|----------------|
| Ex: `book.save()` dans Book | models/book.py | ~50 | Séparation des responsabilités |
| `Book.get_by_id()` méthode statique avec SQL | models/book.py | | |
| LibraryService contient print() | services/ | | |
| Import de database dans models | models/book.py | | |
| datetime.now() partout | Plusieurs | | |
| Service instancié directement dans main | main.py Ex: `book.save()` dans la classe Book | ~50 | Séparation des responsabilités |
| | | |
| | | |
| | | |
| | | |

---

### 1.3 Problèmes d'évolutivité (5 min)

Si on vous demande ces changements, qu'est-ce qui serait difficile ?

| Changement demandé | Difficulté<br>(1-5) | Fichiers/lignes à modifier | Pourquoi c'est difficile ? |
|-------------------|---------------------|----------------------------|---------------------------|
| Remplacer SQLite par PostgreSQL | | | |
| Ajouter une API REST à côté du CLI | | | |
| Tester `borrow_book()` sans DB | | | |
| Changer durée d'emprunt (21j au lieu de 14j) | | | |
| Envoyer un email quand livre emprunté | | | |

**Conclusion : Quel est le plus gros problème de ce code ?**

Réponse : _________________________________________________________________

_________________________________________________________________

---

## Phase 2 : Proposition de refactoring hexagonal (25 minutes)

### 2.1 Structure cible (10 min)

Proposez une structure hexagonale pour refactorer ce code :

```
src/
├── domain/
│   ├── _______________.py  (quelle(s) classe(s) ?)
│   ├── _______________.py
│   └── _______________.py
│
├── ports/
│   ├── _______________.py  (quelle(s) interface(s) ?)
│   └── _______________.py
│
├── application/
│   └── usecases/
│       ├── _______________.py  (quel(s) use case(s) ?)
│       ├── _______________.py
│       └── _______________.py
│
├── adapters/
│   ├── cli/
│   │   └── _______________.py  (quoi ?)
│   └── db/
│       └── _______________.py  (quoi ?)
│
└── main.py  (composition root)
```

---

### 2.2 Ports à créer (5 min)

Listez les **interfaces (ports)** nécessaires et leurs implémentations possibles :

| Port (interface) | Responsabilité | Implémentations possibles |
|------------------|----------------|--------------------------|
| Ex: `BookRepository` | Persistance des livres | `SQLiteBookRepository`, `InMemoryBookRepository` |
| | | |
| | | |
| | | |

**Question :** Pourquoi créer une interface `BookRepository` au lieu d'utiliser directement `SQLiteBookRepository` ?

Réponse : _________________________________________________________________

---

### 2.3 Use cases à identifier (5 min)

Dans le code actuel (`library.py`), quels **use cases** identifiez-vous ?

| Fonction actuelle | Use case proposé | Responsabilité |
|-------------------|------------------|----------------|
| Ex: `borrow_book()` | `BorrowBookUseCase` | Orchestrer l'emprunt (vérifications + état) |
| | | |
| | | |
| | | |
| | | |

---
Analyse dossier par dossier (5 min)

**Pour chaque dossier actuel, analysez :**

| Dossier | Ce qui devrait rester | Ce qui doit être déplacé | Vers où ? |
|---------|----------------------|--------------------------|-----------|
| models/ | Entités pures (Book, Member, Loan) | save(), get_by_id(), imports DB | adapters/db/ (repository) |
| services/ | ? | Logique + print() + DB | application/usecases/ + adapters/cli/ |
| database/ | ? | Connexion + init | adapters/db/ |
| utils/ | ? | date_utils, id_generator | ports/ (Clock) ou supprimer |

**Qu'est-ce qui devrait rester dans Book (domain/) ?**
- [ ] `__init__` avec validation ✅
- [ ] `save()` ❌ (déplacer vers BookRepository)
- [ ] `get_by_id()` ❌ (déplacer vers BookRepository)
- [ ] `is_available()` ✅ (logique métier)
- [ ] `mark_as_borrowed()` ✅ (logique métier)ifier disponibilité)
- [ ] Autre : _______________

**Classe Book refactorisée (écrivez les grandes lignes) :**

```python
class Book:
    def __init__(self, ...):
        # Quels attributs ?
        # Quelle validation ?
        pass
    
    # Quelles méthodes métier ?
```

---

### 2.5 Priorisation du refactoring

**Si vous ne pouviez refactorer qu'UNE SEULE chose en priorité, ce serait quoi ?**

☐ A. Extraire la persistance (créer BookRepository)  
☐ B. Créer les use cases (séparer logique applicative)  
☐ C. Séparer le domaine (classes pures)  
☐ D. Isoler le CLI (adaptateur)

**Votre choix :** ______  

**Justification :** _________________________________________________________________

_________________________________________________________________

---

## Phase 3 : Comparaison avec la solution (optionnel)

Si le temps le permet, consultez la branche `refactored-hexagonal` :

```bash
git checkout refactored-hexagonal
```

**Explorez la structure et comparez avec votre proposition :**

| Aspect | Votre proposition | Solution refactored | Similitudes / Différences |
|--------|-------------------|---------------------|--------------------------|
| Structure des dossiers | | | |
| Ports créés | | | |
| Use cases identifiés | | | |

**Question finale :** Qu'avez-vous appris de cette comparaison ?

_________________________________________________________________

_________________________________________________________________

---

## 🎓 Auto-évaluation

| Compétence | ☆☆☆☆☆ |
|------------|-------|
| Je comprends pourquoi le code actuel pose problème | |
| Je sais identifier les violations architecturales | |
| Je peux proposer une structure hexagonale | |
| Je comprends le rôle des ports (interfaces) | |
| Je sais différencier domaine / application / adaptateurs | |
| Je peux justifier mes choix d'architecture | |

**Une chose que j'ai comprise grâce à cet exercice :**

_________________________________________________________________

**Une question que je me pose encore :**

_________________________________________________________________

---

## 💡 Pour aller plus loin (après la séance)

1. Essayez de refactorer réellement le code (créez les fichiers)
2. Comparez étape par étape avec la branche `refactored-hexagonal`
3. Ajoutez des tests unitaires au domaine refactorisé
4. Proposez une API REST comme second adaptateur (à côté du CLI)

**Ressources :**
- Branche `refactored-hexagonal` du repo
- Annexes du cours sur l'architecture hexagonale
- Documentation sur le principe d'inversion de dépendances
