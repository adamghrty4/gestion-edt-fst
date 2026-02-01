class Seance:
    def __init__(self, cours, groupe, enseignant, creneau):
        self.cours = cours
        self.groupe = groupe
        self.enseignant = enseignant
        self.creneau = creneau
        self.salle = None

    def est_valide(self):
        return (
            self.salle is not None and
            self.enseignant.est_disponible(self.creneau)
        )