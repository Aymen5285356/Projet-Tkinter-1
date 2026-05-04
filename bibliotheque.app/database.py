import sqlite3
from datetime import date, timedelta

class Database:
    def __init__(self, db_name="bibliotheque.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS livres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                auteur TEXT NOT NULL,
                genre TEXT,
                annee INTEGER,
                exemplaires INTEGER DEFAULT 1
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS membres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL,
                email TEXT UNIQUE,
                numero_adh TEXT UNIQUE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS emprunts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                livre_id INTEGER,
                membre_id INTEGER,
                date_emprunt TEXT,
                date_retour_prevue TEXT,
                date_retour_reelle TEXT,
                FOREIGN KEY(livre_id) REFERENCES livres(id),
                FOREIGN KEY(membre_id) REFERENCES membres(id)
            )
        ''')
        self.conn.commit()

    def ajouter_livre(self, titre, auteur, genre, annee, exemplaires):
        try:
            self.cursor.execute('''
                INSERT INTO livres (titre, auteur, genre, annee, exemplaires)
                VALUES (?, ?, ?, ?, ?)
            ''', (titre, auteur, genre, annee, exemplaires))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Erreur: {e}")
            return False

    def modifier_livre(self, livre_id, titre, auteur, genre, annee, exemplaires):
        try:
            self.cursor.execute('''
                UPDATE livres SET titre=?, auteur=?, genre=?, annee=?, exemplaires=?
                WHERE id=?
            ''', (titre, auteur, genre, annee, exemplaires, livre_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Erreur: {e}")
            return False

    def supprimer_livre(self, livre_id):
        try:
            self.cursor.execute('''
                SELECT * FROM emprunts WHERE livre_id=? AND date_retour_reelle IS NULL
            ''', (livre_id,))
            if self.cursor.fetchone():
                raise Exception("Ce livre a des emprunts en cours")

            self.cursor.execute("DELETE FROM livres WHERE id=?", (livre_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Erreur: {e}")
            return False

    def rechercher_livres(self, mot_cle=""):
        query = "SELECT * FROM livres WHERE titre LIKE ? OR auteur LIKE ?"
        mot = f"%{mot_cle}%"
        self.cursor.execute(query, (mot, mot))
        return self.cursor.fetchall()

    def get_all_livres(self):
        self.cursor.execute("SELECT * FROM livres")
        return self.cursor.fetchall()

    def get_livre_by_id(self, livre_id):
        self.cursor.execute("SELECT * FROM livres WHERE id=?", (livre_id,))
        return self.cursor.fetchone()

    def ajouter_membre(self, nom, prenom, email, numero_adh):
        try:
            self.cursor.execute('''
                INSERT INTO membres (nom, prenom, email, numero_adh)
                VALUES (?, ?, ?, ?)
            ''', (nom, prenom, email, numero_adh))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Erreur: {e}")
            return False

    def modifier_membre(self, membre_id, nom, prenom, email, numero_adh):
        try:
            self.cursor.execute('''
                UPDATE membres SET nom=?, prenom=?, email=?, numero_adh=?
                WHERE id=?
            ''', (nom, prenom, email, numero_adh, membre_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Erreur: {e}")
            return False

    def supprimer_membre(self, membre_id):
        try:
            self.cursor.execute('''
                SELECT * FROM emprunts WHERE membre_id=? AND date_retour_reelle IS NULL
            ''', (membre_id,))
            if self.cursor.fetchone():
                raise Exception("Ce membre a des emprunts en cours")

            self.cursor.execute("DELETE FROM membres WHERE id=?", (membre_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Erreur: {e}")
            return False

    def rechercher_membres(self, mot_cle=""):
        query = "SELECT * FROM membres WHERE nom LIKE ? OR prenom LIKE ? OR numero_adh LIKE ?"
        mot = f"%{mot_cle}%"
        self.cursor.execute(query, (mot, mot, mot))
        return self.cursor.fetchall()

    def get_all_membres(self):
        self.cursor.execute("SELECT * FROM membres")
        return self.cursor.fetchall()

    def get_membre_by_id(self, membre_id):
        self.cursor.execute("SELECT * FROM membres WHERE id=?", (membre_id,))
        return self.cursor.fetchone()

    def ajouter_emprunt(self, livre_id, membre_id):
        try:
            self.cursor.execute("SELECT exemplaires FROM livres WHERE id=?", (livre_id,))
            result = self.cursor.fetchone()
            if not result:
                raise Exception("Livre inexistant")

            exemplaires = result[0]
            if exemplaires <= 0:
                raise Exception("Plus d'exemplaires disponibles")

            self.cursor.execute('''
                SELECT * FROM emprunts 
                WHERE livre_id=? AND membre_id=? AND date_retour_reelle IS NULL
            ''', (livre_id, membre_id))
            if self.cursor.fetchone():
                raise Exception("Ce membre a déjà ce livre en cours")

            aujourdhui = date.today().isoformat()
            retour_prevue = (date.today() + timedelta(days=14)).isoformat()
            self.cursor.execute('''
                INSERT INTO emprunts (livre_id, membre_id, date_emprunt, date_retour_prevue)
                VALUES (?, ?, ?, ?)
            ''', (livre_id, membre_id, aujourdhui, retour_prevue))

            self.cursor.execute("UPDATE livres SET exemplaires = exemplaires - 1 WHERE id=?", (livre_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Erreur: {e}")
            return False

    def retourner_livre(self, emprunt_id):
        try:
            self.cursor.execute("SELECT livre_id FROM emprunts WHERE id=?", (emprunt_id,))
            result = self.cursor.fetchone()
            if not result:
                raise Exception("Emprunt inexistant")

            livre_id = result[0]

            aujourdhui = date.today().isoformat()
            self.cursor.execute('''
                UPDATE emprunts SET date_retour_reelle=?
                WHERE id=?
            ''', (aujourdhui, emprunt_id))

            self.cursor.execute("UPDATE livres SET exemplaires = exemplaires + 1 WHERE id=?", (livre_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Erreur: {e}")
            return False

    def get_emprunts_en_cours(self):
        self.cursor.execute('''
            SELECT e.id, l.titre, m.nom, m.prenom, e.date_emprunt, e.date_retour_prevue
            FROM emprunts e
            JOIN livres l ON e.livre_id = l.id
            JOIN membres m ON e.membre_id = m.id
            WHERE e.date_retour_reelle IS NULL
        ''')
        return self.cursor.fetchall()

    def get_all_emprunts(self):
        self.cursor.execute('''
            SELECT e.id, l.titre, m.nom, m.prenom, e.date_emprunt, e.date_retour_prevue, 
                   CASE WHEN e.date_retour_reelle IS NULL THEN 'En cours' ELSE 'Rendu' END as statut
            FROM emprunts e
            JOIN livres l ON e.livre_id = l.id
            JOIN membres m ON e.membre_id = m.id
            ORDER BY e.date_emprunt DESC
        ''')
        return self.cursor.fetchall()

    def rechercher_emprunts(self, mot_cle=""):
        query = '''
            SELECT e.id, l.titre, m.nom, m.prenom, e.date_emprunt, e.date_retour_prevue,
                   CASE WHEN e.date_retour_reelle IS NULL THEN 'En cours' ELSE 'Rendu' END as statut
            FROM emprunts e
            JOIN livres l ON e.livre_id = l.id
            JOIN membres m ON e.membre_id = m.id
            WHERE l.titre LIKE ? OR m.nom LIKE ? OR m.prenom LIKE ?
            ORDER BY e.date_emprunt DESC
        '''
        mot = f"%{mot_cle}%"
        self.cursor.execute(query, (mot, mot, mot))
        return self.cursor.fetchall()

    def get_statistiques(self):
        stats = {}

        self.cursor.execute("SELECT COUNT(*) FROM livres")
        stats['total_livres'] = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT SUM(exemplaires) FROM livres")
        stats['exemplaires_disponibles'] = self.cursor.fetchone()[0] or 0

        self.cursor.execute("SELECT COUNT(*) FROM emprunts WHERE date_retour_reelle IS NULL")
        stats['emprunts_cours'] = self.cursor.fetchone()[0]

        self.cursor.execute('''
            SELECT l.titre, COUNT(e.id) as nb_emprunts
            FROM livres l
            JOIN emprunts e ON l.id = e.livre_id
            GROUP BY l.id
            ORDER BY nb_emprunts DESC
            LIMIT 5
        ''')
        stats['livres_populaires'] = self.cursor.fetchall()

        return stats

    def close(self):
        self.conn.close()