# Projet-Tkinter
# 📚 Bibliothèque - Système de Gestion

## 📝 Description

Application de bureau développée en Python pour la gestion complète d'une bibliothèque.  
Elle permet aux bibliothécaires de gérer les livres, les membres abonnés et les emprunts via une interface graphique conviviale Tkinter.

## 🎯 Fonctionnalités implémentées

### 📖 Gestion des livres
- ✅ Ajouter un nouveau livre (titre, auteur, genre, année, nombre d'exemplaires)
- ✅ Modifier les informations d'un livre existant
- ✅ Supprimer un livre (uniquement s'il n'a aucun emprunt en cours)
- ✅ Rechercher un livre par titre ou auteur
- ✅ Afficher la liste complète des livres dans un tableau

### 👥 Gestion des membres
- ✅ Enregistrer un nouveau membre (nom, prénom, email, numéro d'adhésion)
- ✅ Modifier les informations d'un membre
- ✅ Supprimer un membre (uniquement sans emprunt en cours)
- ✅ Rechercher un membre par nom ou numéro d'adhésion
- ✅ Afficher tous les membres dans un tableau

### 🔄 Gestion des emprunts
- ✅ Enregistrer un nouvel emprunt avec vérification :
  - Vérifier qu'il reste des exemplaires disponibles
  - Vérifier que le membre n'a pas déjà ce livre non rendu
- ✅ Date d'emprunt automatique (date du jour)
- ✅ Date de retour prévue automatique (+14 jours)
- ✅ Enregistrer le retour d'un livre
- ✅ Rechercher des emprunts par titre ou nom de membre
- ✅ Afficher tous les emprunts avec leur statut (En cours / Rendu)

### 📊 Statistiques (Bonus)
- ✅ Nombre total de livres en stock
- ✅ Nombre d'exemplaires disponibles
- ✅ Nombre d'emprunts en cours
- ✅ Liste des 5 livres les plus empruntés

## 🛠️ Technologies utilisées

| Technologie | Rôle |
|-------------|------|
| **Python 3.x** | Langage de programmation principal |
| **Tkinter** | Interface graphique (GUI) |
| **SQLite3** | Base de données locale |
| **ttk** | Widgets modernes pour Tkinter |

## 📁 Structure du projet

bibliotheque_app/
│
├── main.py # Point d'entrée de l'application
├── database.py # Gestion de la base de données SQLite
├── gui_livres.py # Interface de gestion des livres
├── gui_membres.py # Interface de gestion des membres
├── gui_emprunts.py # Interface de gestion des emprunts
├── gui_statistiques.py # Interface des statistiques (bonus)
└── bibliotheque.db # Base de données (créée automatiquement)

## 🚀 Installation et exécution

### Prérequis
- Python 3.6 ou supérieur
- Tkinter (inclus par défaut avec Python)
