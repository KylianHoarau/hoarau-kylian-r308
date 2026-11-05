"""Jeux d'essai de l'énoncé et contrôles de cohérence."""

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from bibliotheque import Bibliotheque
from livre import Livre
from main import main
from utilisateur import Utilisateur


class TestsBibliotheque(unittest.TestCase):
    def setUp(self):
        self.b = Bibliotheque()
        self.l = Livre("1984", "Orwell", 1949)
        self.b.ajouter_livre(self.l)
        self.b.ajouter_utilisateur(Utilisateur("Ana"))
        self.b.ajouter_utilisateur(Utilisateur("Léo"))

    def test_livre(self):
        self.assertTrue(self.l.emprunter("Ana"))
        self.assertFalse(self.l.emprunter("Léo"))
        self.assertTrue(self.l.rendre())
        self.assertFalse(self.l.rendre())
        self.assertIsNone(self.l.emprunteur)

    def test_inconnus_et_mauvais_emprunteur(self):
        self.assertFalse(self.b.emprunter("Inconnu", "1984"))
        self.assertFalse(self.b.emprunter("Ana", "Inconnu"))
        self.assertFalse(self.b.rendre("Inconnu", "1984"))
        self.assertFalse(self.b.rendre("Ana", "Inconnu"))
        self.assertTrue(self.b.emprunter("Ana", "1984"))
        self.assertFalse(self.b.emprunter("Léo", "1984"))
        self.assertFalse(self.b.rendre("Léo", "1984"))
        self.assertEqual(self.l.emprunteur, "Ana")
        self.assertEqual(self.b.utilisateurs["Ana"].emprunts, [self.l])
        self.assertTrue(self.b.rendre("Ana", "1984"))
        self.assertEqual(self.b.utilisateurs["Ana"].emprunts, [])

    def test_doublons(self):
        self.assertFalse(self.b.ajouter_livre(Livre("1984", "Autre", 2000)))
        self.assertFalse(self.b.ajouter_utilisateur(Utilisateur("Ana")))
        self.assertIs(self.b.livres["1984"], self.l)

    def test_limite_et_retour(self):
        for i in range(4):
            self.b.ajouter_livre(Livre(str(i), "Auteur", 2000))
        for i in range(3):
            self.assertTrue(self.b.emprunter("Ana", str(i)))
        self.assertFalse(self.b.emprunter("Ana", "3"))
        self.assertTrue(self.b.livres["3"].disponible)
        self.assertTrue(self.b.rendre("Ana", "0"))
        self.assertTrue(self.b.emprunter("Ana", "3"))

    def test_csv_et_reconstruction(self):
        with tempfile.TemporaryDirectory() as dossier:
            chemin = Path(dossier) / "livres.csv"
            self.b.ajouter_livre(Livre('Titre, avec "guillemets"', "Écrivain", 2020))
            self.b.emprunter("Ana", "1984")
            self.b.sauvegarder(chemin)
            autre = Bibliotheque()
            autre.charger(chemin)
            self.assertFalse(autre.livres["1984"].disponible)
            self.assertEqual(autre.livres["1984"].emprunteur, "Ana")
            self.assertIn("Léo", autre.utilisateurs)
            self.assertIn('Titre, avec "guillemets"', autre.livres)
            self.assertIs(autre.utilisateurs["Ana"].emprunts[0], autre.livres["1984"])
            self.assertTrue(autre.rendre("Ana", "1984"))
            chemin.with_name("livres_utilisateurs.csv").unlink()
            autre.charger(chemin)
            self.assertTrue(autre.rendre("Ana", "1984"))

    def test_csv_absent_et_invalide(self):
        with tempfile.TemporaryDirectory() as dossier:
            chemin = Path(dossier) / "livres.csv"
            vide = Bibliotheque()
            vide.charger(chemin)
            self.assertEqual(vide.livres, {})
            for contenu in (
                "mauvais,en-tete\n",
                "titre,auteur,année,disponible,emprunteur\n1984,Orwell,abc,True,\n",
                "titre,auteur,année,disponible,emprunteur\n1984,Orwell,1949,False,\n",
            ):
                chemin.write_text(contenu, encoding="utf-8")
                with self.assertRaises(ValueError):
                    self.b.charger(chemin)
                self.assertIs(self.b.livres["1984"], self.l)

    def test_stats_recherche_json(self):
        b = Bibliotheque()
        b.ajouter_utilisateur(Utilisateur("Ana"))
        for i in range(3):
            b.ajouter_livre(Livre(str(i), "Orwell", 1949))
        b.emprunter("Ana", "0")
        b.emprunter("Ana", "1")
        self.assertEqual(b.stats(), {"total": 3, "empruntes": 2, "par_utilisateur": {"Ana": 2}})
        self.assertEqual(len(b.rechercher_par_auteur("ORW")), 3)
        self.assertEqual(b.rechercher_par_auteur("absent"), [])
        with tempfile.TemporaryDirectory() as dossier:
            chemin = Path(dossier) / "export.json"
            b.exporter_json(chemin)
            donnees = json.loads(chemin.read_text(encoding="utf-8"))
            self.assertEqual(donnees["utilisateurs"][0]["emprunts"], ["0", "1"])

    def test_menu_et_redemarrage(self):
        with tempfile.TemporaryDirectory() as dossier:
            chemin = Path(dossier) / "livres.csv"
            saisies = ["1", "Erreur", "Auteur", "abc", "9",
                       "1", "1984", "Orwell", "1949", "2", "Ana",
                       "3", "Ana", "1984", "6"]
            sortie = io.StringIO()
            with patch("builtins.input", side_effect=saisies), redirect_stdout(sortie):
                main(chemin)
            self.assertIn("L'année doit être numérique", sortie.getvalue())
            self.assertIn("Choix invalide", sortie.getvalue())
            sortie = io.StringIO()
            with patch("builtins.input", side_effect=["5", "4", "Ana", "1984", "6"]), redirect_stdout(sortie):
                main(chemin)
            self.assertIn("emprunté par Ana", sortie.getvalue())
            self.assertIn("Livre rendu.", sortie.getvalue())
            b = Bibliotheque()
            b.charger(chemin)
            self.assertTrue(b.livres["1984"].disponible)


if __name__ == "__main__":
    unittest.main()
