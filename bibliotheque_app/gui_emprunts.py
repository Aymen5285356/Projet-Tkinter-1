# gui_emprunts.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

BG_SECTION = "#FFFFFF"
TEXT_PRIMARY = "#333333"
BTN_PRIMARY_BG = "#2E86C1"
BTN_DANGER_BG = "#C0392B"
BTN_TEXT = "#FFFFFF"

class EmpruntsGUI:
    def __init__(self, parent, db):
        self.db = db
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        form_frame = tk.Frame(self.parent, bg=BG_SECTION, relief='groove', bd=1)
        form_frame.pack(fill='x', padx=20, pady=10)

        tk.Label(form_frame, text="Livre:", font=('Arial', 10), bg=BG_SECTION, fg=TEXT_PRIMARY).grid(row=0, column=0, padx=5, pady=10, sticky='e')
        self.livre_combo = ttk.Combobox(form_frame, font=('Arial', 10), width=40)
        self.livre_combo.grid(row=0, column=1, padx=5, pady=10)

        tk.Label(form_frame, text="Membre:", font=('Arial', 10), bg=BG_SECTION, fg=TEXT_PRIMARY).grid(row=0, column=2, padx=5, pady=10, sticky='e')
        self.membre_combo = ttk.Combobox(form_frame, font=('Arial', 10), width=40)
        self.membre_combo.grid(row=0, column=3, padx=5, pady=10)

        tk.Button(form_frame, text="Enregistrer Emprunt", command=self.enregistrer_emprunt, bg=BTN_PRIMARY_BG, fg=BTN_TEXT, font=('Arial', 9, 'bold'), width=20).grid(row=0, column=4, padx=20, pady=10)

        search_frame = tk.Frame(self.parent, bg=BG_SECTION)
        search_frame.pack(fill='x', padx=20, pady=10)
        tk.Label(search_frame, text="Rechercher emprunt:", font=('Arial', 10), bg=BG_SECTION, fg=TEXT_PRIMARY).pack(side='left', padx=5)
        self.search_entry = tk.Entry(search_frame, font=('Arial', 10), width=30, bg=BG_SECTION, fg=TEXT_PRIMARY)
        self.search_entry.pack(side='left', padx=5)
        tk.Button(search_frame, text="Chercher", command=self.rechercher, bg=BTN_PRIMARY_BG, fg=BTN_TEXT, font=('Arial', 9, 'bold')).pack(side='left', padx=5)
        tk.Button(search_frame, text="Afficher tout", command=self.rafraichir, bg=BTN_PRIMARY_BG, fg=BTN_TEXT, font=('Arial', 9, 'bold')).pack(side='left', padx=5)

        self.tree = ttk.Treeview(self.parent, columns=('ID', 'Livre', 'Membre', 'Date emprunt', 'Retour prévu'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Livre', text='Livre')
        self.tree.heading('Membre', text='Membre')
        self.tree.heading('Date emprunt', text='Date emprunt')
        self.tree.heading('Retour prévu', text='Retour prévu')
        self.tree.column('ID', width=50)
        self.tree.column('Livre', width=250)
        self.tree.column('Membre', width=200)
        self.tree.column('Date emprunt', width=100)
        self.tree.column('Retour prévu', width=100)
        self.tree.pack(fill='both', expand=True, padx=20, pady=10)

        btn_retour = tk.Button(self.parent, text="Enregistrer Retour", command=self.enregistrer_retour, bg=BTN_DANGER_BG, fg=BTN_TEXT, font=('Arial', 9, 'bold'), width=20)
        btn_retour.pack(pady=10)

        self.rafraichir_combos()
        self.rafraichir()

    def rafraichir_combos(self):
        livres = self.db.get_all_livres()
        self.livre_combo['values'] = [f"{l[0]} - {l[1]} (Dispo: {l[5]})" for l in livres if l[5] > 0]
        membres = self.db.get_all_membres()
        self.membre_combo['values'] = [f"{m[0]} - {m[1]} {m[2]}" for m in membres]

    def enregistrer_emprunt(self):
        livre_sel = self.livre_combo.get()
        membre_sel = self.membre_combo.get()
        if not livre_sel or not membre_sel:
            messagebox.showerror("Erreur", "Sélectionnez un livre et un membre.")
            return
        livre_id = int(livre_sel.split(' - ')[0])
        membre_id = int(membre_sel.split(' - ')[0])

        exemplaires = self.db.get_exemplaires_disponibles(livre_id)
        if exemplaires <= 0:
            messagebox.showerror("Erreur", "Plus d'exemplaires disponibles.")
            return

        if self.db.verifier_emprunt_existant(livre_id, membre_id):
            messagebox.showerror("Erreur", "Ce membre a déjà emprunté ce livre et ne l'a pas rendu.")
            return

        date_emprunt = datetime.now().strftime("%Y-%m-%d")
        date_retour_prevue = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
        self.db.ajouter_emprunt(livre_id, membre_id, date_emprunt, date_retour_prevue)
        self.rafraichir_combos()
        self.rafraichir()
        messagebox.showinfo("Succès", f"Emprunt enregistré. Retour prévu le {date_retour_prevue}")

    def enregistrer_retour(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showerror("Erreur", "Sélectionnez un emprunt.")
            return
        emprunt_id = self.tree.item(selection[0])['values'][0]
        livre_titre = self.tree.item(selection[0])['values'][1]
        if messagebox.askyesno("Confirmation", f"Retour du livre '{livre_titre}' ?"):
            livre_id = self.db.cursor.execute("SELECT livre_id FROM emprunts WHERE id=?", (emprunt_id,)).fetchone()[0]
            self.db.retourner_livre(emprunt_id, livre_id)
            self.rafraichir_combos()
            self.rafraichir()
            messagebox.showinfo("Succès", "Retour enregistré.")

    def rechercher(self):
        terme = self.search_entry.get()
        if not terme:
            self.rafraichir()
            return
        resultats = self.db.rechercher_emprunts(terme)
        self.tree.delete(*self.tree.get_children())
        for emp in resultats:
            nom_complet = f"{emp[2]} {emp[3]}"
            self.tree.insert('', 'end', values=(emp[0], emp[1], nom_complet, emp[4], emp[5]))

    def rafraichir(self):
        self.tree.delete(*self.tree.get_children())
        emprunts = self.db.get_emprunts_actifs()
        for emp in emprunts:
            nom_complet = f"{emp[2]} {emp[3]}"
            self.tree.insert('', 'end', values=(emp[0], emp[1], nom_complet, emp[4], emp[5]))