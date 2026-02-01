from models.utilisateur import Utilisateur

class Etudiant(Utilisateur):
    def __init__(self, id, nom, filiere='', groupe=''):
        super().__init__(id, nom)
        self.filiere = filiere
        self.groupe = groupe

    def get_filiere(self):
        return self.filiere

    def get_groupe(self):
        return self.groupe

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.nom,
            'filiere': self.filiere,
            'group': self.groupe
        }
