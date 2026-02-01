import json
from models.salle import Salle
from models.groupe import Groupe
from models.creneau import Creneau
from models.enseignant import Enseignant
from models.cours import Cours
from models.seance import Seance

class ChargeurDonnees:

    @staticmethod
    def charger_salles(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        salles = []
        for s in data:
            bloquees = [Creneau(b["jour"], b["debut"], b["fin"]) for b in s.get("bloquees", [])]
            salles.append(Salle(s["nom"], s["capacite"], s["equipements"], bloquees))
        return salles

    @staticmethod
    def charger_groupes(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        groupes = []
        for g in data:
            grp = Groupe(g["nom"], g["effectif"])
            pref = g.get("preference")
            if pref:
                grp.preference = pref
            groupes.append(grp)
        return groupes

    @staticmethod
    def charger_enseignants(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        enseignants = []
        for e in data:
            disponibilites = [Creneau(d["jour"], d["debut"], d["fin"]) for d in e["disponibilites"]]
            indispo = [Creneau(b["jour"], b["debut"], b["fin"]) for b in e.get("indisponibilites", [])]
            enseignants.append(Enseignant(e["id"], e["nom"], disponibilites, indispo))
        return enseignants

    @staticmethod
    def charger_creneaux(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Creneau(c["jour"], c["debut"], c["fin"]) for c in data]

    @staticmethod
    def charger_cours(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
