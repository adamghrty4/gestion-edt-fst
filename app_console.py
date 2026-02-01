import json
import os
import webbrowser
from main import generer_edt
from models.creneau import Creneau
from services.optimiseur import Optimiseur
 
def _normalize_salle_name(nom_salle):
    try:
        with open("data/salles.json", "r", encoding="utf-8") as f:
            salles = json.load(f)
        # Exact match
        for s in salles:
            if s.get("nom", "").strip().lower() == nom_salle.strip().lower():
                return s["nom"]
        # Suffix/contains match (ex: "F11" -> "Salle F11")
        for s in salles:
            full = s.get("nom", "").strip().lower()
            token = nom_salle.strip().lower()
            if token and (full.endswith(token) or token in full):
                return s["nom"]
    except:
        pass
    return nom_salle

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
            menu_admin()
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
        # Envoyer dans la file d'attente admin
        filepath = "data/demandes_reservations.json"
        if not os.path.exists(filepath):
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump([], f)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        data.append(nouvelle_res)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("✅ Demande envoyée à l'administrateur pour validation !")
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

def menu_admin():
    while True:
        clear_screen()
        print("--- ⚙️  ESPACE ADMINISTRATEUR ---")
        print("1. 🔄 Forcer la mise à jour de l'EDT (Régénérer)")
        print("2. 📊 Voir les statistiques globales")
        print("3. ✅ Gérer les demandes de réservation en attente")
        print("4. 🗑️  Réinitialiser les données (Réservations/Indispos)")
        print("0. Retour")
        choix = input("Choix : ")

        if choix == "1":
            load_data()
            input("\nAppuyez sur Entrée pour continuer...")
        elif choix == "2":
            afficher_statistiques()
        elif choix == "3":
            gerer_demandes()
        elif choix == "4":
            reset_data()
        elif choix == "0":
            break

def gerer_demandes():
    print("\n--- ✅ Validation des Demandes ---")
    try:
        filepath = "data/demandes_reservations.json"
        if not os.path.exists(filepath):
            print("Aucune demande en attente.")
            input("Entrée...")
            return

        with open(filepath, "r", encoding="utf-8") as f:
            demandes = json.load(f)
        
        if not demandes:
            print("Aucune demande en attente.")
            input("Entrée...")
            return

        print(f"Il y a {len(demandes)} demande(s) en attente.")
        for i, d in enumerate(demandes):
            print(f"\n[{i+1}] {d['enseignant']} - {d['cours']} ({d['type']})")
            print(f"    📅 {d['jour']} : {d['debut']} -> {d['fin']} | Salle: {d['salle']}")
            
            action = input("    👉 Action (v=Valider, r=Rejeter, i=Ignorer) : ").lower()
            
            if action == 'v':
                # Move to reservations.json
                # Normalize salle name to match data set
                d["salle"] = _normalize_salle_name(d.get("salle", ""))
                with open("data/reservations.json", "r", encoding="utf-8") as f:
                    res_data = json.load(f)
                res_data.append(d)
                with open("data/reservations.json", "w", encoding="utf-8") as f:
                    json.dump(res_data, f, indent=4, ensure_ascii=False)
                print("    ✅ Validée.")
                demandes[i] = None # Mark for removal
            
            elif action == 'r':
                print("    ❌ Rejetée.")
                demandes[i] = None # Mark for removal
            
            else:
                print("    ➡️ Ignorée.")

        # Cleanup processed requests
        demandes = [d for d in demandes if d is not None]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(demandes, f, indent=4, ensure_ascii=False)
            
        print("\nTraitement terminé. Mise à jour du système...")
        load_data()

    except Exception as e:
        print(f"Erreur : {e}")
    
    input("\nAppuyez sur Entrée pour continuer...")

def afficher_statistiques():
    print("\n--- 📊 Statistiques de l'Emploi du Temps ---")
    if not SEANCES:
        print("⚠️ Aucune donnée chargée. Veuillez d'abord générer l'EDT.")
        input("Appuyez sur Entrée...")
        return

    try:
        with open("data/cours.json", "r", encoding="utf-8") as f:
            cours_data = json.load(f)
        total_cours = len(cours_data)
    except:
        total_cours = 0

    nb_seances = len(SEANCES)
    taux = 0
    if total_cours > 0:
        taux = (nb_seances / total_cours) * 100
    
    print(f"Nombre de cours total (Data) : {total_cours}")
    print(f"Nombre de séances planifiées : {nb_seances}")
    print(f"Taux de couverture : {taux:.1f}%")
    
    salles_utilisees = set(s.salle.nom for s in SEANCES if s.salle)
    print(f"Salles utilisées : {len(salles_utilisees)} / {len(SALLES)}")
    
    # Calcul Taux d'Occupation
    print("\n--- Occupation des Salles (Top 5) ---")
    occupation = {}
    for s in SEANCES:
        if s.salle:
            nom = s.salle.nom
            # Estimation durée (2h par défaut si calcul complexe)
            duree = 2 
            try:
                h_debut = int(s.creneau.debut.split(':')[0])
                h_fin = int(s.creneau.fin.split(':')[0])
                duree = h_fin - h_debut
            except:
                pass
            occupation[nom] = occupation.get(nom, 0) + duree

    # Tri par occupation décroissante
    sorted_salles = sorted(occupation.items(), key=lambda x: x[1], reverse=True)[:5]
    for salle, heures in sorted_salles:
        # Taux basé sur 50h/semaine (5 jours * 10h)
        taux_salle = (heures / 50) * 100
        print(f" - {salle} : {heures}h ({taux_salle:.0f}%)")

    input("\nAppuyez sur Entrée pour continuer...")

def reset_data():
    print("\n--- 🗑️ Réinitialisation ---")
    confirm = input("⚠️ Êtes-vous sûr de vouloir supprimer toutes les réservations et indisponibilités ajoutées ? (o/n) : ")
    if confirm.lower() == 'o':
        try:
            with open("data/reservations.json", "w", encoding="utf-8") as f:
                json.dump([], f)
            with open("data/indisponibilites.json", "w", encoding="utf-8") as f:
                json.dump([], f)
            print("✅ Données remises à zéro.")
            load_data()
        except Exception as e:
            print(f"Erreur : {e}")
    input("\nAppuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    # Initial load
    load_data()
    menu_principal()
