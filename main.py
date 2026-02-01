from services.chargeur_donnees import ChargeurDonnees
import json
from models.cours import Cours
from models.groupe import Groupe
from models.seance import Seance
from models.creneau import Creneau
from services.detecteur_conflits import DetecteurConflits
from services.optimiseur import Optimiseur
from services.exportateur import Exportateur

def generer_edt():
    print("🔄 Chargement des données et génération de l'emploi du temps...")
    # 1️⃣ Charger toutes les données
    # -----------------------------
    salles = ChargeurDonnees.charger_salles("data/salles.json")
    enseignants = ChargeurDonnees.charger_enseignants("data/enseignants.json")
    # Merge indisponibilités externes si fichier présent
    try:
        with open("data/indisponibilites.json", "r", encoding="utf-8") as f:
            indispos_ext = json.load(f)
        for ent in enseignants:
            for b in indispos_ext:
                if b.get("enseignant") == ent.nom:
                    ent.indisponibilites.append(Creneau(b["jour"], b["debut"], b["fin"]))
    except FileNotFoundError:
        pass
    groupes = ChargeurDonnees.charger_groupes("data/groupes.json")
    creneaux = ChargeurDonnees.charger_creneaux("data/creneaux.json")
    cours_input = ChargeurDonnees.charger_cours("data/cours.json")
    with open("data/type_requirements.json", "r", encoding="utf-8") as f:
        type_requirements = json.load(f)

    # Créer objets Cours
    cours_objs = []
    for c in cours_input:
        enseignant_obj = next(e for e in enseignants if e.id == c['enseignant_id'])
        eq = c.get('equipements', type_requirements.get(c['type'], []))
        cours_objs.append(Cours(c['nom'], enseignant_obj, c['type'], eq, c.get('filiere'), c.get('semestre')))

    # -----------------------------
    # 2️⃣ Générer EDT pour tous les groupes
    # -----------------------------
    seances_planifiees = []

    for c in cours_objs:
        for g in groupes:
            if c.filiere and g.nom != c.filiere:
                continue
            candidats = [cr for cr in creneaux if c.enseignant.est_disponible(cr)]
            if not candidats:
                continue
            choisi = Optimiseur.meilleur_creneau(candidats, seances_planifiees, g)
            essai = [choisi] + [cr for cr in candidats if cr != choisi]
            for cr in essai:
                seance = Seance(c, g, c.enseignant, cr)
                salle = Optimiseur.meilleure_salle(seance, salles)
                if salle and DetecteurConflits.seance_valide(seance, salle, seances_planifiees):
                    seance.salle = salle
                    salle.reserver(cr)
                    seances_planifiees.append(seance)
                    break

    # Traiter les réservations ponctuelles si présentes
    try:
        with open("data/reservations.json", "r", encoding="utf-8") as f:
            reservations = json.load(f)
        for r in reservations:
            enseignant_obj = next((e for e in enseignants if e.nom == r.get("enseignant")), None)
            groupe_obj = next((g for g in groupes if g.nom == r.get("groupe")), None)
            salle_obj = next((s for s in salles if s.nom == r.get("salle")), None)
            cr = Creneau(r["jour"], r["debut"], r["fin"])
            if enseignant_obj and groupe_obj and salle_obj:
                cours_res = Cours(r["cours"], enseignant_obj, r.get("type", "CM"), [], groupe_obj.nom, None)
                seance = Seance(cours_res, groupe_obj, enseignant_obj, cr)
                # Note: On force un peu la réservation si possible, mais on vérifie quand même les conflits majeurs
                if salle_obj and DetecteurConflits.seance_valide(seance, salle_obj, seances_planifiees):
                    seance.salle = salle_obj
                    salle_obj.reserver(cr)
                    seances_planifiees.append(seance)
                    print(f"➕ Réservation ajoutée: {cr} | {seance.cours.nom} | {groupe_obj.nom} | {salle_obj.nom}")
                else:
                    print(f"⚠️ Impossible d'ajouter la réservation: {r['cours']} (Conflit)")
    except FileNotFoundError:
        pass

    # -----------------------------
    # 3️⃣ Exporter l'emploi du temps
    # -----------------------------
    Exportateur.exporter(seances_planifiees, "edt_final.json")
    Exportateur.exporter_csv(seances_planifiees, "edt_final.csv")
    Exportateur.exporter_html(seances_planifiees, "edt_final.html")
    print("✅ EDT FST Tanger généré et exporté (edt_final.html) !")
    return seances_planifiees, salles, creneaux

if __name__ == "__main__":
    generer_edt()
