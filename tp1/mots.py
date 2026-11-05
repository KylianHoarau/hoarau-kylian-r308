"""TP1 partie C : choix et masquage des mots."""

import random
from pathlib import Path


MOTS_DEFAUT = ["PYTHON", "RESEAU", "ROUTEUR", "ÉLÉPHANT", "BIBLIOTHEQUE"]
FICHIER_MOTS = Path(__file__).resolve().parent / "mots.txt"


def charger_mots(fichier=FICHIER_MOTS):
    try:
        lignes = Path(fichier).read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as erreur:
        print(f"Liste de mots indisponible ({erreur}) ; liste intégrée utilisée.")
        return MOTS_DEFAUT.copy()
    mots = [ligne.strip() for ligne in lignes if ligne.strip().isalpha()]
    return mots or MOTS_DEFAUT.copy()


def choisir_mot(liste, generateur=None):
    mots = [mot.strip() for mot in liste if isinstance(mot, str) and mot.strip().isalpha()]
    if not mots:
        raise ValueError("La liste ne contient aucun mot valide.")
    return (generateur or random).choice(mots).upper()


def masque(mot):
    return ["_" for _ in mot]
