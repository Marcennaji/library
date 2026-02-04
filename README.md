# 📚 Library Management System - Refactoring Challenge

> 🔧 **Exercice de refactoring : Du code problématique à l'architecture hexagonale**

## 🎯 Contexte

Ce projet est une application CLI de gestion de bibliothèque (emprunts de livres) qui **fonctionne** mais qui présente de nombreux **problèmes architecturaux**.

**Objectif pédagogique :** Diagnostiquer les problèmes, comprendre leurs impacts, et apprendre à refactoriser vers l'architecture hexagonale.

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
models/              # Entités mélangées avec persistance
├── book.py
├── member.py
└── loan.py
services/            # Service "god class" tout-en-un
├── library_service.py
└── validation.py
database/            # Accès direct SQLite
├── db_connection.py
└── init_db.py
utils/               # Utilitaires non abstraits
├── date_utils.py
└── id_generator.py
main.py              # CLI avec instanciation directe
```

**⚠️ Problèmes à identifier :**
- Couplage fort entre domaine et infrastructure
- Testabilité compromise
- Responsabilités mal séparées
- Pas d'injection de dépendances

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
- Créer des livres (IDs courts : B1, B2, ...)
- Créer des membres (IDs courts : M1, M2, ...)
- Emprunter/retourner des livres

**Note :** L'application fonctionne, mais analysez le code pour identifier les problèmes !

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
- ✅ **23 tests qui passent** (fixtures, unit tests, integration tests)
- ✅ **Testabilité démontrée** avec test doubles (InMemoryRepositories, FixedClock, FixedIDGenerator)
- ✅ **Documentation détaillée** (ANALYSE_REFACTORING.md)

**Lancer les tests :**
```bash
pytest tests/ -v
```

**Comparer les structures :**
```bash
# Voir les différences de fichiers entre les branches
git diff main refactored-hexagonal --name-status
```

**Utilisez-la pour comprendre le chemin de transformation !**

---

## 📝 Utilisation pédagogique

### 📋 Documents fournis :
- **FICHE_REFACTORING.md** : Feuille de route pour l'étudiant (diagnostic + planification)
- **GUIDE_ENSEIGNANT.md** : Correction et déroulé de séance (55min)
- **ANALYSE_REFACTORING.md** : Comparaison détaillée avant/après (disponible sur branche refactored-hexagonal)

### 🎓 Déroulement suggéré (55 min) :
1. **Phase 1 - Diagnostic** (20 min) : Analyser le code, identifier les problèmes
2. **Phase 2 - Correction collective** (25 min) : Comparer avec la branche refactored-hexagonal
3. **Phase 3 - Synthèse** (10 min) : Principes à retenir, application à son propre projet

---

## ⚠️ Note importante

**Ne comparez PAS mécaniquement ce code avec votre projet ticketing !** 

L'objectif est d'identifier les problèmes en appliquant les **principes architecturaux** :
- ✅ Le domaine est-il pur (sans dépendances externes) ?
- ✅ Les responsabilités sont-elles bien séparées ?
- ✅ Le code est-il testable ?
- ✅ Les dépendances sont-elles injectées ?

Les mêmes principes s'appliquent à TOUS les domaines métier (bibliothèque, ticketing, e-commerce, etc.).

---

## 📊 Statistiques

**Branche main (code problématique) :**
- 14 fichiers Python
- Couplage fort : models appellent directement la DB
- 0 tests (code non testable)

**Branche refactored-hexagonal (architecture propre) :**
- 30+ fichiers Python (mieux organisés)
- Couplage faible : injection de dépendances
- 23 tests qui passent (testabilité démontrée)

**Le bénéfice de l'architecture hexagonale : la testabilité !** 🎯
