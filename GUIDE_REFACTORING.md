# 🔧 Guide de Refactoring Progressif

> **Objectif** : Transformer progressivement ce code vers une architecture maintenable, **sans tout casser**.
>
> 📚 **Quand utiliser ce guide ?** Après la séance encadrée (voir [README.md](README.md)), pour refactoriser en autonomie avec l'aide de l'IA.
>

## 🎯 Principe : Refactoring Incrémental

**"Make the change easy, then make the easy change"** - Kent Beck

### Règle d'or
- ✅ **Petits pas** : Une modification à la fois
- ✅ **Tests en continu** : Vérifier que rien ne casse après chaque étape
- ✅ **Progression visible** : Commit après chaque amélioration réussie

---

## 🤖 L'IA : Un Outil Puissant pour le Refactoring

### Pourquoi utiliser l'IA ?

L'IA (GitHub Copilot, ChatGPT, Claude, etc.) peut **considérablement accélérer** le refactoring :
- Génération de tests de caractérisation
- Extraction de méthodes/classes
- Création de ports (interfaces)
- Identification des code smells

### ⚠️ Comment bien utiliser l'IA ?

**✅ Bonnes pratiques :**
1. **Donnez du contexte** : Expliquez l'architecture cible (ex: "architecture hexagonale")
2. **Demandez des explications** : Ne copiez pas sans comprendre
3. **Validez chaque étape** : Lancez les tests après chaque modification générée
4. **Itérez** : Si le résultat n'est pas bon, précisez votre demande

**❌ Pièges à éviter :**
1. Ne pas demander "refactore tout" → préférez des étapes incrémentales
2. Ne pas tester le code généré → l'IA peut se tromper
3. Ne pas comprendre le code généré → vous ne pourrez pas le maintenir

### 💡 Exemples de prompts efficaces

- "Extrait la logique de calcul de statistiques de cette méthode dans une classe dédiée"
- "Crée un port (interface) pour ce repository avec les méthodes suivantes..."
- "Génère des tests unitaires pour cette classe en utilisant des mocks"
- "Identifie les violations du principe de responsabilité unique dans ce code"

---

## 🧪 Phase 0 : Expérimentation (Recommandée)

### Objectif : Comprendre le problème

**Avant de refactoriser, essayez de tester le code actuel.**

#### Exercice pratique (15-20 min max)

1. **Ouvrez** `tests/test_library_service.py`
2. **Essayez d'écrire un test unitaire** pour la méthode `borrow_book()`
3. **Contrainte** : Le test doit être rapide (<100ms) et ne pas dépendre de :
   - Base de données réelle
   - Système de fichiers (logs/)
   - Datetime système
   - Affichage console

#### Questions à se poser

- Quelles sont les difficultés rencontrées ?
- Quelles dépendances bloquent la testabilité ?
- Combien de comportements différents faudrait-il tester ?
- Est-ce que le test serait maintenable ?

#### Conclusion attendue

Vous devriez constater qu'il est **impossible ou très difficile** de tester unitairement `borrow_book()` dans son état actuel. Cette expérience motive le refactoring : **un code difficile à tester est un code mal structuré**.

---

## 📊 Priorisation des Problèmes

### 🔴 Priorité 1 : Rendre le code testable

**Pourquoi en premier ?**
- Sans tests, impossible de refactoriser en toute sécurité
- Les tests sont votre filet de sécurité
- La testabilité révèle les problèmes architecturaux

**Problèmes bloquants :**
1. **Couplage DB hardcodé** : `get_connection()` retourne toujours `library.db`
2. **Datetime système** : `datetime.now()` impossible à contrôler
3. **Effets de bord** : Logging, print(), I/O fichiers mélangés à la logique

### 🟠 Priorité 2 : Séparer les responsabilités

**Pourquoi ensuite ?**
- Une fois testable, on peut isoler chaque responsabilité sans risque
- Chaque extraction rend le code plus testable
- Progression visible (méthode `borrow_book` : 9 responsabilités → 1)

**Problèmes à traiter :**
1. **Violation SRP massive** : `borrow_book()` fait tout
2. **Models avec persistance** : `Book.save()`, `Member.save()`
3. **Service god class** : `LibraryService` orchestre + fait la logique

### 🟡 Priorité 3 : Inverser les dépendances

**Pourquoi en dernier ?**
- Nécessite que les responsabilités soient déjà séparées
- C'est le passage à l'architecture hexagonale proprement dite
- Demande le plus de restructuration

