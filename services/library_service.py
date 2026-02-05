"""Service de gestion de la bibliothèque."""

import os
from datetime import datetime, timedelta
from models.book import Book
from models.member import Member
from models.loan import Loan


class LibraryService:
    """Service principal gérant les opérations de la bibliothèque."""
    
    def create_book(self, title, author, isbn):
        """Crée un nouveau livre."""
        try:
            # Génère un ID court séquentiel
            all_books = Book.list_all()
            next_num = len(all_books) + 1
            book_id = f"B{next_num}"
            
            book = Book(
                id=book_id,
                title=title,
                author=author,
                isbn=isbn,
                status="available"
            )
            book.save()
            print(f"✅ Livre '{title}' créé avec succès !")
            return book
        except ValueError as e:
            print(f"❌ Erreur lors de la création du livre : {e}")
            return None
    
    def create_member(self, name, email):
        """Enregistre un nouveau membre."""
        try:
            # Génère un ID court séquentiel
            conn = Member.get_by_id("dummy")  # Juste pour avoir accès à la connexion
            from database.db_connection import get_connection
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM members")
            count = cursor.fetchone()[0]
            conn.close()
            next_num = count + 1
            member_id = f"M{next_num}"
            
            member = Member(
                id=member_id,
                name=name,
                email=email
            )
            member.save()
            print(f"✅ Membre '{name}' enregistré avec succès !")
            return member
        except ValueError as e:
            print(f"❌ Erreur lors de l'enregistrement : {e}")
            return None
    
    def borrow_book(self, book_id, member_id):
        """
        Gère l'emprunt d'un livre.
        
        VIOLATION MASSIVE DU SRP : Cette méthode fait TOUT !
        - Validation métier
        - Accès base de données
        - Calcul de statistiques
        - Logging fichier
        - Envoi email
        - Génération de rapports
        
        → IMPOSSIBLE à tester unitairement !
        """
        # 1. VALIDATION MÉTIER
        book = Book.get_by_id(book_id)
        member = Member.get_by_id(member_id)
        
        if not book:
            print("❌ Livre non trouvé !")
            return None
        
        if not member:
            print("❌ Membre non trouvé !")
            return None
        
        if not book.is_available():
            print(f"❌ Le livre '{book.title}' n'est pas disponible !")
            return None
        
        try:
            # 2. MISE À JOUR BASE DE DONNÉES
            book.mark_as_borrowed()
            book.save()
            
            # 3. CALCUL DE STATISTIQUES (mélangé avec la logique métier)
            from database.db_connection import get_connection
            conn = get_connection()
            cursor = conn.cursor()
            
            # Compter les emprunts du membre ce mois-ci
            cursor.execute("""
                SELECT COUNT(*) FROM loans 
                WHERE member_id = ? 
                AND strftime('%Y-%m', borrowed_at) = strftime('%Y-%m', 'now')
            """, (member_id,))
            monthly_borrows = cursor.fetchone()[0]
            
            # Calculer le taux d'activité du membre
            cursor.execute("SELECT COUNT(*) FROM loans WHERE member_id = ?", (member_id,))
            total_borrows = cursor.fetchone()[0]
            
            # Vérifier si le membre est un "lecteur actif" (>5 emprunts)
            is_active_reader = total_borrows >= 5
            
            # Compter combien de livres du même auteur sont disponibles
            cursor.execute("""
                SELECT COUNT(*) FROM books 
                WHERE author = ? AND status = 'available' AND id != ?
            """, (book.author, book_id))
            similar_books_available = cursor.fetchone()[0]
            
            # 4. GÉNÉRATION ID SÉQUENTIEL (encore un accès DB)
            cursor.execute("SELECT COUNT(*) FROM loans")
            count = cursor.fetchone()[0]
            loan_id = f"L{count + 1}"
            
            # 5. CRÉER LE LOAN
            loan = Loan(
                id=loan_id,
                book_id=book.id,
                member_id=member.id
            )
            loan.save()
            
            conn.close()
            
            # 6. LOGGING DANS UN FICHIER (I/O supplémentaire)
            log_dir = "logs"
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            with open(f"{log_dir}/borrows.log", "a", encoding="utf-8") as f:
                log_entry = (
                    f"{datetime.now().isoformat()} | "
                    f"Emprunt: {book.title} par {member.name} | "
                    f"Emprunts ce mois: {monthly_borrows + 1} | "
                    f"Total: {total_borrows + 1}\n"
                )
                f.write(log_entry)
            
            # 7. GÉNÉRATION DE RECOMMANDATIONS (logique complexe mélangée)
            recommendations = []
            if similar_books_available > 0:
                recommendations.append(
                    f"📚 {similar_books_available} autre(s) livre(s) de {book.author} disponible(s)"
                )
            
            if is_active_reader:
                recommendations.append("⭐ Vous êtes un lecteur actif ! Merci de votre fidélité.")
            
            # 8. SIMULATION D'ENVOI EMAIL (impossible à mocker facilement)
            email_subject = f"Confirmation d'emprunt : {book.title}"
            email_body = f"""
Bonjour {member.name},

Votre emprunt a été enregistré avec succès !

📖 Livre : {book.title}
✍️  Auteur : {book.author}
📅 Date de retour : {loan.due_date.strftime('%d/%m/%Y')}

Statistiques :
- Emprunts ce mois : {monthly_borrows + 1}
- Total d'emprunts : {total_borrows + 1}
- Statut : {'Lecteur actif' if is_active_reader else 'Nouveau lecteur'}

{chr(10).join(recommendations) if recommendations else ''}

Bonne lecture !
            """
            
            # Simuler l'envoi (écriture dans un fichier)
            email_log_path = f"{log_dir}/emails_sent.log"
            with open(email_log_path, "a", encoding="utf-8") as f:
                f.write(f"{'='*70}\n")
                f.write(f"TO: {member.email}\n")
                f.write(f"SUBJECT: {email_subject}\n")
                f.write(f"DATE: {datetime.now().isoformat()}\n")
                f.write(f"{'-'*70}\n")
                f.write(email_body)
                f.write(f"\n{'='*70}\n\n")
            
            # 9. AFFICHAGE CONSOLE (encore une responsabilité)
            print(f"✅ Livre '{book.title}' emprunté par {member.name} !")
            print(f"   Date de retour prévue : {loan.due_date.strftime('%d/%m/%Y')}")
            
            if monthly_borrows >= 3:
                print(f"   ⚠️  Attention : C'est votre {monthly_borrows + 1}e emprunt ce mois !")
            
            if recommendations:
                print("\n   💡 Recommandations :")
                for rec in recommendations:
                    print(f"      {rec}")
            
            print(f"\n   📧 Email de confirmation envoyé à {member.email}")
            
            return loan
            
        except ValueError as e:
            print(f"❌ Erreur : {e}")
            return None
        except Exception as e:
            print(f"❌ Erreur inattendue : {e}")
            return None
    
    def return_book(self, book_id):
        """Gère le retour d'un livre."""
        book = Book.get_by_id(book_id)
        
        if not book:
            print("❌ Livre non trouvé !")
            return False
        
        loan = Loan.find_active_loan(book_id)
        
        if not loan:
            print(f"❌ Aucun emprunt actif trouvé pour '{book.title}' !")
            return False
        
        book.mark_as_returned()
        book.save()
        
        loan.mark_as_returned()
        loan.save()
        
        if loan.is_overdue():
            days_overdue = (datetime.now() - loan.due_date).days
            print(f"⚠️  Le livre '{book.title}' avait {days_overdue} jour(s) de retard !")
        
        print(f"✅ Livre '{book.title}' retourné avec succès !")
        return True
    
    def list_all_books(self):
        """Liste tous les livres de la bibliothèque."""
        books = Book.list_all()
        
        if not books:
            print("Aucun livre dans la bibliothèque.")
            return []
        
        print(f"\n{'='*70}")
        print(f"{'ID':<5} {'Titre':<30} {'Auteur':<22} {'Statut':<10}")
        print(f"{'='*70}")
        for book in books:
            status_fr = "disponible" if book.status == "available" else "emprunté"
            print(f"{book.id:<5} {book.title:<30} {book.author:<22} {status_fr:<10}")
        print(f"{'='*70}\n")
        
        return books
    
    def list_available_books(self):
        """Liste les livres disponibles."""
        books = Book.list_available()
        
        if not books:
            print("Aucun livre disponible.")
            return []
        
        print(f"\n{'='*70}")
        print(f"{'ID':<5} {'Titre':<30} {'Auteur':<32}")
        print(f"{'='*70}")
        for book in books:
            print(f"{book.id:<5} {book.title:<30} {book.author:<32}")
        print(f"{'='*70}\n")
        
        return books
    
    def list_all_members(self):
        """Liste tous les membres."""
        from database.db_connection import get_connection
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM members")
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            print("Aucun membre enregistré.")
            return []
        
        print(f"\n{'='*70}")
        print(f"{'ID':<5} {'Nom':<25} {'Email':<37}")
        print(f"{'='*70}")
        for row in rows:
            member = Member(row[0], row[1], row[2], row[3])
            print(f"{member.id:<5} {member.name:<25} {member.email:<37}")
        print(f"{'='*70}\n")
        
        return rows
