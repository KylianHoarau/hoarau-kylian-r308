"""Modèle d'un livre de la bibliothèque."""


class Livre:
    def __init__(self, titre, auteur, annee, disponible=True, emprunteur=None):
        if not titre.strip() or not auteur.strip():
            raise ValueError("Le titre et l'auteur sont obligatoires.")
        self.titre = titre.strip()
        self.auteur = auteur.strip()
        self.annee = int(annee)
        self.disponible = disponible
        self.emprunteur = None if disponible else emprunteur
        if not disponible and not emprunteur:
            raise ValueError("Un livre emprunté doit avoir un emprunteur.")

    def afficher(self):
        etat = "disponible" if self.disponible else f"emprunté par {self.emprunteur}"
        print(f"{self.titre} - {self.auteur} ({self.annee}) : {etat}")

    def emprunter(self, nom):
        if not self.disponible or not nom.strip():
            return False
        self.disponible = False
        self.emprunteur = nom.strip()
        return True

    def rendre(self):
        if self.disponible:
            return False
        self.disponible = True
        self.emprunteur = None
        return True
