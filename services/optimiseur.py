class Optimiseur:

    @staticmethod
    def meilleure_salle(seance, salles):
        salles_valides = []
        for s in salles:
            if s.capacite < seance.groupe.effectif:
                continue
            if seance.cours.equipements:
                ok = all(e in s.equipements for e in seance.cours.equipements)
                if not ok:
                    continue
            salles_valides.append(s)

        if not salles_valides:
            return None

        return min(salles_valides, key=lambda s: s.capacite)

    @staticmethod
    def meilleur_creneau(creneaux, seances, groupe=None):
        best = None
        best_score = None
        for c in creneaux:
            base = 0
            for s in seances:
                if s.creneau.chevauche(c):
                    base += 1
            pref_penalty = 0
            if groupe and hasattr(groupe, "preference"):
                if groupe.preference == "matin":
                    pref_penalty = 0 if c._debut_min < 12 * 60 else 1
                elif groupe.preference == "apres-midi":
                    pref_penalty = 0 if c._debut_min >= 12 * 60 else 1
            score = base + pref_penalty
            if best_score is None or score < best_score:
                best = c
                best_score = score
        return best

    @staticmethod
    def salles_vacantes(creneau, salles, min_capacite=0, equipements=None):
        equipements = equipements or []
        result = []
        for s in salles:
            if s.capacite < min_capacite:
                continue
            if any(e not in s.equipements for e in equipements):
                continue
            if s.est_disponible(creneau):
                result.append(s)
        return result
