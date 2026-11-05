"""TP1 partie D : jeu du pendu."""

from mots import charger_mots, choisir_mot, masque


MAX_ERREURS = 7


def jouer_partie(mot):
    """Renvoie True si le mot est découvert avant sept erreurs."""
    if not isinstance(mot, str) or not mot.isalpha():
        raise ValueError("Le mot doit contenir uniquement des lettres.")
    mot = mot.upper()
    cache = masque(mot)
    proposees = []
    erreurs = 0

    while erreurs < MAX_ERREURS:
        print(f"Mot : {' '.join(cache)} | Erreurs : {erreurs}/{MAX_ERREURS}"
              f" | Lettres : {', '.join(proposees) or '-'}")
        lettre = input("Proposez une lettre : ").strip().upper()
        if len(lettre) != 1 or not lettre.isalpha():
            print("Entrez une seule lettre.")
            continue
        if lettre in proposees:
            print("Lettre déjà proposée.")
            continue
        proposees.append(lettre)
        if lettre in mot:
            for position, caractere in enumerate(mot):
                if caractere == lettre:
                    cache[position] = lettre
            if "_" not in cache:
                print(f"Mot : {' '.join(cache)} | Erreurs : {erreurs}/{MAX_ERREURS}"
                      f" | Lettres : {', '.join(proposees)}")
                print("Gagné !")
                return True
        else:
            erreurs += 1
            print("Lettre absente.")

    print(f"Mot : {' '.join(cache)} | Erreurs : {erreurs}/{MAX_ERREURS}"
          f" | Lettres : {', '.join(proposees)}")
    print(f"Perdu, le mot était {mot}.")
    return False


def main():
    try:
        jouer_partie(choisir_mot(charger_mots()))
    except (EOFError, KeyboardInterrupt):
        print("\nPartie interrompue.")


if __name__ == "__main__":
    main()
