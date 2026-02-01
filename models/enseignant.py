from models.utilisateur import Utilisateur

class Enseignant(Utilisateur):
    def __init__(self, id, nom, disponibilites, indisponibilites=None):
        super().__init__(id, nom)
        self.disponibilites = disponibilites
        self.indisponibilites = indisponibilites or []

    def est_disponible(self, creneau):
        for b in self.indisponibilites:
            if b.chevauche(creneau):
                return False
        if not self.disponibilites:
            return True
        for c in self.disponibilites:
            if c.jour == creneau.jour and c._debut_min <= creneau._debut_min and c._fin_min >= creneau._fin_min:
                return True
        return False
