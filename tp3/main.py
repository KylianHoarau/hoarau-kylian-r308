"""Lancement : python tp3/main.py depuis la racine du dépôt."""

from pathlib import Path

from bibliotheque import Bibliotheque
from livre import Livre
from utilisateur import Utilisateur


DONNEES = Path(__file__).resolve().parent / "donnees" / "livres.csv"


def main(chemin=DONNEES):
    bibliotheque = Bibliotheque()
    try:
        bibliotheque.charger(chemin)
    except (OSError, ValueError, UnicodeError) as erreur:
        # Ne pas écraser au prochain enregistrement un fichier illisible.
        print(f"Chargement impossible : {erreur}")
        print("Corrigez le fichier de données avant de relancer.")
        return

    while True:
        print("\n1 Ajouter un livre\n2 Ajouter un utilisateur\n3 Emprunter un livre"
              "\n4 Rendre un livre\n5 Afficher les livres\n6 Quitter et sauvegarder"
              "\n7 Statistiques\n8 Rechercher par auteur\n10 Exporter en JSON")
        try:
            choix = input("Votre choix : ").strip()
            if choix == "1":
                titre = input("Titre : ").strip()
                auteur = input("Auteur : ").strip()
                texte_annee = input("Année : ").strip()
                try:
                    annee = int(texte_annee)
                except ValueError:
                    print("L'année doit être numérique (un entier).")
                    continue
                livre = Livre(titre, auteur, annee)
                print("Livre ajouté." if bibliotheque.ajouter_livre(livre)
                      else "Ce titre existe déjà.")
            elif choix == "2":
                utilisateur = Utilisateur(input("Nom : "))
                print("Utilisateur ajouté." if bibliotheque.ajouter_utilisateur(utilisateur)
                      else "Ce nom existe déjà.")
            elif choix in ("3", "4"):
                nom = input("Nom de l'utilisateur : ").strip()
                titre = input("Titre du livre : ").strip()
                if nom not in bibliotheque.utilisateurs:
                    print("Utilisateur inconnu.")
                elif titre not in bibliotheque.livres:
                    print("Livre inconnu.")
                elif choix == "3":
                    print("Emprunt effectué." if bibliotheque.emprunter(nom, titre)
                          else "Emprunt refusé : livre indisponible ou limite atteinte.")
                else:
                    print("Livre rendu." if bibliotheque.rendre(nom, titre)
                          else "Retour refusé : cet utilisateur n'a pas emprunté ce livre.")
            elif choix == "5":
                bibliotheque.afficher_livres()
            elif choix == "6":
                try:
                    bibliotheque.sauvegarder(chemin)
                except OSError as erreur:
                    print(f"Sauvegarde impossible : {erreur}. Vous pouvez réessayer.")
                    continue
                print("Données sauvegardées. Au revoir !")
                return
            elif choix == "7":
                print(bibliotheque.stats())
            elif choix == "8":
                livres = bibliotheque.rechercher_par_auteur(input("Auteur (ou partie du nom) : "))
                if not livres:
                    print("Aucun résultat.")
                for livre in livres:
                    livre.afficher()
            elif choix == "10":
                destination = Path(chemin).with_suffix(".json")
                try:
                    bibliotheque.exporter_json(destination)
                    print(f"Export créé : {destination}")
                except OSError as erreur:
                    print(f"Export impossible : {erreur}")
            else:
                print("Choix invalide.")
        except ValueError as erreur:
            print(erreur)
        except (EOFError, KeyboardInterrupt):
            print("\nArrêt demandé.")
            try:
                bibliotheque.sauvegarder(chemin)
                print("Données sauvegardées.")
            except OSError as erreur:
                print(f"Sauvegarde impossible : {erreur}")
            return


if __name__ == "__main__":
    main()
