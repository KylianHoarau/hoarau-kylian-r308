"""Grille de morpion 3 × 3. Les coordonnées sont (ligne, colonne)."""


class Grille:
    TAILLE = 3

    def __init__(self):
        self.cases = [[" " for _ in range(self.TAILLE)] for _ in range(self.TAILLE)]

    def afficher(self):
        lignes = [" | ".join(ligne) for ligne in self.cases]
        print(("\n" + "---------" + "\n").join(lignes))

    def jouer(self, x, y, joueur):
        """Place X ou O ; renvoie False si le coup est invalide."""
        if joueur not in ("X", "O"):
            return False
        if not isinstance(x, int) or isinstance(x, bool):
            return False
        if not isinstance(y, int) or isinstance(y, bool):
            return False
        if not (0 <= x < self.TAILLE and 0 <= y < self.TAILLE):
            return False
        if self.cases[x][y] != " ":
            return False
        self.cases[x][y] = joueur
        return True

    def est_gagnant(self, joueur):
        if joueur not in ("X", "O"):
            return False
        c = self.cases
        return (any(all(c[x][y] == joueur for y in range(3)) for x in range(3))
                or any(all(c[x][y] == joueur for x in range(3)) for y in range(3))
                or all(c[i][i] == joueur for i in range(3))
                or all(c[i][2 - i] == joueur for i in range(3)))

    def est_plein(self):
        return all(case != " " for ligne in self.cases for case in ligne)

    def coups_libres(self):
        return [(x, y) for x in range(3) for y in range(3)
                if self.cases[x][y] == " "]
