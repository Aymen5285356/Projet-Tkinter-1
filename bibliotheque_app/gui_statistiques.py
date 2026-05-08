# gui_statistiques.py
import tkinter as tk
from tkinter import ttk

BG_SECTION = "#FFFFFF"
TEXT_PRIMARY = "#333333"
TEXT_SECONDARY = "#555555"
BTN_PRIMARY_BG = "#2E86C1"
BTN_TEXT = "#FFFFFF"

class StatistiquesGUI:
    def __init__(self, parent, db):
        self.db = db
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        self.stats_frame = tk.Frame(self.parent, bg=BG_SECTION)
        self.stats_frame.pack(fill='both', expand=True, padx=20, pady=20)

        self.rafraichir()

        btn_refresh = tk.Button(self.parent, text="Actualiser", command=self.rafraichir, bg=BTN_PRIMARY_BG, fg=BTN_TEXT, font=('Arial', 9, 'bold'), width=15)
        btn_refresh.pack(pady=10)

    def rafraichir(self):
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        total_livres, emprunts_cours, plus_empruntes, exemplaires_dispo = self.db.get_statistiques()

        tk.Label(self.stats_frame, text="STATISTIQUES DE LA BIBLIOTHÈQUE", font=('Arial', 16, 'bold'), bg=BG_SECTION, fg=TEXT_PRIMARY).pack(pady=20)

        stats_card = tk.Frame(self.stats_frame, bg=BG_SECTION, relief='groove', bd=2)
        stats_card.pack(fill='x', padx=50, pady=10)

        tk.Label(stats_card, text=f"📚 Nombre total de livres en stock: {total_livres}", font=('Arial', 12), bg=BG_SECTION, fg=TEXT_PRIMARY).pack(anchor='w', padx=20, pady=10)
        tk.Label(stats_card, text=f"📖 Nombre d'exemplaires disponibles: {exemplaires_dispo}", font=('Arial', 12), bg=BG_SECTION, fg=TEXT_PRIMARY).pack(anchor='w', padx=20, pady=10)
        tk.Label(stats_card, text=f"🔄 Nombre d'emprunts en cours: {emprunts_cours}", font=('Arial', 12), bg=BG_SECTION, fg=TEXT_PRIMARY).pack(anchor='w', padx=20, pady=10)

        tk.Label(self.stats_frame, text="Livres les plus empruntés:", font=('Arial', 14, 'bold'), bg=BG_SECTION, fg=TEXT_PRIMARY).pack(pady=(20,10))

        top_frame = tk.Frame(self.stats_frame, bg=BG_SECTION, relief='groove', bd=2)
        top_frame.pack(fill='x', padx=50, pady=10)

        if plus_empruntes:
            for livre in plus_empruntes:
                tk.Label(top_frame, text=f"🏆 {livre[0]} - {livre[1]} emprunt(s)", font=('Arial', 11), bg=BG_SECTION, fg=TEXT_SECONDARY).pack(anchor='w', padx=20, pady=5)
        else:
            tk.Label(top_frame, text="Aucun emprunt enregistré", font=('Arial', 11), bg=BG_SECTION, fg=TEXT_SECONDARY).pack(anchor='w', padx=20, pady=10)