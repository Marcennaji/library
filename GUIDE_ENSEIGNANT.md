# 📋 Guide Enseignant - Exercice Refactoring Pédagogique

## 🎯 Objectif de l'exercice

**Séance :** TD4b - Séance 10 (31 mars 2026)  
**Durée :** 55 minutes  
**Moment :** Après le QCM (exercice pratique final)

**But pédagogique :** 
- Consolider la compréhension des principes d'architecture hexagonale
- Développer la compétence de diagnostic architectural
- Comprendre que séparer en dossiers ≠ bonne architecture
- Transférer les apprentissages à un nouveau domaine métier (bibliothèque)

---

## 📦 Contenu du repo

**Thème :** Gestion de bibliothèque (emprunts de livres)

**Structure du repo :**
```
library-violations-pedagogiques/
├── README.md                  # Présentation du projet
├── FICHE_REFACTORING.md       # À distribuer aux étudiants
├── GUIDE_ENSEIGNANT.md        # Ce fichier (correction détaillée)
├── requirements.txt           # Dépendances (aucune, juste stdlib)
├── models/                    # ❌ Entités mélangées avec persistance
│   ├── book.py               # Book avec save(), get_by_id()
│   ├── member.py             # Member avec méthodes DB
│   └── loan.py               # Loan avec persistance
├── services/                  # ❌ Service "god class"
│   ├── library_service.py    # Fait tout : logique + print + DB
│   └── validation.py         # Validations externalisées
├── database/                  # ❌ Infrastructure mélangée
│   ├── db_connection.py      # get_connection() SQLite
│   └── init_db.py            # CREATE TABLE scripts
├── utils/                     # ❌ Wrappers sans abstraction
│   ├── date_utils.py         # get_current_datetime()
│   └── id_generator.py       # generate_id()
└── main.py                    # ❌ CLI sans injection de dépendances
```

**Branche refactored-hexagonal (pour correction) :**
```
src/
├── domain/                    # ✅ Entités pures
│   ├── book.py
│   ├── member.py
│   └── loan.py
├── ports/                     # ✅ Interfaces
│   ├── book_repository.py
│   ├── member_repository.py
│   └── clock.py
├── application/               # ✅ Use cases
│   └── usecases/
│       ├── borrow_book.py
│       └── return_book.py
├── adapters/                  # ✅ Implémentations
│   ├── db/
│   │   ├── book_repository_sqlite.py
│   │   └── member_repository_sqlite.py
│   └── cli/
│       └── cli_adapter.py
└── main.py                    # ✅ Composition root
```
```

---

## 🎬 Déroulé de l'exercice (55 min)

### **Phase 1 : Distribution et exploration (5 min)**

**Actions :**
1. Projeter l'URL du repo : `https://github.com/[votre-compte]/library-violations-pedagogiques`
2. Demander aux étudiants de cloner (branche `main` par défaut)
3. Distribuer `FICHE_REFACTORING.md` (imprimée ou numérique)

**Consigne orale :**
> "Ce projet de bibliothèque fonctionne. Il est séparé en dossiers models/, services/, database/... mais l'architecture est mauvaise. Votre objectif : diagnostiquer les problèmes et proposer un refactoring vers l'hexagonale."

**Lancer l'appli ensemble (1 min de démo) :**
```bash
python main.py
# Créer un livre → Créer un membre → Emprunter
```

---

### **Phase 2 : Diagnostic (20 min)**

**Les étudiants :**
- Remplissent les sections 1.1, 1.2, 1.3 de la fiche
- Identifient les problèmes d'architecture
- Notent les fichiers concernés et les violations

**Votre rôle :**
- Circuler dans la salle
- Orienter les blocages : "Regardez models/book.py ligne 50 : la méthode save() vous semble normale ?"
- Si un étudiant dit "c'est bien structuré", demander : "Que fait Book.get_by_id() ? Est-ce le rôle d'une entité ?"

**Questions pièges à anticiper :**
- "Mais prof, c'est bien séparé en dossiers !" → Oui, mais regarde les **dépendances**
- "C'est un modèle MVC classique non ?" → Oui, et c'est justement le problème : couplage fort

