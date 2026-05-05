import tkinter as tk
from tkinter import ttk, messagebox

class GestionEmprunts:
    def __init__(self, parent, db):
        self.db = db
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        cadre_emprunt = ttk.LabelFrame(self.frame, text="Nouvel emprunt", padding=10)
        cadre_emprunt.pack(fill="x", pady=5)

        ttk.Label(cadre_emprunt, text="Livre:").grid(row=0, column=0, sticky="w", pady=5)
        self.livre_combo = ttk.Combobox(cadre_emprunt, width=40)
        self.livre_combo.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(cadre_emprunt, text="Membre:").grid(row=1, column=0, sticky="w", pady=5)
        self.membre_combo = ttk.Combobox(cadre_emprunt, width=40)
        self.membre_combo.grid(row=1, column=1, pady=5, padx=5)

        ttk.Button(cadre_emprunt, text=" Enregistrer l'emprunt", command=self.enregistrer_emprunt).grid(row=2,column=0,columnspan=2,pady=10)

        cadre_retour = ttk.LabelFrame(self.frame, text="Retour de livre", padding=10)
        cadre_retour.pack(fill="x", pady=5)

        ttk.Label(cadre_retour, text="Rechercher emprunt:").grid(row=0, column=0, sticky="w", pady=5)
        self.recherche_emprunt = ttk.Entry(cadre_retour, width=40)
        self.recherche_emprunt.grid(row=0, column=1, pady=5, padx=5)
        ttk.Button(cadre_retour, text=" Rechercher", command=self.rechercher_emprunts).grid(row=0, column=2, pady=5,padx=5)

        cadre_tableau = ttk.LabelFrame(self.frame, text="Liste des emprunts", padding=5)
        cadre_tableau.pack(fill="both", expand=True, pady=5)

        colonnes = ("ID", "Livre", "Membre", "Date emprunt", "Retour prévue", "Statut")
        self.tree = ttk.Treeview(cadre_tableau, columns=colonnes, show="headings", height=15)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Livre", text="Livre")
        self.tree.heading("Membre", text="Membre")
        self.tree.heading("Date emprunt", text="Date emprunt")
        self.tree.heading("Retour prévue", text="Retour prévue")
        self.tree.heading("Statut", text="Statut")

        self.tree.column("ID", width=50)
        self.tree.column("Livre", width=200)
        self.tree.column("Membre", width=150)
        self.tree.column("Date emprunt", width=100)
        self.tree.column("Retour prévue", width=100)
        self.tree.column("Statut", width=80)

        scrollbar = ttk.Scrollbar(cadre_tableau, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        cadre_boutons = ttk.Frame(self.frame)
        cadre_boutons.pack(fill="x", pady=10)
        ttk.Button(cadre_boutons, text="Enregistrer le retour", command=self.enregistrer_retour).pack(side="left",padx=5)
        ttk.Button(cadre_boutons, text="Rafraîchir", command=self.rafraichir).pack(side="left", padx=5)

        self.charger_combos()
        self.rafraichir()

    def charger_combos(self):
        """Charger les livres et membres dans les combobox"""
        try:
            livres = self.db.get_all_livres()
            livres_dispo = []

            for livre in livres:
                try:
                    exemplaires_valeur = livre[5]
                    if isinstance(exemplaires_valeur, str):
                        exemplaires_valeur = int(exemplaires_valeur) if exemplaires_valeur.isdigit() else 0
                    elif exemplaires_valeur is None:
                        exemplaires_valeur = 0

                    if exemplaires_valeur > 0:
                        livres_dispo.append(f"{livre[1]} - {livre[2]} (ID:{livre[0]})")
                except (ValueError, TypeError, IndexError):
                    continue

            self.livre_combo['values'] = livres_dispo

            membres = self.db.get_all_membres()
            membres_list = []
            for membre in membres:
                try:
                    membres_list.append(f"{membre[1]} {membre[2]} - {membre[4]} (ID:{membre[0]})")
                except IndexError:
                    continue

            self.membre_combo['values'] = membres_list

            if not livres_dispo:
                print("Aucun livre disponible pour l'emprunt")
            if not membres_list:
                print("Aucun membre enregistré")

        except Exception as e:
            print(f"Erreur dans charger_combos: {e}")

    def enregistrer_emprunt(self):
        """Enregistrer un nouvel emprunt"""
        if not self.livre_combo.get() or not self.membre_combo.get():
            messagebox.showwarning("Champs manquants", "Veuillez sélectionner un livre et un membre")
            return

        livre_text = self.livre_combo.get()
        membre_text = self.membre_combo.get()

        livre_id = int(livre_text.split("ID:")[1].split(")")[0])
        membre_id = int(membre_text.split("ID:")[1].split(")")[0])

        if self.db.ajouter_emprunt(livre_id, membre_id):
            messagebox.showinfo("Succès", "Emprunt enregistré avec succès")
            self.livre_combo.set("")
            self.membre_combo.set("")
            self.charger_combos()
            self.rafraichir()
        else:
            messagebox.showerror("Erreur",
                                 "Impossible d'enregistrer l'emprunt\n(Vérifiez la disponibilité et que le membre n'a pas déjà ce livre)")

    def enregistrer_retour(self):
        """Enregistrer le retour d'un livre"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Avertissement", "Sélectionnez un emprunt à retourner")
            return

        valeurs = self.tree.item(selection[0])["values"]
        if valeurs[5] == "Rendu":
            messagebox.showwarning("Attention", "Ce livre a déjà été retourné")
            return

        if messagebox.askyesno("Confirmation", "Enregistrer le retour de ce livre ?"):
            emprunt_id = valeurs[0]
            if self.db.retourner_livre(emprunt_id):
                messagebox.showinfo("Succès", "Retour enregistré avec succès")
                self.charger_combos()
                self.rafraichir()
            else:
                messagebox.showerror("Erreur", "Impossible d'enregistrer le retour")

    def rafraichir(self):
        """Rafraîchir la liste des emprunts"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        for emprunt in self.db.get_all_emprunts():
            self.tree.insert("", "end", values=emprunt)

    def rechercher_emprunts(self):
        """Rechercher des emprunts"""
        mot_cle = self.recherche_emprunt.get()
        if not mot_cle:
            self.rafraichir()
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        resultats = self.db.rechercher_emprunts(mot_cle)
        for emprunt in resultats:
            self.tree.insert("", "end", values=emprunt)

        if not resultats:
            messagebox.showinfo("Information", "Aucun emprunt trouvé")