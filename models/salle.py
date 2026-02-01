class Salle:
    def __init__(self, nom, capacite, equipements, bloquees=None):
        self.nom = nom
        self.capacite = capacite
        self.equipements = equipements
        self.occupees = []
        self.bloquees = bloquees or []

    def est_disponible(self, creneau):
        for c in self.occupees:
            if c.chevauche(creneau):
                return False
        for b in self.bloquees:
            if b.chevauche(creneau):
                return False
        return True

    def reserver(self, creneau):
        self.occupees.append(creneau)
