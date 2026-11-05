"""TP1 partie B : deviner un entier en dix essais au maximum."""

import random


def jouer_partie(minimum=1, maximum=100, secret=None):
    if not isinstance(minimum, int) or not isinstance(maximum, int) or minimum >= maximum:
        raise ValueError("Les bornes doivent être des entiers croissants.")
    if secret is None:
        secret = random.randint(minimum, maximum)
    if not isinstance(secret, int) or not minimum <= secret <= maximum:
        raise ValueError("Le nombre secret doit être dans les bornes.")

    print(f"Devinez un nombre entre {minimum} et {maximum} (10 essais).")
    essais = 0
    while essais < 10:
        try:
            proposition = int(input(f"Essai {essais + 1}/10 : ").strip())
        except ValueError:
            print("Entrez un nombre entier.")
            continue
        if not minimum <= proposition <= maximum:
            print(f"Choisissez un nombre entre {minimum} et {maximum}.")
            continue
        essais += 1
        if proposition < secret:
            print("Trop petit")
        elif proposition > secret:
            print("Trop grand")
        else:
            print(f"Gagné en {essais} essai(s) !")
            return True
    print(f"Perdu. Le nombre était {secret}.")
    return False


def main():
    while True:
        try:
            bornes = input("Bornes min max (Entrée pour 1 100) : ").strip()
            if bornes:
                parties = bornes.split()
                if len(parties) != 2:
                    print("Entrez deux bornes entières séparées par un espace.")
                    continue
                try:
                    minimum, maximum = map(int, parties)
                    jouer_partie(minimum, maximum)
                except ValueError as erreur:
                    print(erreur)
                    continue
            else:
                jouer_partie()
            if input("Rejouer ? (o/n) : ").strip().casefold() != "o":
                return
        except (EOFError, KeyboardInterrupt):
            print("\nPartie interrompue.")
            return


if __name__ == "__main__":
    main()
