# 📚 Library Management System - Refactoring Challenge

> 🔧 **Exercice de refactoring : De la boule de boue à l'architecture hexagonale**

## 🎯 Contexte

Ce projet est une application CLI de gestion de bibliothèque (emprunts de livres) qui **fonctionne** mais qui est structurée comme un **"big ball of mud"** (grosse boule de boue).

**Objectif pédagogique :** Diagnostiquer les problèmes architecturaux et proposer un refactoring vers l'architecture hexagonale.

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

## 🏗️ Architecture (supposément hexagonale)

```
src/
├── domain/              # Entités métier
│   ├── book.py
│   ├── member.py
│   └── loan.py
├── ports/               # Interfaces
│   ├── book_repository.py
│   └── clock.py
├── application/         # Cas d'usage
│   └── usecases/
│       └── borrow_book.py
├── adapters/            # Implémentations techniques
│   ├── api/
│   │   └── book_router.py
│   └── db/
│       └── book_repository_in_memory.py
└── main.py              # Composition root
```

---

## 🔍 Mission : Trouvez les 10 violations !

Ce code viole 10 principes d'architecture hexagonale. À vous de les identifier !

**Indice sur la répartition :**
- Domain (domain/) : 6 violations
- Application (application/) : 2 violations
- Adaptateurs (adapters/) : 2 violations

**Principes à vérifier :**
1. **Indépendance du domaine** : Aucune dépendance externe (framework, DB, etc.)
2. **Inversion de dépendances** : Use cases dépendent de ports (interfaces), pas d'adaptateurs
3. **Injection de dépendances** : Pas d'instanciation directe dans les constructeurs
4. **Séparation des responsabilités** : Le domaine ne gère pas la persistance
5. **Respect des couches** : Les adaptateurs n'exécutent pas de logique métier

---

## 🚀 Installation

```bash
# Cloner le repo
git clone https://github.com/[enseignant]/library-violations-pedagogiques
cd library-violations-pedagogiques

# Vous êtes sur la branche 'main' (big ball of mud)
```

## 🧪 Lancer l'application (branche main)

```bash
python library.py
```

Vous verrez un menu CLI pour gérer la bibliothèque.

**Note :** L'application fonctionne, mais le code est ingérable !

---

## 🌟 Solution refactorisée (branche refactored-hexagonal)

Pour voir la version refactorisée en architecture hexagonale :

```bash
git checkout refactored-hexagonal
```

Cette branche contient :
- Structure hexagonale complète
- Domain pur (aucune dépendance externe)
- Ports & Adapters bien séparés
- Use cases testables
- Code maintenable et évolutif

**Utilisez-la pour comprendre le chemin de transformation !**

---

## 📝 Utilisation pédagogique

1. **Analyse individuelle** (15 min) : Parcourir le code et identifier les violations
2. **Correction collective** (30 min) : Discussion et correction guidée
3. **Transfert** (10 min) : Vérifier son propre projet ticketing

---

## ⚠️ Note importante

**Ne comparez PAS ce code avec votre projet ticketing !** 

L'objectif est d'identifier les violations en appliquant les **principes architecturaux**, pas en comparant mécaniquement deux projets.

Les mêmes principes s'appliquent à TOUS les domaines métier.
