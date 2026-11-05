"""Jeux d'essai du TP2 et cas piégés de la soutenance."""

import io
import random
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from grille import Grille
from jeu import jouer_partie
from joueurs import JoueurHumain, JoueurIA, JoueurIAMalin
from main import main


class JoueurProgramme:
    def __init__(self, nom, coups):
        self.nom = nom
        self.coups = iter(coups)
        self.appels = 0

    def prochain_coup(self, tab, symbole):
        self.appels += 1
        return next(self.coups)


class TestsMorpion(unittest.TestCase):
    def test_grille_et_coups_invalides(self):
        g = Grille()
        self.assertTrue(g.jouer(0, 0, "X"))
        self.assertTrue(g.jouer(0, 1, "O"))
        self.assertTrue(g.jouer(1, 1, "X"))
        self.assertFalse(g.jouer(0, 0, "O"))
        for x, y in ((3, 0), (-1, 0), (0, 3), (0, -1), ("0", 2), (True, 2)):
            self.assertFalse(g.jouer(x, y, "O"))
        self.assertFalse(g.jouer(2, 2, "A"))
        self.assertFalse(g.est_gagnant("X"))
        self.assertTrue(g.jouer(2, 2, "X"))
        self.assertTrue(g.est_gagnant("X"))
        self.assertFalse(g.est_plein())
        sortie = io.StringIO()
        with redirect_stdout(sortie):
            g.afficher()
        self.assertIn("X | O |  ", sortie.getvalue())

    def test_huit_lignes_gagnantes(self):
        combinaisons = (
            [[(x, y) for y in range(3)] for x in range(3)]
            + [[(x, y) for x in range(3)] for y in range(3)]
            + [[(i, i) for i in range(3)], [(i, 2 - i) for i in range(3)]]
        )
        self.assertEqual(len(combinaisons), 8)
        for combinaison in combinaisons:
            with self.subTest(combinaison=combinaison):
                g = Grille()
                for x, y in combinaison:
                    self.assertTrue(g.jouer(x, y, "O"))
                self.assertTrue(g.est_gagnant("O"))
                self.assertFalse(g.est_gagnant("X"))

    def test_grille_pleine(self):
        g = Grille()
        for x, ligne in enumerate(("XOX", "XOO", "OXX")):
            for y, symbole in enumerate(ligne):
                g.jouer(x, y, symbole)
        self.assertTrue(g.est_plein())
        self.assertEqual(g.coups_libres(), [])
        self.assertFalse(g.est_gagnant("X"))
        self.assertFalse(g.est_gagnant("O"))

    def test_ia_aleatoire_et_humain(self):
        g = Grille()
        g.jouer(0, 0, "X")
        ia = JoueurIA(generateur=random.Random(7))
        coup = ia.prochain_coup(g, "O")
        self.assertIn(coup, g.coups_libres())
        with patch("builtins.input", side_effect=["abc", "1 2"]), redirect_stdout(io.StringIO()):
            self.assertEqual(JoueurHumain().prochain_coup(g, "X"), (1, 2))

    def test_ia_maline_bloque_et_gagne(self):
        ia = JoueurIAMalin(generateur=random.Random(1))
        g = Grille()
        g.cases = [["X", "X", " "], [" ", "O", " "], [" ", " ", " "]]
        self.assertEqual(ia.prochain_coup(g, "O"), (0, 2))
        self.assertEqual(g.cases[0][2], " ")
        g.cases = [["O", "O", " "], ["X", "X", " "], [" ", " ", " "]]
        self.assertEqual(ia.prochain_coup(g, "O"), (0, 2))
        g.cases = [["O", "O", " "], ["X", "X", " "], [" ", " ", " "]]
        self.assertEqual(ia.prochain_coup(g, "X"), (1, 2))

    def test_coup_refuse_meme_joueur(self):
        x = JoueurProgramme("X", [(3, 0), (-1, 0), (0, 0), (0, 0),
                                   (0, 1), (0, 2)])
        o = JoueurProgramme("O", [(1, 0), (1, 1)])
        sortie = io.StringIO()
        with redirect_stdout(sortie):
            resultat = jouer_partie(x, o)
        self.assertEqual(resultat, "X")
        self.assertEqual(x.appels, 6)
        self.assertEqual(o.appels, 2)
        self.assertEqual(sortie.getvalue().count("Coup invalide"), 3)

    def test_vingt_parties_ia(self):
        resultats = [jouer_partie(
            JoueurIA("X", random.Random(i)),
            JoueurIA("O", random.Random(i + 100)), afficher=False)
            for i in range(20)]
        self.assertEqual(len(resultats), 20)
        self.assertTrue(all(r in ("X", "O", "Nul") for r in resultats))

    def test_menu_et_scores(self):
        sortie = io.StringIO()
        with patch("builtins.input", side_effect=["9", "3", "4", "5"]), redirect_stdout(sortie):
            main()
        self.assertIn("Choix invalide", sortie.getvalue())
        self.assertIn("20 parties terminées", sortie.getvalue())
        self.assertIn("Scores depuis le lancement", sortie.getvalue())


if __name__ == "__main__":
    unittest.main()
