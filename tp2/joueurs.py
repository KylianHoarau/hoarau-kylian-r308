"""Joueurs interchangeables grâce à prochain_coup(tab, symbole)."""

import random

from grille import Grille


def cases_de(tab):
    """Accepte une Grille ou sa liste de listes pour les jeux d'essai."""
    return tab.cases if isinstance(tab, Grille) else tab


def coups_libres(tab):
    cases = cases_de(tab)
    return [(x, y) for x in range(3) for y in range(3)
            if cases[x][y] == " "]


class JoueurHumain:
    def __init__(self, nom="Humain"):
        self.nom = nom

    def prochain_coup(self, tab, symbole):
        while True:
            saisie = input(f"{self.nom} ({symbole}), ligne colonne (0 à 2) : ").split()
            if len(saisie) == 2:
                try:
                    return int(saisie[0]), int(saisie[1])
                except ValueError:
                    pass
            print("Entrez deux nombres entiers, par exemple : 1 2.")


class JoueurIA:
    def __init__(self, nom="IA", generateur=None):
        self.nom = nom
        self.generateur = generateur or random

    def prochain_coup(self, tab, symbole):
        libres = coups_libres(tab)
        if not libres:
            raise ValueError("Aucun coup possible : la grille est pleine.")
        return self.generateur.choice(libres)
