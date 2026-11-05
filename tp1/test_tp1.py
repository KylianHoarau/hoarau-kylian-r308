"""Vérifications des jeux d'essai et des cas limites du TP1."""

import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import main as menu
from devine_nombre import jouer_partie as deviner
from mots import choisir_mot, masque
from partie_A import (ajouter_etudiant, charger_etudiants, meilleur_etudiant,
                      moyenne_classe, sauvegarder_etudiants)
from pendu import jouer_partie as pendu


class TestsTP1(unittest.TestCase):
    def test_notes_exemple_et_mise_a_jour(self):
        notes = {}
        for nom, note in (("Alice", 12), ("Bob", 15), ("Claire", "9.5")):
            self.assertTrue(ajouter_etudiant(notes, nom, note))
        self.assertEqual(moyenne_classe(notes), 12.17)
        self.assertEqual(meilleur_etudiant(notes), ("Bob", 15.0))
        self.assertTrue(ajouter_etudiant(notes, "Alice", 18))
        self.assertEqual(meilleur_etudiant(notes), ("Alice", 18.0))
        self.assertEqual(moyenne_classe({}), 0.0)
        self.assertIsNone(meilleur_etudiant({}))
        for note in ("abc", "nan", "inf", None):
            self.assertFalse(ajouter_etudiant(notes, "Autre", note))

    def test_notes_fichier_absent_et_lignes_invalides(self):
        with tempfile.TemporaryDirectory() as dossier:
            chemin = Path(dossier) / "notes.txt"
            self.assertEqual(charger_etudiants(chemin), {})
            chemin.write_text("Alice:12\nBob:abc\nLigneSansSeparateur\nClaire:9.5\n",
                              encoding="utf-8")
            with redirect_stdout(io.StringIO()):
                notes = charger_etudiants(chemin)
            self.assertEqual(notes, {"Alice": 12.0, "Claire": 9.5})
            self.assertTrue(sauvegarder_etudiants(notes, chemin))
            self.assertEqual(charger_etudiants(chemin), notes)

    def test_deviner_gagne_et_dix_essais(self):
        sortie = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "101", "1", "100", "42"]), redirect_stdout(sortie):
            self.assertTrue(deviner(secret=42))
        self.assertIn("Trop petit", sortie.getvalue())
        self.assertIn("Trop grand", sortie.getvalue())
        self.assertIn("Gagné en 3 essai(s)", sortie.getvalue())
        with patch("builtins.input", side_effect=["1"] * 10), redirect_stdout(io.StringIO()):
            self.assertFalse(deviner(secret=42))
        with self.assertRaises(ValueError):
            deviner(10, 1)

    def test_mots_et_pendu_gagne(self):
        self.assertEqual(choisir_mot(["Python"]), "PYTHON")
        self.assertEqual(masque("PYTHON"), ["_"] * 6)
        sortie = io.StringIO()
        with patch("builtins.input", side_effect=list("python")), redirect_stdout(sortie):
            self.assertTrue(pendu("Python"))
        self.assertIn("Gagné", sortie.getvalue())

    def test_pendu_perd_et_doublon(self):
        sortie = io.StringIO()
        with patch("builtins.input", side_effect=list("aabcdefg")), redirect_stdout(sortie):
            self.assertFalse(pendu("PYTHON"))
        self.assertIn("Lettre déjà proposée", sortie.getvalue())
        self.assertIn("Erreurs : 7/7", sortie.getvalue())
        self.assertIn("Perdu, le mot était PYTHON", sortie.getvalue())

    def test_score_rejouer_et_mot_accentue(self):
        with tempfile.TemporaryDirectory() as dossier:
            chemin = Path(dossier) / "scores.txt"
            saisies = ["2", "Ana", *list("python"), "o",
                       "3", "Ana", *list("éléphant"), "n"]
            sortie = io.StringIO()
            with patch("builtins.input", side_effect=saisies), \
                    patch.object(menu, "choisir_mot", return_value="PYTHON"), \
                    patch.object(menu, "getpass", return_value="ÉLÉPHANT"), \
                    redirect_stdout(sortie):
                menu.main(chemin)
            self.assertIn("Ana:2.0", chemin.read_text(encoding="utf-8"))
            sortie = io.StringIO()
            with patch("builtins.input", side_effect=["4", "5"]), redirect_stdout(sortie):
                menu.main(chemin)
            self.assertIn("Ana : 2.0", sortie.getvalue())


if __name__ == "__main__":
    unittest.main()
