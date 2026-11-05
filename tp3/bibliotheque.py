"""Catalogue et utilisateurs, indexés par titre et par nom."""

from livre import Livre
from utilisateur import Utilisateur


class Bibliotheque:
    def __init__(self):
        self.livres = {}
        self.utilisateurs = {}

    def ajouter_livre(self, livre):
        if livre.titre in self.livres:
            return False
        self.livres[livre.titre] = livre
        return True

    def ajouter_utilisateur(self, utilisateur):
        if utilisateur.nom in self.utilisateurs:
            return False
        self.utilisateurs[utilisateur.nom] = utilisateur
        return True

    def emprunter(self, nom, titre):
        utilisateur = self.utilisateurs.get(nom)
        livre = self.livres.get(titre)
        return bool(utilisateur and livre and utilisateur.emprunter_livre(livre))

    def rendre(self, nom, titre):
        utilisateur = self.utilisateurs.get(nom)
        livre = self.livres.get(titre)
        return bool(utilisateur and livre and utilisateur.rendre_livre(livre))

    def afficher_livres(self):
        for disponible, rubrique in ((True, "Disponibles"), (False, "Empruntés")):
            print(f"\n{rubrique} :")
            selection = [l for l in self.livres.values() if l.disponible == disponible]
            if not selection:
                print("Aucun livre.")
            for livre in selection:
                livre.afficher()
