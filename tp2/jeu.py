"""Une partie complète de morpion."""

from grille import Grille


def jouer_partie(joueur_x, joueur_o, afficher=True):
    """Renvoie 'X', 'O' ou 'Nul'. Un coup refusé ne change pas le joueur."""
    grille = Grille()
    joueurs = {"X": joueur_x, "O": joueur_o}
    symbole = "X"
    while True:
        if afficher:
            print()
            grille.afficher()
        x, y = joueurs[symbole].prochain_coup(grille, symbole)
        if not grille.jouer(x, y, symbole):
            if afficher:
                print("Coup invalide : case occupée ou hors grille. Réessayez.")
            continue
        if afficher:
            print(f"{joueurs[symbole].nom} joue en ({x}, {y}).")
        if grille.est_gagnant(symbole):
            if afficher:
                grille.afficher()
                print(f"Victoire de {joueurs[symbole].nom} ({symbole}) !")
            return symbole
        if grille.est_plein():
            if afficher:
                grille.afficher()
                print("Match nul !")
            return "Nul"
        symbole = "O" if symbole == "X" else "X"
