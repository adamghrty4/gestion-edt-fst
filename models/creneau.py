class Creneau:
    def __init__(self, jour, debut, fin):
        self.jour = jour
        self.debut = debut
        self.fin = fin
        self._debut_min = int(debut[:2]) * 60 + int(debut[3:5])
        self._fin_min = int(fin[:2]) * 60 + int(fin[3:5])

    def chevauche(self, other):
        if self.jour != other.jour:
            return False
        return not (self._fin_min <= other._debut_min or self._debut_min >= other._fin_min)

    def __eq__(self, other):
        return (
            self.jour == other.jour and
            self.debut == other.debut and
            self.fin == other.fin
        )

    def __str__(self):
        return f"{self.jour} {self.debut}-{self.fin}"