---

### **Phase 3 : Refactoring proposé (20 min)**

**Les étudiants :**
- Remplissent les sections 2.1 à 2.5 (architecture cible)
- Dessinent le schéma hexagonal
- Proposent le découpage en use cases

**Votre rôle :**
- Vérifier les schémas proposés
- Valider ou corriger les découpages

**Pattern de questions :**
1. "Qu'est-ce qui doit rester dans Book (domaine) ?"
   → Validation, logique métier (`is_available()`), rien d'autre
2. "Où va `save()` ?" → Dans BookRepository (adapter)
3. "Pourquoi validation.py existe séparément ?" → Validation = responsabilité du domaine

---

### **Phase 4 : Correction collective (10 min)**

**Afficher la branche `refactored-hexagonal` :**
```bash
git checkout refactored-hexagonal
```

1. **Sollicitation** : "Qui a trouvé une violation dans domain/book.py ?"
2. **Réponse étudiant** : Un étudiant partage
3. **Discussion** : "Pourquoi c'est un problème ?"
4. **Correction** : Vous projetez le code corrigé (CORRECTION.md)
5. **Principe** : Vous reliez à un principe architectural

**Ordre suggéré (du plus évident au plus subtil) :**

| Ordre | Violation | Fichier | Difficulté |
|-------|-----------|---------|------------|
| 1 | Import FastAPI | domain/book.py:8 | ⭐ Facile |
| 2 | HTTPException | domain/book.py:41 | ⭐ Facile |
| 3 | save_to_database() | domain/book.py:75 | ⭐⭐ Moyen |
| 4 | send_notification() | domain/book.py:97 | ⭐⭐ Moyen |
| 5 | datetime.now() | domain/book.py:53 | ⭐⭐⭐ Subtil |
| 6 | Import datetime | domain/book.py:11 | ⭐⭐⭐ Subtil |
| 7 | Import adaptateur | usecases/borrow_book.py:13 | ⭐⭐ Moyen |
| 8 | Instanciation directe | usecases/borrow_book.py:24 | ⭐⭐ Moyen |
| 9 | Logique dans API | api/book_router.py:34 | ⭐⭐ Moyen |
| 10 | Import domaine dans API | api/book_router.py:14 | ⭐⭐⭐ Débat |

**Gestion du temps :**
- Si en avance : Approfondir les questions de réflexion
- Si en retard : Regrouper violations similaires (1+3, 2+4, 7+8)

---

### **Phase 4 : Synthèse et transfert (5 min)**

**Questions finales (projeter) :**

1. **"Ces violations existent-elles dans votre projet ticketing ?"**
   - Levez la main si vous pensez avoir corrigé toutes les violations
   - Qui va vérifier son code après cette séance ?

2. **"Quel est le principe le plus important selon vous ?"**
   - Discussion rapide (2-3 étudiants)

3. **"En stage, comment allez-vous appliquer ces principes ?"**
   - Code review de vos collègues
   - Proposer des refactorings architecturaux
   - Questionner les choix techniques

**Message de clôture :**
> "Félicitations ! Vous venez de faire une vraie code review architecturale. Cette compétence est aussi importante que d'écrire du code. En entreprise, vous allez reviewer et être reviewés quotidiennement. Les principes que vous avez appris s'appliquent à TOUS les domaines métier : bibliothèque, ticketing, e-commerce, banque... C'est ça, être un bon développeur."

---

## 🛠️ Préparation avant la séance

### **1 semaine avant (2-3h de travail) :**

✅ **Créer le repo GitHub/GitLab**
```bash
cd C:\Users\Utilisateur\admin\iut\library-violations-pedagogiques
git init
git add .
git commit -m "Initial commit: Library violations pédagogiques"
git remote add origin https://github.com/[votre-compte]/library-violations-pedagogiques.git
git push -u origin main
```

✅ **Rendre le repo public**
- Settings → Visibility → Public
- (À remettre en privé après la séance)

✅ **Tester le code**
```bash
# Vérifier que l'application fonctionne malgré les violations
cd library-violations-pedagogiques
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --reload
# Ouvrir http://127.0.0.1:8000/docs
```

