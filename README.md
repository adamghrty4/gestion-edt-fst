# Gestion EDT - FST Tanger (Licence)

Ce projet est une application Python permettant de générer, gérer et visualiser les emplois du temps pour les filières de Licence de la **FST Tanger** (Université Abdelmalek Essaâdi).

Il a été conçu pour être **réaliste**, **sans serveur (serverless)** et **interactif**.

## 🚀 Fonctionnalités

*   **Génération Automatique** : Algorithme d'optimisation pour placer les cours sans conflits (Salles, Professeurs, Groupes).
*   **Données Réalistes** : Gestion de 5 filières (AD, IDAI, GI, ENR, MIP), enseignants, et salles équipées.
*   **Interface Web Interactive** : Export HTML autonome (`edt_final.html`) avec filtres dynamiques (Enseignant, Groupe, Salle).
*   **Système de Réservation** : Permet aux enseignants de demander des réservations ponctuelles via la console.
*   **Gestion des Indisponibilités** : Prise en compte des absences et réajustement automatique du planning.
*   **Exports** : PDF (via impression navigateur), CSV et JSON.

## 📂 Structure du Projet

*   `app_console.py` : **Point d'entrée principal**. Menu interactif pour simuler les rôles (Étudiant, Prof, Admin).
*   `main.py` : Moteur de génération de l'emploi du temps.
*   `data/` : Fichiers JSON contenant les données (cours, profs, salles, etc.).
*   `models/` : Classes Python (Cours, Enseignant, Salle...).
*   `services/` : Logique métier (Optimiseur, Détecteur de conflits, Exportateur).
*   `edt_final.html` : L'emploi du temps généré (Visualisation).

## 🛠️ Installation

1.  **Cloner le projet** (ou télécharger les fichiers) :
    ```bash
    git clone https://github.com/votre-user/project_python_FM.git
    cd project_python_FM
    ```

2.  **Créer un environnement virtuel (recommandé)** :
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Mac/Linux
    source .venv/bin/activate
    ```

3.  **Installer les dépendances** :
    ```bash
    pip install -r requirements.txt
    ```

## ▶️ Utilisation

Lancez l'application console pour accéder au menu principal :

```bash
python app_console.py
```

Vous aurez accès à 3 espaces :
1.  **Espace Étudiant** : Consulter son EDT, chercher une salle libre.
2.  **Espace Enseignant** : Consulter son planning, réserver une salle, signaler une absence.
3.  **Admin / Système** : Régénérer les données manuellement.

## 👤 Auteurs

Projet réalisé dans le cadre du module Python.
