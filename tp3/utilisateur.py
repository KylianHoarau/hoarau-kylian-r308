"""Gestion des emprunts d'un utilisateur."""


class Utilisateur:
    def __init__(self, nom, limite_emprunts=3):
        if not nom.strip():
            raise ValueError("Le nom est obligatoire.")
        if limite_emprunts < 1:
            raise ValueError("La limite doit être positive.")
        self.nom = nom.strip()
        self.emprunts = []
        self.limite_emprunts = limite_emprunts

    def emprunter_livre(self, livre):
        if len(self.emprunts) >= self.limite_emprunts or livre in self.emprunts:
            return False
        if not livre.emprunter(self.nom):
            return False
        self.emprunts.append(livre)
        return True

    def rendre_livre(self, livre):
        if livre not in self.emprunts or livre.emprunteur != self.nom:
            return False
        if not livre.rendre():
            return False
        self.emprunts.remove(livre)
        return True

    def afficher_emprunts(self):
        print(f"Emprunts de {self.nom} :")
        if not self.emprunts:
            print("Aucun emprunt.")
        for livre in self.emprunts:
            livre.afficher()
