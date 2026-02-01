from models.utilisateur import Utilisateur

class Administrateur(Utilisateur):
    def __init__(self, id, nom):
        super().__init__(id, nom)

    def generer_edt(self, generateur, cours, salles, groupes):
        return generateur.generer(cours, salles, groupes)