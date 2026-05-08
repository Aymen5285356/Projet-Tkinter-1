# gui_livres.py
import tkinter as tk
from tkinter import ttk, messagebox

BG_SECTION = "#FFFFFF"
TEXT_PRIMARY = "#333333"
BTN_PRIMARY_BG = "#2E86C1"
BTN_DANGER_BG = "#C0392B"
BTN_TEXT = "#FFFFFF"

class LivresGUI:
    def __init__(self, parent, db):
        self.db = db
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        form_frame = tk.Frame(self.parent, bg=BG_SECTION, relief='groove', bd=1)
        form_frame.pack(fill='x', padx=20, pady=10)

        champs = [('Titre:', 'titre'), ('Auteur:', 'auteur'), ('Genre:', 'genre'), ('Année:', 'annee'), ('Exemplaires:', 'exemplaires')]
        self.entries = {}
        for i, (label, key) in enumerate(champs):
            tk.Label(form_frame, text=label, font=('Arial', 10), bg=BG_SECTION, fg=TEXT_PRIMARY).grid(row=0, column=i*2, padx=5, pady=10, sticky='e')
            entry = tk.Entry(form_frame, font=('Arial', 10), width=15, bg=BG_SECTION, fg=TEXT_PRIMARY, relief='solid', bd=1)
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

        self.tree = ttk.Treeview(self.parent, columns=('ID', 'Titre', 'Auteur', 'Genre', 'Année', 'Exemplaires'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Titre', text='Titre')
        self.tree.heading('Auteur', text='Auteur')
        self.tree.heading('Genre', text='Genre')
        self.tree.heading('Année', text='Année')
        self.tree.heading('Exemplaires', text='Exemplaires')
        self.tree.column('ID', width=50)
        self.tree.column('Titre', width=200)
        self.tree.column('Auteur', width=150)
        self.tree.column('Genre', width=100)
        self.tree.column('Année', width=80)
        self.tree.column('Exemplaires', width=100)
        self.tree.pack(fill='both', expand=True, padx=20, pady=10)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        self.rafraichir()

    def ajouter(self):
        titre = self.entries['titre'].get()
        auteur = self.entries['auteur'].get()
        genre = self.entries['genre'].get()
        annee = self.entries['annee'].get()
        exemplaires = self.entries['exemplaires'].get()
        if not titre or not auteur or not exemplaires:
            messagebox.showerror("Erreur", "Titre, Auteur et Exemplaires sont requis.")
            return
        try:
            annee = int(annee) if annee else None
            exemplaires = int(exemplaires)
            if exemplaires < 1:
                raise ValueError
        except:
            messagebox.showerror("Erreur", "Année et Exemplaires doivent être des nombres valides.")
            return
        self.db.ajouter_livre(titre, auteur, genre, annee, exemplaires)
        self.rafraichir()
        self.vider_champs()
        messagebox.showinfo("Succès", "Livre ajouté.")

    def modifier(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showerror("Erreur", "Sélectionnez un livre.")
            return
        livre_id = self.tree.item(selection[0])['values'][0]
        titre = self.entries['titre'].get()
        auteur = self.entries['auteur'].get()
        genre = self.entries['genre'].get()
        annee = self.entries['annee'].get()
        exemplaires = self.entries['exemplaires'].get()
        if not titre or not auteur or not exemplaires:
            messagebox.showerror("Erreur", "Titre, Auteur et Exemplaires sont requis.")
            return
        try:
            annee = int(annee) if annee else None
            exemplaires = int(exemplaires)
            if exemplaires < 1:
                raise ValueError
        except:
            messagebox.showerror("Erreur", "Année et Exemplaires doivent être des nombres.")
            return
        self.db.modifier_livre(livre_id, titre, auteur, genre, annee, exemplaires)
        self.rafraichir()
        self.vider_champs()
        messagebox.showinfo("Succès", "Livre modifié.")

    def supprimer(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showerror("Erreur", "Sélectionnez un livre.")
            return
        livre_id = self.tree.item(selection[0])['values'][0]
        actifs = self.db.cursor.execute("SELECT COUNT(*) FROM emprunts WHERE livre_id=? AND date_retour IS NULL", (livre_id,)).fetchone()[0]
        if actifs > 0:
            messagebox.showerror("Erreur", "Impossible: ce livre a des emprunts actifs.")
            return
        if messagebox.askyesno("Confirmation", "Supprimer ce livre ?"):
            self.db.supprimer_livre(livre_id)
            self.rafraichir()
            self.vider_champs()
            messagebox.showinfo("Succès", "Livre supprimé.")

    def rechercher(self):
        terme = self.search_entry.get()
        if not terme:
            self.rafraichir()
            return
        resultats = self.db.rechercher_livres(terme)
        self.tree.delete(*self.tree.get_children())
        for livre in resultats:
            self.tree.insert('', 'end', values=livre)

    def rafraichir(self):
        self.tree.delete(*self.tree.get_children())
        livres = self.db.get_all_livres()
        for livre in livres:
            self.tree.insert('', 'end', values=livre)

    def on_select(self, event):
        selection = self.tree.selection()
        if selection:
            valeurs = self.tree.item(selection[0])['values']
            self.entries['titre'].delete(0, tk.END)
            self.entries['titre'].insert(0, valeurs[1])
            self.entries['auteur'].delete(0, tk.END)
            self.entries['auteur'].insert(0, valeurs[2])
            self.entries['genre'].delete(0, tk.END)
            self.entries['genre'].insert(0, valeurs[3] if valeurs[3] else '')
            self.entries['annee'].delete(0, tk.END)
            self.entries['annee'].insert(0, valeurs[4] if valeurs[4] else '')
            self.entries['exemplaires'].delete(0, tk.END)
            self.entries['exemplaires'].insert(0, valeurs[5])

    def vider_champs(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)