class Utilisateur:
    def __init__(self, id, nom):
        self.id = id
        self.nom = nom

    def __str__(self):
        return f"{self.nom}"