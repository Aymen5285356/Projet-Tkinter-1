import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from gui_livres import GestionLivres
from gui_membres import GestionMembres
from gui_emprunts import GestionEmprunts
from gui_statistiques import GestionStatistiques

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Bibliothèque - Système de Gestion")
        self.root.geometry("1100x700")
        self.appliquer_style()
        self.db = Database()
        self.creer_menu()
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)
        self.frame_livres = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_livres, text="Livres")
        self.gestion_livres = GestionLivres(self.frame_livres, self.db)
        self.frame_membres = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_membres, text="Membres")
        self.gestion_membres = GestionMembres(self.frame_membres, self.db)
        self.frame_emprunts = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_emprunts, text="Emprunts")
        self.gestion_emprunts = GestionEmprunts(self.frame_emprunts, self.db)
        self.frame_statistiques = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_statistiques, text="Statistiques")
        self.gestion_statistiques = GestionStatistiques(self.frame_statistiques, self.db)
        self.status_bar = ttk.Label(root, text="Prêt", relief="sunken")
        self.status_bar.pack(side="bottom", fill="x")
        self.root.protocol("WM_DELETE_WINDOW", self.fermer_application)

        messagebox.showinfo("Bienvenue", "Bienvenue dans le système de gestion de bibliothèque")

    def appliquer_style(self):
        """Appliquer le style personnalisé selon les couleurs du cahier des charges"""
        style = ttk.Style()

        self.root.configure(bg='#F2F2F2')

        style.configure("TButton", background="#2E86C1", foreground="#333333", padding=6)
        style.map("TButton", background=[("active", "#2874A6")])
        style.configure("TLabel", background="#F2F2F2", foreground="#333333")
        style.configure("TLabelframe", background="#FFFFFF", foreground="#333333")
        style.configure("TLabelframe.Label", background="#FFFFFF", foreground="#333333")

    def creer_menu(self):
        """Créer la barre de menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        fichier_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Fichier", menu=fichier_menu)
        fichier_menu.add_command(label="Exporter les données (CSV)", command=self.exporter_csv)
        fichier_menu.add_separator()
        fichier_menu.add_command(label="Quitter", command=self.fermer_application)
        aide_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Aide", menu=aide_menu)
        aide_menu.add_command(label="À propos", command=self.a_propos)
        aide_menu.add_command(label="Aide", command=self.aide)

    def exporter_csv(self):
        """Exporter les données en CSV (bonus)"""
        messagebox.showinfo("Information", "Fonctionnalité à implémenter\nExport CSV")

    def a_propos(self):
        """Afficher la fenêtre À propos"""
        messagebox.showinfo("À propos",
                            "Système de gestion de bibliothèque\nVersion 1.0\n\n"
                            "Développé dans le cadre du projet de stage\n"
                            "Filière: Développement Digital\n"
                            "Année: 2025/2026")

    def aide(self):
        """Afficher l'aide"""
        messagebox.showinfo("Aide",
                            "Guide rapide:\n\n"
                            "Livres: Ajoutez, modifiez ou supprimez des livres\n"
                            "Membres: Gérez les membres abonnés\n"
                            "Emprunts: Enregistrez les emprunts et retours\n"
                            "Statistiques: Consultez les statistiques de la bibliothèque\n\n"
                            "Note: Un livre ne peut être supprimé s'il est emprunté\n"
                            "Un membre ne peut être supprimé s'il a des emprunts en cours")

    def fermer_application(self):
        """Fermer proprement l'application"""
        if messagebox.askyesno("Quitter", "Voulez-vous vraiment quitter l'application ?"):
            self.db.close()
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()