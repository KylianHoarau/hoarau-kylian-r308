"""Menu TP1 : jeux et hall of fame commun."""

from getpass import getpass
from pathlib import Path

from devine_nombre import jouer_partie as deviner
from mots import charger_mots, choisir_mot
from partie_A import ajouter_etudiant, charger_etudiants, sauvegarder_etudiants
from pendu import jouer_partie as pendu


SCORES = Path(__file__).resolve().parent / "scores.txt"


def enregistrer_victoire(scores, nom):
    if not isinstance(nom, str) or not nom.strip() or ":" in nom or "\n" in nom:
        return False
    nom = nom.strip()
    return ajouter_etudiant(scores, nom, scores.get(nom, 0.0) + 1.0)


def afficher_scores(scores):
    if not scores:
        print("Aucune victoire enregistrée.")
    else:
        print("Hall of fame :")
        for nom, victoires in sorted(scores.items(), key=lambda item: (-item[1], item[0])):
            print(f"{nom} : {victoires:.1f}")


def main(chemin_scores=SCORES):
    scores = charger_etudiants(chemin_scores)
    try:
        while True:
            print("\n1 Devine le nombre\n2 Pendu (mot aléatoire)"
                  "\n3 Pendu (mot choisi par un autre joueur)"
                  "\n4 Hall of fame\n5 Quitter")
            choix = input("Votre choix : ").strip()
            if choix == "4":
                afficher_scores(scores)
                continue
            if choix == "5":
                break
            if choix not in ("1", "2", "3"):
                print("Choix invalide.")
                continue

            nom = input("Votre nom : ").strip()
            if not nom or ":" in nom or "\n" in nom:
                print("Nom invalide.")
                continue
            if choix == "1":
                gagne = deviner()
            elif choix == "2":
                gagne = pendu(choisir_mot(charger_mots()))
            else:
                mot = getpass("L'autre joueur choisit un mot (saisie masquée) : ").strip()
                if not mot.isalpha():
                    print("Entrez un mot composé uniquement de lettres.")
                    continue
                gagne = pendu(mot)
            if gagne:
                enregistrer_victoire(scores, nom)
            if not sauvegarder_etudiants(scores, chemin_scores):
                print("Les scores n'ont pas pu être enregistrés.")
            if input("Rejouer ? (o/n) : ").strip().casefold() != "o":
                break
    except (EOFError, KeyboardInterrupt):
        print("\nPartie interrompue.")
    if not sauvegarder_etudiants(scores, chemin_scores):
        print("Les scores n'ont pas pu être enregistrés.")


if __name__ == "__main__":
    main()