**Objectifs :**
1. Créer les ports (interfaces)
2. Faire dépendre les use cases des ports (pas des implémentations)
3. Injecter les dépendances

---

## 🛠️ Méthode : Refactoring Progressif

### Phase 1 : Établir un filet de sécurité (tests)

**Objectif** : Pouvoir détecter les régressions

#### Étape 1.1 : Ajouter des tests de caractérisation

**Qu'est-ce qu'un test de caractérisation ?**
- Un test qui documente le comportement **actuel** (même s'il est mauvais)
- Permet de s'assurer qu'on ne change pas le comportement pendant le refactoring
- Accepte temporairement les dépendances (DB, fichiers, datetime)

**Comment procéder ?**
1. Identifier un comportement observable (ex: création d'un fichier log)
2. Écrire un test end-to-end qui valide ce comportement
3. Capturer tous les outputs (print, fichiers, état de la DB)
4. Documenter les valeurs attendues

**💡 Astuce IA** : "Génère un test de caractérisation pour la méthode borrow_book qui valide que le fichier logs/borrows.log est créé avec le bon format"

#### Étape 1.2 : Identifier les seams (points d'injection)

**Qu'est-ce qu'un seam ?**
Un endroit où on peut injecter un comportement différent sans modifier le code appelant.

**Exemple concret :**
```python
# ❌ Pas de seam : impossible de tester avec une date fixe
def calculate_age():
    today = datetime.now()  # Dépendance hard-codée
    return today.year - birth_year

# ✅ Avec seam : on peut injecter une date pour les tests
def calculate_age(clock):
    today = clock.now()  # Dépendance injectable
    return today.year - birth_year

# En test : calculate_age(FixedClock("2026-01-01"))
# En prod : calculate_age(SystemClock())
```

**Seams typiques dans ce projet :**
- Fonction `get_connection()` → peut devenir un paramètre
- Appels à `datetime.now()` → peut devenir une dépendance Clock
- Appels à `print()` → peut être redirigé vers un logger injectable

**Technique** : Extraction de paramètres ou création de wrappers testables

**💡 Astuce IA** : "Identifie tous les seams dans cette méthode et propose des stratégies pour les rendre injectables"

---

### Phase 2 : Extraire et isoler

**Objectif** : Séparer chaque responsabilité en une classe/fonction dédiée

#### Étape 2.1 : Extraire les dépendances externes

**Technique : Envelopper les dépendances système dans des abstractions**

Pour chaque dépendance externe (datetime, DB, filesystem) :
1. Créer une abstraction (interface ou classe abstraite)
2. Créer une implémentation réelle (ex: SystemClock)
3. Créer une implémentation de test (ex: FixedClock)
4. Injecter la dépendance au lieu de l'appeler directement

**Avantages :**
- Tests deviennent déterministes
- Possibilité de tester des cas limites (ex: date dans le futur)
- Isolation complète de l'environnement système

**💡 Astuce IA** : "Crée une abstraction Clock avec une implémentation SystemClock et une FixedClock pour les tests"

#### Étape 2.2 : Extraire les services métier

**Technique : Créer une classe dédiée pour chaque responsabilité distincte**

Pour la méthode `borrow_book()` qui contient 9 responsabilités :
1. Identifier chaque bloc de responsabilité distinct
2. Extraire chaque bloc dans une classe dédiée
3. Injecter ces classes dans le service principal
4. Garder uniquement l'orchestration dans le service

**Responsabilités à extraire :**
- Calcul de statistiques → `StatisticsService`
- Logging fichiers → `LoggingService` ou `AuditTrail`
- Envoi d'emails → `EmailService` ou `NotificationService`
- Génération de recommandations → `RecommendationService`
- Génération d'ID → `IDGenerator`

**⚠️ Important** : Après chaque extraction, **relancer TOUS les tests** !

**💡 Astuce IA** : "Extrait la logique de calcul de statistiques (lignes X-Y) dans une classe StatisticsService avec une méthode calculate_borrowing_stats()"

#### Étape 2.3 : Séparer domaine et persistance

**Technique : Séparer les entités métier de la logique d'accès aux données**

**Principe :**
- Les entités du domaine (Book, Member, Loan) ne doivent PAS connaître la persistance
- Créer des repositories qui gèrent toute la logique SQL
- Les entités contiennent uniquement les attributs et la logique métier

**Étapes :**
1. Supprimer les méthodes `save()` des entités
2. Créer des classes Repository (BookRepository, MemberRepository, etc.)
3. Déplacer toute la logique SQL dans les repositories
4. Faire appeler les repositories par les services

**Avantage** : Le domaine devient testable sans DB.

**💡 Astuce IA** : "Refactorise la classe Book pour supprimer la méthode save() et crée un BookRepository qui gère la persistance"

---

### Phase 3 : Introduire l'abstraction (Ports)

**Objectif** : Rendre les use cases indépendants de l'infrastructure

⚠️ **Important : Éviter l'over-engineering**

Créer des ports/adapters n'est **pas systématique**. Posez-vous ces questions :
- Est-ce que cette dépendance change souvent ?
- Est-ce que je veux plusieurs implémentations (prod, test, mock) ?
- Est-ce que ça complique inutilement le code ?

**Exemples où c'est utile :**
- ✅ Repository (tests avec InMemory, prod avec SQLite)
- ✅ Clock (tests avec FixedClock, prod avec SystemClock)
- ✅ EmailSender (tests avec FakeEmailSender, prod avec SMTP)

**Exemples où c'est excessif :**
- ❌ Créer un port pour un calcul mathématique simple
- ❌ Abstraire une bibliothèque standard stable (json, math)
- ❌ Multiplier les interfaces quand une seule implémentation suffira toujours

**Règle** : Abstraire uniquement ce qui apporte de la **testabilité** ou de la **flexibilité** réelle.

#### Étape 3.1 : Créer les interfaces (ports)

Les use cases (logique métier) doivent dépendre d'abstractions, pas d'implémentations concrètes.
Voir l'[Annexe SOLID](../architecture-logicielle-BUT2-ressources/cm/annexe_04_principes_SOLID.md#-d---dependency-inversion-principle-dip) pour une explication détaillée du DIP (Dependency Inversion Principle).

**Comment procéder :**
1. Créer un dossier `ports/` pour les interfaces
2. Définir les contrats (méthodes nécessaires) pour chaque dépendance
3. Utiliser des classes abstraites (ABC) ou des Protocol de Python

**Exemple de ports à créer :**
- `BookRepository` (interface)
- `MemberRepository` (interface)
- `LoanRepository` (interface)
- `Clock` (interface)
- `EmailSender` (interface)

**💡 Astuce IA** : "Crée une interface BookRepository avec les méthodes get_by_id, save, find_available en utilisant ABC de Python"

#### Étape 3.2 : Faire dépendre les use cases des ports

**Transformation :**
Les use cases (anciennement dans LibraryService) doivent :
1. Recevoir des ports en paramètres du constructeur
2. Ne jamais importer directement des implémentations concrètes
3. Utiliser uniquement les méthodes définies dans les interfaces

**Structure cible :**
```
application/
  usecases/
    borrow_book.py  → dépend de BookRepository (port)
    create_book.py  → dépend de BookRepository (port)
```

**Avantage** : Injection de `InMemoryBookRepository()` dans les tests !

**💡 Astuce IA** : "Refactorise BorrowBookUseCase pour qu'il dépende de l'interface BookRepository au lieu de l'implémentation SQLite"

#### Étape 3.3 : Créer le composition root

**Qu'est-ce que le composition root ?**
Le seul endroit du code qui connaît les implémentations concrètes et assemble toutes les dépendances.

**Emplacement** : Généralement dans `main.py` ou un fichier `container.py`

**Responsabilités :**
1. Instancier les adapters (implémentations concrètes)
2. Instancier les use cases en injectant les adapters
3. Câbler toute l'application

**Règle** : Tous les autres fichiers ne connaissent que les interfaces (ports).

**💡 Astuce IA** : "Crée un composition root dans main.py qui instancie tous les adapters et use cases nécessaires"

---

## 🧪 Tests à Chaque Étape

### Stratégie de test progressive

| Phase | Type de tests | Objectif |
|-------|--------------|----------|
| **Phase 1** | Tests de caractérisation (intégration) | Filet de sécurité |
| **Phase 2** | Tests unitaires des classes extraites | Valider chaque extraction |
| **Phase 3** | Tests unitaires des use cases avec mocks | Valider l'architecture |

**Règle** : Ne jamais supprimer un test qui passe. Ajouter de nouveaux tests unitaires, garder les tests d'intégration.

---

## 📚 Ressources et Exemples

### Voir la branche `refactored-hexagonal`

Cette branche montre **UN exemple** d'architecture améliorée (pas forcément LA solution) :
- 23 tests (21 unitaires, 2 intégration)
- Séparation domain/ports/application/adapters
- Injection de dépendances explicite

**À comparer :**
```bash
git diff main refactored-hexagonal --stat
```

### Documents complémentaires

- **[VIOLATION_SRP.md](VIOLATION_SRP.md)** : Analyse du problème `borrow_book()`
- **[ANALYSE_REFACTORING.md](ANALYSE_REFACTORING.md)** (branche refactored) : Comparaison détaillée

---

## 🎯 Checklist de Progression

### ✅ Phase 1 : Testable
- [ ] Tests de caractérisation en place
- [ ] Clock injectable
- [ ] DB connection injectable
- [ ] Logging extractible

### ✅ Phase 2 : Séparé
- [ ] Entities sans persistance
- [ ] Services extraits (Statistics, Email, Logging)
- [ ] Use case avec logique métier pure
- [ ] Tests unitaires des entities

### ✅ Phase 3 : Inversé
- [ ] Ports (interfaces) créés
- [ ] Use cases dépendent des ports
- [ ] Adapters implémentent les ports
- [ ] Composition root en place
- [ ] Tests unitaires avec mocks

---

## 💡 Conseils Pratiques

### 1. Commencer petit
Ne refactorisez **PAS** tout d'un coup. Choisissez **une méthode** (ex: `create_book`) et appliquez toute la méthode dessus.

### 2. Commits fréquents
Un commit par étape qui fonctionne :
- `feat: extract Clock dependency`
- `refactor: separate Book entity from persistence`
- `test: add unit tests for Book entity`

### 3. Mesurer la progression
Indicateurs de qualité :
- **Nombre de tests unitaires** : Devrait augmenter
- **Temps d'exécution des tests** : Devrait diminuer
- **Nombre de dépendances externes** : Devrait diminuer dans la logique métier
- **Longueur des méthodes** : Devrait diminuer (méthodes <20 lignes idéalement)

### 4. Accepter l'imperfection
Le code ne sera jamais parfait. L'objectif est **d'améliorer progressivement**, pas d'atteindre la perfection.

### 5. Utiliser l'IA intelligemment
- **Décomposez** : Demandez une transformation à la fois
- **Vérifiez** : Lancez les tests après chaque génération
- **Comprenez** : Demandez des explications si nécessaire
- **Itérez** : Affinez vos prompts si le résultat n'est pas satisfaisant

---

## 🚀 Comment utiliser ce guide ?

### 📝 Contexte d'utilisation

Ce guide est conçu pour le **travail en autonomie après la séance encadrée**.

**Avant d'utiliser ce guide :**
1. Suivez d'abord le déroulement de la séance décrit dans le [README.md](README.md)
2. Analysez le problème avec [VIOLATION_SRP.md](VIOLATION_SRP.md)
3. Explorez la branche `refactored-hexagonal` pour voir un exemple de solution

**Utilisation de ce guide :**
- **Commencez par la Phase 0** : Expérimentez pour comprendre la difficulté
- **Suivez l'ordre des phases** : Testable → Séparé → Inversé
- **Allez à votre rythme** : Ce n'est pas un sprint de 1h, c'est un travail itératif
- **Utilisez l'IA** : Elle peut considérablement accélérer le refactoring

### 🎯 Approche recommandée

**Démarrage suggéré (premières étapes concrètes) :**

1. **(Phase 0)** Tentez d'écrire un test unitaire pour `borrow_book()` → constatez la difficulté
2. **(Phase 1)** Ajoutez un test de caractérisation pour `create_book()`
3. **(Phase 2.1)** Extrayez la génération d'ID dans une classe `IDGenerator`
4. **(Phase 2.1)** Rendez `IDGenerator` injectable dans `LibraryService`
5. **(Phase 2.3)** Séparez `Book` de sa persistance (créez `BookRepository`)
6. Continuez progressivement en suivant les phases du guide

**Avec l'aide de l'IA :**
- "Extrait la logique de génération d'ID de LibraryService dans une classe IDGenerator"
- "Crée une interface BookRepository avec les méthodes get_by_id, save, find_available"
- "Génère des tests unitaires pour la classe Book en utilisant des fixtures simples"
- "Identifie les seams dans la méthode borrow_book et propose comment les rendre injectables"

**Objectif** : Voir la testabilité s'améliorer à chaque étape. Commitez après chaque transformation réussie.

---

**Référence** : *Working Effectively with Legacy Code* - Michael Feathers
