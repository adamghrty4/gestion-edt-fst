class Cours:
    def __init__(self, nom, enseignant, type_seance, equipements=None, filiere=None, semestre=None):
        self.nom = nom
        self.enseignant = enseignant
        self.type_seance = type_seance
        self.equipements = equipements or []
        self.filiere = filiere
        self.semestre = semestre
