"""Menu du TP2 : python tp2/main.py depuis la racine du dépôt."""

from jeu import jouer_partie
from joueurs import JoueurHumain, JoueurIA


def main():
    scores = {"X": 0, "O": 0, "Nul": 0}
    while True:
        print("\n1 Humain contre IA aléatoire"
              "\n2 Deux humains"
              "\n3 IA contre IA (20 parties)"
              "\n4 Afficher les scores"
              "\n5 Quitter")
        try:
            choix = input("Votre choix : ").strip()
            if choix == "1":
                resultat = jouer_partie(JoueurHumain("Humain"), JoueurIA())
                scores[resultat] += 1
            elif choix == "2":
                resultat = jouer_partie(JoueurHumain("Joueur 1"),
                                        JoueurHumain("Joueur 2"))
                scores[resultat] += 1
            elif choix == "3":
                bilan = {"X": 0, "O": 0, "Nul": 0}
                for _ in range(20):
                    resultat = jouer_partie(JoueurIA("IA X"),
                                            JoueurIA("IA O"), afficher=False)
                    bilan[resultat] += 1
                    scores[resultat] += 1
                print(f"20 parties terminées : {bilan}")
            elif choix == "4":
                print(f"Scores depuis le lancement : {scores}")
            elif choix == "5":
                print("Au revoir !")
                return
            else:
                print("Choix invalide.")
        except (EOFError, KeyboardInterrupt):
            print("\nPartie interrompue. Au revoir !")
            return


if __name__ == "__main__":
    main()
