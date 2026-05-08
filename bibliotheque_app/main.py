# main.py
import tkinter as tk
from database import Database
from gui_livres import LivresGUI
from gui_membres import MembresGUI
from gui_emprunts import EmpruntsGUI
from gui_statistiques import StatistiquesGUI

BG_MAIN = "#F2F2F2"
BG_SECTION = "#FFFFFF"
TEXT_PRIMARY = "#333333"
BTN_PRIMARY_BG = "#2E86C1"
BTN_TEXT = "#FFFFFF"

class LibraryApp:
    def __init__(self, root):
        self.db = Database()
        self.root = root
        self.root.title("Bibliothèque - Gestion des Emprunts")
        self.root.geometry("1200x700")
        self.root.configure(bg=BG_MAIN)

        self.create_header()
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=(0,20))

        self.livres_frame = ttk.Frame(self.notebook)
        self.membres_frame = ttk.Frame(self.notebook)
        self.emprunts_frame = ttk.Frame(self.notebook)
        self.stats_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.livres_frame, text="Livres")
        self.notebook.add(self.membres_frame, text="Membres")
        self.notebook.add(self.emprunts_frame, text="Emprunts")
        self.notebook.add(self.stats_frame, text="Statistiques")

        self.livres_gui = LivresGUI(self.livres_frame, self.db)
        self.membres_gui = MembresGUI(self.membres_frame, self.db)
        self.emprunts_gui = EmpruntsGUI(self.emprunts_frame, self.db)
        self.stats_gui = StatistiquesGUI(self.stats_frame, self.db)

    def create_header(self):
        header_frame = tk.Frame(self.root, bg=BTN_PRIMARY_BG, height=80)
        header_frame.pack(fill='x', pady=(0,20))
        header_frame.pack_propagate(False)

        logo_label = tk.Label(header_frame, text="📚 BIBLIOTHÈQUE", font=('Arial', 24, 'bold'), fg=BTN_TEXT, bg=BTN_PRIMARY_BG)
        logo_label.pack(side='left', padx=30, pady=20)

        placeholder_logo = tk.Label(header_frame, text="[LOGO]", font=('Arial', 14), fg=BTN_TEXT, bg=BTN_PRIMARY_BG)
        placeholder_logo.pack(side='right', padx=30, pady=20)

if __name__ == "__main__":
    from tkinter import ttk
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()