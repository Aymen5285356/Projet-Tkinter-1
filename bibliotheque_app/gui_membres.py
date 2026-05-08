# gui_membres.py
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

BG_SECTION = "#FFFFFF"
TEXT_PRIMARY = "#333333"
BTN_PRIMARY_BG = "#2E86C1"
BTN_DANGER_BG = "#C0392B"
BTN_TEXT = "#FFFFFF"

class MembresGUI:
    def __init__(self, parent, db):
        self.db = db
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        form_frame = tk.Frame(self.parent, bg=BG_SECTION, relief='groove', bd=1)
        form_frame.pack(fill='x', padx=20, pady=10)

        champs = [('Prénom:', 'prenom'), ('Nom:', 'nom'), ('Email:', 'email'), ('N° adhésion:', 'numero_adhésion')]
        self.entries = {}
        for i, (label, key) in enumerate(champs):
            tk.Label(form_frame, text=label, font=('Arial', 10), bg=BG_SECTION, fg=TEXT_PRIMARY).grid(row=0, column=i*2, padx=5, pady=10, sticky='e')
            entry = tk.Entry(form_frame, font=('Arial', 10), width=20, bg=BG_SECTION, fg=TEXT_PRIMARY, relief='solid', bd=1)
            entry.grid(row=0, column=i*2+1, padx=5, pady=10, sticky='w')
            self.entries[key] = entry

        btn_frame = tk.Frame(form_frame, bg=BG_SECTION)
        btn_frame.grid(row=0, column=len(champs)*2, padx=20, pady=10)
        tk.Button(btn_frame, text="Ajouter", command=self.ajouter, bg=BTN_PRIMARY_BG, fg=BTN_TEXT, font=('Arial', 9, 'bold'), width=10).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Modifier", command=self.modifier, bg=BTN_PRIMARY_BG, fg=BTN_TEXT, font=('Arial', 9, 'bold'), width=10).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Supprimer", command=self.supprimer, bg=BTN_DANGER_BG, fg=BTN_TEXT, font=('Arial', 9, 'bold'), width=10).pack(side='left', padx=5)

        search_frame = tk.Frame(self.parent, bg=BG_SECTION)
        search_frame.pack(fill='x', padx=20, pady=10)
        tk.Label(search_frame, text="Rechercher:", font=('Arial', 10), bg=BG_SECTION, fg=TEXT_PRIMARY).pack(side='left', padx=5)
        self.search_entry = tk.Entry(search_frame, font=('Arial', 10), width=30, bg=BG_SECTION, fg=TEXT_PRIMARY)
        self.search_entry.pack(side='left', padx=5)
        tk.Button(search_frame, text="Chercher", command=self.rechercher, bg=BTN_PRIMARY_BG, fg=BTN_TEXT, font=('Arial', 9, 'bold')).pack(side='left', padx=5)
        tk.Button(search_frame, text="Afficher tout", command=self.rafraichir, bg=BTN_PRIMARY_BG, fg=BTN_TEXT, font=('Arial', 9, 'bold')).pack(side='left', padx=5)

        self.tree = ttk.Treeview(self.parent, columns=('ID', 'Prénom', 'Nom', 'Email', 'N° adhésion'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Prénom', text='Prénom')
        self.tree.heading('Nom', text='Nom')
        self.tree.heading('Email', text='Email')
        self.tree.heading('N° adhésion', text='N° adhésion')
        self.tree.column('ID', width=50)
        self.tree.column('Prénom', width=120)
        self.tree.column('Nom', width=120)
        self.tree.column('Email', width=200)
        self.tree.column('N° adhésion', width=120)
        self.tree.pack(fill='both', expand=True, padx=20, pady=10)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        self.rafraichir()

    def ajouter(self):
        prenom = self.entries['prenom'].get()
        nom = self.entries['nom'].get()
        email = self.entries['email'].get()
        numero = self.entries['numero_adhésion'].get()
        if not prenom or not nom or not email or not numero:
            messagebox.showerror("Erreur", "Tous les champs sont requis.")
            return
        try:
            self.db.ajouter_membre(prenom, nom, email, numero)
        except sqlite3.IntegrityError:
            messagebox.showerror("Erreur", "Email ou numéro d'adhésion déjà existant.")
            return
        self.rafraichir()
        self.vider_champs()
        messagebox.showinfo("Succès", "Membre ajouté.")

    def modifier(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showerror("Erreur", "Sélectionnez un membre.")
            return
        membre_id = self.tree.item(selection[0])['values'][0]
        prenom = self.entries['prenom'].get()
        nom = self.entries['nom'].get()
        email = self.entries['email'].get()
        numero = self.entries['numero_adhésion'].get()
        if not prenom or not nom or not email or not numero:
            messagebox.showerror("Erreur", "Tous les champs sont requis.")
            return
        try:
            self.db.modifier_membre(membre_id, prenom, nom, email, numero)
        except sqlite3.IntegrityError:
            messagebox.showerror("Erreur", "Email ou numéro d'adhésion déjà existant.")
            return
        self.rafraichir()
        self.vider_champs()
        messagebox.showinfo("Succès", "Membre modifié.")

    def supprimer(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showerror("Erreur", "Sélectionnez un membre.")
            return
        membre_id = self.tree.item(selection[0])['values'][0]
        actifs = self.db.cursor.execute("SELECT COUNT(*) FROM emprunts WHERE membre_id=? AND date_retour IS NULL", (membre_id,)).fetchone()[0]
        if actifs > 0:
            messagebox.showerror("Erreur", "Impossible: ce membre a des emprunts actifs.")
            return
        if messagebox.askyesno("Confirmation", "Supprimer ce membre ?"):
            self.db.supprimer_membre(membre_id)
            self.rafraichir()
            self.vider_champs()
            messagebox.showinfo("Succès", "Membre supprimé.")

    def rechercher(self):
        terme = self.search_entry.get()
        if not terme:
            self.rafraichir()
            return
        resultats = self.db.rechercher_membres(terme)
        self.tree.delete(*self.tree.get_children())
        for membre in resultats:
            self.tree.insert('', 'end', values=membre)

    def rafraichir(self):
        self.tree.delete(*self.tree.get_children())
        membres = self.db.get_all_membres()
        for membre in membres:
            self.tree.insert('', 'end', values=membre)

    def on_select(self, event):
        selection = self.tree.selection()
        if selection:
            valeurs = self.tree.item(selection[0])['values']
            self.entries['prenom'].delete(0, tk.END)
            self.entries['prenom'].insert(0, valeurs[1])
            self.entries['nom'].delete(0, tk.END)
            self.entries['nom'].insert(0, valeurs[2])
            self.entries['email'].delete(0, tk.END)
            self.entries['email'].insert(0, valeurs[3])
            self.entries['numero_adhésion'].delete(0, tk.END)
            self.entries['numero_adhésion'].insert(0, valeurs[4])

    def vider_champs(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)