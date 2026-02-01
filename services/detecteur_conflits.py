class DetecteurConflits:

    @staticmethod
    def conflit_salle(seance, salle):
        return not salle.est_disponible(seance.creneau)

    @staticmethod
    def conflit_enseignant(seance):
        return not seance.enseignant.est_disponible(seance.creneau)

    @staticmethod
    def conflit_groupe(seance, seances_planifiees):
        for s in seances_planifiees:
            if (
                s.groupe == seance.groupe and
                s.creneau.chevauche(seance.creneau)
            ):
                return True
        return False

    @staticmethod
    def conflit_enseignant_planifie(seance, seances_planifiees):
        for s in seances_planifiees:
            if (
                s.enseignant == seance.enseignant and
                s.creneau.chevauche(seance.creneau)
            ):
                return True
        return False

    @staticmethod
    def seance_valide(seance, salle, seances_planifiees):
        if DetecteurConflits.conflit_salle(seance, salle):
            return False
        if DetecteurConflits.conflit_enseignant(seance):
            return False
        if DetecteurConflits.conflit_groupe(seance, seances_planifiees):
            return False
        if DetecteurConflits.conflit_enseignant_planifie(seance, seances_planifiees):
            return False
        return True
