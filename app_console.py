import json
import os
import webbrowser
from main import generer_edt
from models.creneau import Creneau
from services.optimiseur import Optimiseur

# Global state
SEANCES = []
SALLES = []
CRENEAUX = []

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_data():
    global SEANCES, SALLES, CRENEAUX
    SEANCES, SALLES, CRENEAUX = generer_edt()

def menu_principal():
    while True:
        clear_screen()
        print("=====================================================")
        print("   🎓 GESTION EDT - FST TANGER (LICENCE) 🎓")
        print("=====================================================")
        print("1. 👨‍🎓 Espace ÉTUDIANT")
        print("2. 👨‍🏫 Espace ENSEIGNANT")
        print("3. ⚙️  ADMIN / SYSTÈME (Mise à jour)")
        print("0. Quitter")
        print("=====================================================")
        choix = input("Votre choix : ")

        if choix == "1":
            menu_etudiant()
        elif choix == "2":
            menu_enseignant()
        elif choix == "3":
            load_data()
            input("\nAppuyez sur Entrée pour continuer...")
        elif choix == "0":
            break

def menu_etudiant():
    while True:
        clear_screen()
        print("--- 👨‍🎓 ESPACE ÉTUDIANT ---")
        print("1. Consulter mon emploi du temps (HTML/PDF)")
        print("2. Rechercher une salle libre pour révision")
        print("0. Retour")
        choix = input("Choix : ")

        if choix == "1":
            print("\nOuverture de l'emploi du temps...")
            try:
                webbrowser.open("edt_final.html")
                print("Si le navigateur ne s'ouvre pas, ouvrez 'edt_final.html' manuellement.")
            except:
                print("Ouvrez 'edt_final.html' manuellement.")
            input("Appuyez sur Entrée pour continuer...")
        
        elif choix == "2":
            chercher_salle_libre()
        
        elif choix == "0":
            break

def menu_enseignant():
    while True:
        clear_screen()
        print("--- 👨‍🏫 ESPACE ENSEIGNANT ---")
        print("1. Consulter mon planning")
        print("2. Soumettre une demande de réservation (Rattrapage)")
        print("3. Signaler une indisponibilité (Absence)")
        print("0. Retour")
        choix = input("Choix : ")

        if choix == "1":
            print("\nOuverture de l'emploi du temps...")
            webbrowser.open("edt_final.html")
            input("Appuyez sur Entrée pour continuer...")

        elif choix == "2":
            ajouter_reservation()
        
        elif choix == "3":
            ajouter_indisponibilite()
        
        elif choix == "0":
            break

def chercher_salle_libre():
    print("\n--- 🔍 Recherche Salle Libre ---")
    jour = input("Jour (Lundi, Mardi, Mercredi, Jeudi, Vendredi) : ").capitalize()
    heure_debut = input("Heure début (HH:MM, ex: 10:30) : ")
    heure_fin = input("Heure fin (HH:MM, ex: 12:30) : ")
    
    try:
        creneau = Creneau(jour, heure_debut, heure_fin)
        vacantes = Optimiseur.salles_vacantes(creneau, SALLES)
        
        print(f"\n✅ Salles disponibles le {jour} de {heure_debut} à {heure_fin} :")
        if vacantes:
            for s in vacantes:
                print(f" - {s.nom} (Cap: {s.capacite}, Equip: {', '.join(s.equipements)})")
        else:
            print("❌ Aucune salle disponible sur ce créneau.")
    except Exception as e:
        print(f"Erreur : {e}")
    
    input("\nAppuyez sur Entrée pour continuer...")

def ajouter_reservation():
    print("\n--- 📅 Nouvelle Réservation ---")
    print("Exemple: Dr. Khalid / IDAI / Rattrapage Java / TP")
    enseignant = input("Nom Enseignant (ex: Dr. Khalid) : ")
    groupe = input("Groupe (ex: IDAI, AD...) : ")
    cours = input("Intitulé du cours : ")
    type_cours = input("Type (CM, TD, TP) : ")
    jour = input("Jour : ").capitalize()
    debut = input("Début (HH:MM) : ")
    fin = input("Fin (HH:MM) : ")
    salle = input("Salle souhaitée (ex: Salle F11) : ")

    nouvelle_res = {
        "cours": cours,
        "enseignant": enseignant,
        "groupe": groupe,
        "type": type_cours,
        "jour": jour,
        "debut": debut,
        "fin": fin,
        "salle": salle
    }

    try:
        with open("data/reservations.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        data.append(nouvelle_res)
        with open("data/reservations.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("✅ Demande enregistrée ! Mise à jour du système en cours...")
        load_data() # Regenerate
    except Exception as e:
        print(f"Erreur: {e}")
    
    input("\nAppuyez sur Entrée pour continuer...")

def ajouter_indisponibilite():
    print("\n--- 🚫 Signaler Indisponibilité ---")
    enseignant = input("Nom Enseignant (ex: Mme. Aicha) : ")
    jour = input("Jour : ").capitalize()
    debut = input("Début (HH:MM) : ")
    fin = input("Fin (HH:MM) : ")

    nouvelle_indispo = {
        "enseignant": enseignant,
        "jour": jour,
        "debut": debut,
        "fin": fin
    }

    try:
        with open("data/indisponibilites.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        data.append(nouvelle_indispo)
        with open("data/indisponibilites.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("✅ Indisponibilité enregistrée ! Recalcul de l'emploi du temps en cours...")
        load_data() # Regenerate
    except Exception as e:
        print(f"Erreur: {e}")
    
    input("\nAppuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    # Initial load
    load_data()
    menu_principal()
