"""TP1 partie A : dictionnaire de notes et fichier nom:note."""

import math
import tempfile
from pathlib import Path


DOSSIER = Path(__file__).resolve().parent


def ajouter_etudiant(d, nom, note):
    """Ajoute ou actualise une note ; renvoie False si la saisie est invalide."""
    if not isinstance(nom, str) or not nom.strip() or ":" in nom or "\n" in nom:
        return False
    try:
        valeur = float(note)
    except (TypeError, ValueError, OverflowError):
        return False
    if not math.isfinite(valeur):
        return False
    d[nom.strip()] = valeur
    return True


def moyenne_classe(d):
    return round(sum(d.values()) / len(d), 2) if d else 0.0


def meilleur_etudiant(d):
    return max(d.items(), key=lambda paire: paire[1]) if d else None


def sauvegarder_etudiants(d, fichier):
    """Écrit une ligne nom:note par étudiant ; signale les erreurs d'E/S."""
    try:
        with open(fichier, "w", encoding="utf-8") as sortie:
            for nom, note in d.items():
                sortie.write(f"{nom}:{float(note)}\n")
    except (OSError, TypeError, ValueError) as erreur:
        print(f"Erreur lors de la sauvegarde : {erreur}")
        return False
    return True


def charger_etudiants(fichier):
    """Ignore les lignes mal formées ; fichier absent = dictionnaire vide."""
    resultat = {}
    try:
        with open(fichier, encoding="utf-8") as entree:
            for numero, ligne in enumerate(entree, 1):
                ligne = ligne.strip()
                if not ligne:
                    continue
                if ":" not in ligne:
                    print(f"Ligne {numero} ignorée : séparateur manquant.")
                    continue
                nom, note = ligne.split(":", 1)
                if not ajouter_etudiant(resultat, nom, note):
                    print(f"Ligne {numero} ignorée : nom ou note invalide.")
    except FileNotFoundError:
        return {}
    except (OSError, UnicodeError) as erreur:
        print(f"Erreur lors du chargement : {erreur}")
    return resultat


def demonstration():
    etudiants = {}
    for nom, note in (("Alice", 12), ("Bob", 15), ("Claire", 9.5)):
        ajouter_etudiant(etudiants, nom, note)
    print("Étudiants :", etudiants)
    print("Moyenne :", moyenne_classe(etudiants))
    print("Meilleur étudiant :", meilleur_etudiant(etudiants))

    with tempfile.TemporaryDirectory() as dossier:
        chemin = Path(dossier) / "etudiants.txt"
        if sauvegarder_etudiants(etudiants, chemin):
            print("Relu depuis le fichier :", charger_etudiants(chemin))
    print("Fichier absent :", charger_etudiants(DOSSIER / "inexistant.txt"))
    print("Dictionnaire vide :", moyenne_classe({}), meilleur_etudiant({}))
    print("Lignes invalides :", charger_etudiants(DOSSIER / "test_notes.txt"))


if __name__ == "__main__":
    demonstration()