✅ **Préparer les supports**
- Imprimer FICHE_EXERCICE.md (1 par étudiant) OU envoyer par email
- Projeter CORRECTION.md sur votre écran
- Préparer l'URL du repo sur un slide

---

### **Le jour J (15 min avant) :**

✅ **Vérifier le repo**
- Le repo est bien public
- L'URL fonctionne
- Le README s'affiche correctement

✅ **Préparer votre poste**
- Ouvrir CORRECTION.md dans un éditeur
- Ouvrir le repo dans VS Code (pour navigation rapide)
- Tester l'URL du repo

---

## 💡 Conseils pédagogiques

### **Si les étudiants trouvent facilement (< 10 min) :**
- ✅ C'est une bonne nouvelle (ils ont bien compris)
- Demandez-leur d'expliquer POURQUOI c'est une violation
- Ajoutez une question : "Comment corrigeriez-vous ?"

### **Si les étudiants galèrent (> 20 min) :**
- Donnez des indices progressifs :
  - "Cherchez dans domain/book.py"
  - "Regardez les imports en haut du fichier"
  - "Quelle bibliothèque ne devrait jamais être dans le domaine ?"

### **Si débat sur la violation #9 (import domaine dans API) :**
- C'est normal, c'est une zone grise
- Expliquez les 2 écoles :
  - **Puriste** : Jamais d'import direct (créer des DTO/schémas)
  - **Pragmatique** : OK si lecture seule pour conversion
- **Ici** : La violation est combinée avec #10 (logique métier dans API)

### **Si question "Pourquoi l'app fonctionne malgré les violations ?" :**
- ✅ Excellente question !
- "Les violations sont des problèmes d'ARCHITECTURE, pas de FONCTIONNEMENT"
- "Ça fonctionne aujourd'hui, mais ça pose problème quand on veut faire évoluer le code"
- Exemple : "Essayez de changer de DB ou de framework → vous devez tout réécrire"

---

## 📊 Évaluation (optionnel)

Si vous voulez évaluer la compréhension :

**Critères :**
- Nombre de violations trouvées (8-10 = excellent)
- Qualité des explications (principe violé identifié)
- Réponses aux questions de réflexion

**Grille rapide :**
- 8-10 violations + explications correctes = Très bonne compréhension
- 5-7 violations = Bonne compréhension
- 1-4 violations = À consolider

---

## 🎯 Objectifs pédagogiques validés

À la fin de cet exercice, les étudiants sont capables de :

✅ Identifier les violations d'architecture hexagonale dans un code inconnu  
✅ Appliquer les principes architecturaux à un nouveau domaine métier  
✅ Expliquer POURQUOI une violation est problématique  
✅ Proposer une correction architecturale  
✅ Transférer cette compétence à leur propre projet  

---

## 📞 Si besoin d'ajustements

**Exercice trop facile ?** Ajoutez des violations subtiles :
- Violation 11 : Use case qui retourne un DTO au lieu d'une entité
- Violation 12 : Port défini dans adapters/ au lieu de ports/

**Exercice trop difficile ?** Réduisez à 5-7 violations :
- Gardez : 1, 3, 5, 7, 8, 10
- Supprimez : 2, 4, 6, 9 (plus subtiles)

---

## ✅ Checklist finale

Avant la séance :
- [ ] Repo créé et public
- [ ] Code testé (uvicorn fonctionne)
- [ ] FICHE_EXERCICE.md imprimée/distribuée
- [ ] CORRECTION.md ouvert sur votre écran
- [ ] URL du repo prête à partager

Pendant la séance :
- [ ] Phase 1 : Distribution (5 min)
- [ ] Phase 2 : Analyse (15 min)
- [ ] Phase 3 : Correction (30 min)
- [ ] Phase 4 : Synthèse (5 min)

Après la séance :
- [ ] Remettre le repo en privé (optionnel)
- [ ] Noter les retours étudiants (pour l'année prochaine)
- [ ] Archiver les fiches remplies (si collectées)

---

Bonne séance ! 🚀
