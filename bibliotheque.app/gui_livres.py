import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

class GestionLivres:
    def __init__(self, parent, db):
        self.db = db
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        ttk.Label(self.frame, text="Titre:").grid(row=0, column=0)
        self.titre = ttk.Entry(self.frame)
        self.titre.grid(row=0, column=1)

        ttk.Label(self.frame, text="Auteur:").grid(row=1, column=0)
        self.auteur = ttk.Entry(self.frame)
        self.auteur.grid(row=1, column=1)

        ttk.Label(self.frame, text="Genre:").grid(row=2, column=0)
        self.genre = ttk.Entry(self.frame)
        self.genre.grid(row=2, column=1)

        ttk.Label(self.frame, text="Année:").grid(row=3, column=0)
        self.annee = ttk.Entry(self.frame)
        self.annee.grid(row=3, column=1)

        ttk.Label(self.frame, text="Exemplaires:").grid(row=4, column=0)
        self.exemplaires = ttk.Entry(self.frame)
        self.exemplaires.grid(row=4, column=1)

        ttk.Button(self.frame, text="Ajouter", command=self.ajouter).grid(row=5, column=0)
        ttk.Button(self.frame, text="Modifier", command=self.modifier).grid(row=5, column=1)
        ttk.Button(self.frame, text="Supprimer", command=self.supprimer).grid(row=5, column=2)
        ttk.Button(self.frame, text="Rechercher", command=self.rechercher).grid(row=5, column=3)

        colonnes = ("ID", "Titre", "Auteur", "Genre", "Année", "Exemplaires")
        self.tree = ttk.Treeview(self.frame, columns=colonnes, show="headings")
        for col in colonnes:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.grid(row=6, column=0, columnspan=5, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.remplir_champs)
        self.rafraichir()

    def rafraichir(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for livre in self.db.get_all_livres():
            self.tree.insert("", "end", values=livre)

    def remplir_champs(self, event):
        selection = self.tree.selection()
        if selection:
            valeurs = self.tree.item(selection[0])["values"]
            self.titre.delete(0, tk.END)
            self.titre.insert(0, valeurs[1])
            self.auteur.delete(0, tk.END)
            self.auteur.insert(0, valeurs[2])
            self.genre.delete(0, tk.END)
            self.genre.insert(0, valeurs[3])
            self.annee.delete(0, tk.END)
            self.annee.insert(0, valeurs[4])
            self.exemplaires.delete(0, tk.END)
            self.exemplaires.insert(0, valeurs[5])

    def ajouter(self):
        (self.db.ajouter_livre
        (
            self.titre.get(), self.auteur.get(),
            self.genre.get(), self.annee.get(),
            self.exemplaires.get()
        ))
        self.rafraichir()

    def modifier(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Avertissement", "Sélectionnez un livre à modifier")
            return
        livre_id = self.tree.item(selection[0])["values"][0]
        (self.db.modifier_livre
        (
            livre_id, self.titre.get(), self.auteur.get(),
            self.genre.get(), self.annee.get(),
            self.exemplaires.get()
        ))
        self.rafraichir()

    def supprimer(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Avertissement", "Sélectionnez un livre à supprimer")
            return
        if messagebox.askyesno("Confirmation", "Supprimer ce livre ?"):
            livre_id = self.tree.item(selection[0])["values"][0]
            self.db.supprimer_livre(livre_id)
            self.rafraichir()

    def rechercher(self):
        mot = self.titre.get()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for livre in self.db.rechercher_livres(mot):
            self.tree.insert("", "end", values=livre)