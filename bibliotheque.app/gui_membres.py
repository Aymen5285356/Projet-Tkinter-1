import tkinter as tk
from tkinter import ttk, messagebox

class GestionMembres:
    def __init__(self, parent, db):
        self.db = db
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        cadre_form = ttk.LabelFrame(self.frame, text="Informations du membre", padding=10)
        cadre_form.pack(fill="x", pady=5)

        ttk.Label(cadre_form, text="Nom:").grid(row=0, column=0, sticky="w", pady=2)
        self.nom = ttk.Entry(cadre_form, width=30)
        self.nom.grid(row=0, column=1, pady=2, padx=5)

        ttk.Label(cadre_form, text="Prénom:").grid(row=1, column=0, sticky="w", pady=2)
        self.prenom = ttk.Entry(cadre_form, width=30)
        self.prenom.grid(row=1, column=1, pady=2, padx=5)

        ttk.Label(cadre_form, text="Email:").grid(row=2, column=0, sticky="w", pady=2)
        self.email = ttk.Entry(cadre_form, width=30)
        self.email.grid(row=2, column=1, pady=2, padx=5)

        ttk.Label(cadre_form, text="Numéro d'adhésion:").grid(row=3, column=0, sticky="w", pady=2)
        self.numero_adh = ttk.Entry(cadre_form, width=30)
        self.numero_adh.grid(row=3, column=1, pady=2, padx=5)

        cadre_boutons = ttk.Frame(self.frame)
        cadre_boutons.pack(fill="x", pady=10)

        ttk.Button(cadre_boutons, text="Ajouter", command=self.ajouter).pack(side="left", padx=5)
        ttk.Button(cadre_boutons, text="Modifier", command=self.modifier).pack(side="left", padx=5)
        ttk.Button(cadre_boutons, text="Supprimer", command=self.supprimer).pack(side="left", padx=5)
        ttk.Button(cadre_boutons, text="Rechercher", command=self.rechercher).pack(side="left", padx=5)
        ttk.Button(cadre_boutons, text="Rafraîchir", command=self.rafraichir).pack(side="left", padx=5)

        cadre_recherche = ttk.Frame(self.frame)
        cadre_recherche.pack(fill="x", pady=5)

        ttk.Label(cadre_recherche, text="Rechercher:").pack(side="left", padx=5)
        self.recherche_entry = ttk.Entry(cadre_recherche, width=30)
        self.recherche_entry.pack(side="left", padx=5)
        ttk.Button(cadre_recherche, text="Chercher", command=self.rechercher).pack(side="left", padx=5)

        cadre_tableau = ttk.LabelFrame(self.frame, text="Liste des membres", padding=5)
        cadre_tableau.pack(fill="both", expand=True, pady=5)

        colonnes = ("ID", "Nom", "Prénom", "Email", "N° Adhésion")
        self.tree = ttk.Treeview(cadre_tableau, columns=colonnes, show="headings", height=15)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Nom", text="Nom")
        self.tree.heading("Prénom", text="Prénom")
        self.tree.heading("Email", text="Email")
        self.tree.heading("N° Adhésion", text="N° Adhésion")

        self.tree.column("ID", width=50)
        self.tree.column("Nom", width=150)
        self.tree.column("Prénom", width=150)
        self.tree.column("Email", width=200)
        self.tree.column("N° Adhésion", width=120)

        scrollbar = ttk.Scrollbar(cadre_tableau, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", self.remplir_champs)
        self.rafraichir()

    def rafraichir(self):
        """Rafraîchir la liste des membres"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        for membre in self.db.get_all_membres():
            self.tree.insert("", "end", values=membre)

    def remplir_champs(self, event):
        """Remplir les champs avec les données du membre sélectionné"""
        selection = self.tree.selection()
        if selection:
            valeurs = self.tree.item(selection[0])["values"]
            self.nom.delete(0, tk.END)
            self.nom.insert(0, valeurs[1])
            self.prenom.delete(0, tk.END)
            self.prenom.insert(0, valeurs[2])
            self.email.delete(0, tk.END)
            self.email.insert(0, valeurs[3])
            self.numero_adh.delete(0, tk.END)
            self.numero_adh.insert(0, valeurs[4])

    def vider_champs(self):
        """Vider tous les champs"""
        self.nom.delete(0, tk.END)
        self.prenom.delete(0, tk.END)
        self.email.delete(0, tk.END)
        self.numero_adh.delete(0, tk.END)

    def ajouter(self):
        """Ajouter un nouveau membre"""
        if not self.nom.get() or not self.prenom.get() or not self.email.get() or not self.numero_adh.get():
            messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs")
            return

        if self.db.ajouter_membre(self.nom.get(), self.prenom.get(), self.email.get(), self.numero_adh.get()):
            messagebox.showinfo("Succès", "Membre ajouté avec succès")
            self.vider_champs()
            self.rafraichir()
        else:
            messagebox.showerror("Erreur", "Impossible d'ajouter le membre (email ou numéro d'adhésion existe déjà)")

    def modifier(self):
        """Modifier le membre sélectionné"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Avertissement", "Sélectionnez un membre à modifier")
            return

        if not self.nom.get() or not self.prenom.get() or not self.email.get() or not self.numero_adh.get():
            messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs")
            return

        membre_id = self.tree.item(selection[0])["values"][0]
        if self.db.modifier_membre(membre_id, self.nom.get(), self.prenom.get(), self.email.get(),
                                   self.numero_adh.get()):
            messagebox.showinfo("Succès", "Membre modifié avec succès")
            self.vider_champs()
            self.rafraichir()
        else:
            messagebox.showerror("Erreur", "Impossible de modifier le membre (email ou numéro d'adhésion existe déjà)")

    def supprimer(self):
        """Supprimer le membre sélectionné"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Avertissement", "Sélectionnez un membre à supprimer")
            return

        if messagebox.askyesno("Confirmation", "Supprimer ce membre ?\n(Il ne doit avoir aucun emprunt en cours)"):
            membre_id = self.tree.item(selection[0])["values"][0]
            if self.db.supprimer_membre(membre_id):
                messagebox.showinfo("Succès", "Membre supprimé avec succès")
                self.vider_champs()
                self.rafraichir()
            else:
                messagebox.showerror("Erreur", "Impossible de supprimer le membre (il a des emprunts en cours)")

    def rechercher(self):
        """Rechercher des membres"""
        mot_cle = self.recherche_entry.get()
        for item in self.tree.get_children():
            self.tree.delete(item)

        resultats = self.db.rechercher_membres(mot_cle)
        for membre in resultats:
            self.tree.insert("", "end", values=membre)

        if not resultats:
            messagebox.showinfo("Information", "Aucun membre trouvé")