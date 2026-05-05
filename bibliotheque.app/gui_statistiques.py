import tkinter as tk
from tkinter import ttk, messagebox

class GestionStatistiques:
    def __init__(self, parent, db):
        self.db = db
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.rafraichir()
        ttk.Button(self.frame, text="Rafraîchir les statistiques", command=self.rafraichir).pack(pady=10)

    def rafraichir(self):
        """Rafraîchir et afficher les statistiques"""
        for widget in self.frame.winfo_children():
            if isinstance(widget, ttk.LabelFrame):
                widget.destroy()

        stats = self.db.get_statistiques()
        cadre_general = ttk.LabelFrame(self.frame, text="Statistiques générales", padding=15)
        cadre_general.pack(fill="x", pady=5)

        ttk.Label(cadre_general, text=f"Nombre total de livres : {stats['total_livres']}",
                  font=("Arial", 12)).pack(anchor="w", pady=5)
        ttk.Label(cadre_general, text=f"Nombre d'exemplaires disponibles : {stats['exemplaires_disponibles']}",
                  font=("Arial", 12)).pack(anchor="w", pady=5)
        ttk.Label(cadre_general, text=f"Nombre d'emprunts en cours : {stats['emprunts_cours']}",
                  font=("Arial", 12)).pack(anchor="w", pady=5)

        cadre_populaires = ttk.LabelFrame(self.frame, text="Livres les plus empruntés", padding=15)
        cadre_populaires.pack(fill="both", expand=True, pady=5)

        if stats['livres_populaires']:
            for i, (titre, nb) in enumerate(stats['livres_populaires'], 1):
                ttk.Label(cadre_populaires, text=f"{i}. {titre} - {nb} emprunt(s)",
                          font=("Arial", 11)).pack(anchor="w", pady=3)
        else:
            ttk.Label(cadre_populaires, text="Aucun emprunt enregistré pour le moment",
                      font=("Arial", 11)).pack(anchor="w", pady=3)