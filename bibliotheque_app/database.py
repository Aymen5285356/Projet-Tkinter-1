# database.py
import sqlite3
from datetime import datetime, timedelta

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('bibliotheque.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS livres (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                titre TEXT NOT NULL,
                                auteur TEXT NOT NULL,
                                genre TEXT,
                                annee INTEGER,
                                exemplaires INTEGER NOT NULL)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS membres (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                prenom TEXT NOT NULL,
                                nom TEXT NOT NULL,
                                email TEXT NOT NULL UNIQUE,
                                numero_adhésion TEXT NOT NULL UNIQUE)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS emprunts (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                livre_id INTEGER NOT NULL,
                                membre_id INTEGER NOT NULL,
                                date_emprunt TEXT NOT NULL,
                                date_retour_prevue TEXT NOT NULL,
                                date_retour TEXT,
                                FOREIGN KEY (livre_id) REFERENCES livres (id),
                                FOREIGN KEY (membre_id) REFERENCES membres (id))''')
        self.conn.commit()

    def ajouter_livre(self, titre, auteur, genre, annee, exemplaires):
        self.cursor.execute("INSERT INTO livres (titre, auteur, genre, annee, exemplaires) VALUES (?, ?, ?, ?, ?)",
                            (titre, auteur, genre, annee, exemplaires))
        self.conn.commit()

    def modifier_livre(self, livre_id, titre, auteur, genre, annee, exemplaires):
        self.cursor.execute("UPDATE livres SET titre=?, auteur=?, genre=?, annee=?, exemplaires=? WHERE id=?",
                            (titre, auteur, genre, annee, exemplaires, livre_id))
        self.conn.commit()

    def supprimer_livre(self, livre_id):
        self.cursor.execute("DELETE FROM livres WHERE id=?", (livre_id,))
        self.conn.commit()

    def rechercher_livres(self, terme):
        terme = f'%{terme}%'
        self.cursor.execute("SELECT * FROM livres WHERE titre LIKE ? OR auteur LIKE ?", (terme, terme))
        return self.cursor.fetchall()

    def get_all_livres(self):
        self.cursor.execute("SELECT * FROM livres")
        return self.cursor.fetchall()

    def get_livre_by_id(self, livre_id):
        self.cursor.execute("SELECT * FROM livres WHERE id=?", (livre_id,))
        return self.cursor.fetchone()

    def ajouter_membre(self, prenom, nom, email, numero_adhésion):
        self.cursor.execute("INSERT INTO membres (prenom, nom, email, numero_adhésion) VALUES (?, ?, ?, ?)",
                            (prenom, nom, email, numero_adhésion))
        self.conn.commit()

    def modifier_membre(self, membre_id, prenom, nom, email, numero_adhésion):
        self.cursor.execute("UPDATE membres SET prenom=?, nom=?, email=?, numero_adhésion=? WHERE id=?",
                            (prenom, nom, email, numero_adhésion, membre_id))
        self.conn.commit()

    def supprimer_membre(self, membre_id):
        self.cursor.execute("DELETE FROM membres WHERE id=?", (membre_id,))
        self.conn.commit()

    def rechercher_membres(self, terme):
        terme = f'%{terme}%'
        self.cursor.execute("SELECT * FROM membres WHERE prenom LIKE ? OR nom LIKE ? OR numero_adhésion LIKE ?",
                            (terme, terme, terme))
        return self.cursor.fetchall()

    def get_all_membres(self):
        self.cursor.execute("SELECT * FROM membres")
        return self.cursor.fetchall()

    def get_membre_by_id(self, membre_id):
        self.cursor.execute("SELECT * FROM membres WHERE id=?", (membre_id,))
        return self.cursor.fetchone()

    def ajouter_emprunt(self, livre_id, membre_id, date_emprunt, date_retour_prevue):
        self.cursor.execute("INSERT INTO emprunts (livre_id, membre_id, date_emprunt, date_retour_prevue, date_retour) VALUES (?, ?, ?, ?, NULL)",
                            (livre_id, membre_id, date_emprunt, date_retour_prevue))
        self.conn.commit()
        self.cursor.execute("UPDATE livres SET exemplaires = exemplaires - 1 WHERE id=?", (livre_id,))
        self.conn.commit()

    def retourner_livre(self, emprunt_id, livre_id):
        date_retour = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute("UPDATE emprunts SET date_retour=? WHERE id=?", (date_retour, emprunt_id))
        self.conn.commit()
        self.cursor.execute("UPDATE livres SET exemplaires = exemplaires + 1 WHERE id=?", (livre_id,))
        self.conn.commit()

    def get_emprunts_actifs(self):
        self.cursor.execute('''SELECT emprunts.id, livres.titre, membres.prenom, membres.nom, emprunts.date_emprunt, emprunts.date_retour_prevue
                               FROM emprunts
                               JOIN livres ON emprunts.livre_id = livres.id
                               JOIN membres ON emprunts.membre_id = membres.id
                               WHERE emprunts.date_retour IS NULL''')
        return self.cursor.fetchall()

    def rechercher_emprunts(self, terme):
        terme = f'%{terme}%'
        self.cursor.execute('''SELECT emprunts.id, livres.titre, membres.prenom, membres.nom, emprunts.date_emprunt, emprunts.date_retour_prevue
                               FROM emprunts
                               JOIN livres ON emprunts.livre_id = livres.id
                               JOIN membres ON emprunts.membre_id = membres.id
                               WHERE emprunts.date_retour IS NULL AND (livres.titre LIKE ? OR membres.prenom LIKE ? OR membres.nom LIKE ?)
                            ''', (terme, terme, terme))
        return self.cursor.fetchall()

    def verifier_emprunt_existant(self, livre_id, membre_id):
        self.cursor.execute('''SELECT * FROM emprunts WHERE livre_id = ? AND membre_id = ? AND date_retour IS NULL''',
                            (livre_id, membre_id))
        return self.cursor.fetchone() is not None

    def get_exemplaires_disponibles(self, livre_id):
        self.cursor.execute("SELECT exemplaires FROM livres WHERE id=?", (livre_id,))
        resultat = self.cursor.fetchone()
        return resultat[0] if resultat else 0

    def get_statistiques(self):
        total_livres = self.cursor.execute("SELECT SUM(exemplaires) FROM livres").fetchone()[0] or 0
        emprunts_cours = self.cursor.execute("SELECT COUNT(*) FROM emprunts WHERE date_retour IS NULL").fetchone()[0] or 0
        plus_empruntes = self.cursor.execute('''SELECT livres.titre, COUNT(emprunts.id) as nombre_emprunts
                                                FROM emprunts
                                                JOIN livres ON emprunts.livre_id = livres.id
                                                GROUP BY livres.id
                                                ORDER BY nombre_emprunts DESC
                                                LIMIT 5''').fetchall()
        exemplaires_dispo = self.cursor.execute("SELECT SUM(exemplaires) FROM livres").fetchone()[0] or 0
        return total_livres, emprunts_cours, plus_empruntes, exemplaires_dispo

    def close(self):
        self.conn.close()