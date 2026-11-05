"""Catalogue et utilisateurs, indexés par titre et par nom."""

import csv
import json
import os
import tempfile
from pathlib import Path

from livre import Livre
from utilisateur import Utilisateur


class Bibliotheque:
    def __init__(self):
        self.livres = {}
        self.utilisateurs = {}

    def ajouter_livre(self, livre):
        if livre.titre in self.livres:
            return False
        self.livres[livre.titre] = livre
        return True

    def ajouter_utilisateur(self, utilisateur):
        if utilisateur.nom in self.utilisateurs:
            return False
        self.utilisateurs[utilisateur.nom] = utilisateur
        return True

    def emprunter(self, nom, titre):
        utilisateur = self.utilisateurs.get(nom)
        livre = self.livres.get(titre)
        return bool(utilisateur and livre and utilisateur.emprunter_livre(livre))

    def rendre(self, nom, titre):
        utilisateur = self.utilisateurs.get(nom)
        livre = self.livres.get(titre)
        return bool(utilisateur and livre and utilisateur.rendre_livre(livre))

    def afficher_livres(self):
        for disponible, rubrique in ((True, "Disponibles"), (False, "Empruntés")):
            print(f"\n{rubrique} :")
            selection = [l for l in self.livres.values() if l.disponible == disponible]
            if not selection:
                print("Aucun livre.")
            for livre in selection:
                livre.afficher()

    @staticmethod
    def _ecrire_csv(chemin, champs, lignes):
        chemin = Path(chemin)
        chemin.parent.mkdir(parents=True, exist_ok=True)
        temporaire = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", newline="", delete=False,
                dir=chemin.parent, suffix=".tmp"
            ) as fichier:
                temporaire = Path(fichier.name)
                writer = csv.DictWriter(fichier, fieldnames=champs)
                writer.writeheader()
                writer.writerows(lignes)
            os.replace(temporaire, chemin)
        finally:
            if temporaire is not None and temporaire.exists():
                temporaire.unlink()

    def sauvegarder(self, chemin):
        """Le CSV principal respecte les cinq colonnes demandées.

        Un fichier voisin conserve aussi les utilisateurs sans emprunt.
        """
        chemin = Path(chemin)
        self._ecrire_csv(
            chemin.with_name(chemin.stem + "_utilisateurs.csv"),
            ["nom", "limite_emprunts"],
            ({"nom": u.nom, "limite_emprunts": u.limite_emprunts}
             for u in self.utilisateurs.values()),
        )
        self._ecrire_csv(
            chemin, ["titre", "auteur", "année", "disponible", "emprunteur"],
            ({"titre": l.titre, "auteur": l.auteur, "année": l.annee,
              "disponible": str(l.disponible), "emprunteur": l.emprunteur or ""}
             for l in self.livres.values()),
        )

    def charger(self, chemin):
        """Reconstruit les deux côtés des emprunts avant de remplacer l'état.

        Un fichier absent est accepté. Un fichier malformé lève ValueError
        sans modifier les données déjà en mémoire.
        """
        chemin = Path(chemin)
        nouvelle = Bibliotheque()
        utilisateurs_csv = chemin.with_name(chemin.stem + "_utilisateurs.csv")
        try:
            if utilisateurs_csv.exists():
                with utilisateurs_csv.open(encoding="utf-8-sig", newline="") as fichier:
                    reader = csv.DictReader(fichier)
                    if reader.fieldnames != ["nom", "limite_emprunts"]:
                        raise ValueError("Colonnes du fichier utilisateurs invalides.")
                    for ligne in reader:
                        utilisateur = Utilisateur(ligne["nom"], int(ligne["limite_emprunts"]))
                        if not nouvelle.ajouter_utilisateur(utilisateur):
                            raise ValueError("Utilisateur en double dans le CSV.")
            if chemin.exists():
                with chemin.open(encoding="utf-8-sig", newline="") as fichier:
                    reader = csv.DictReader(fichier)
                    if reader.fieldnames != ["titre", "auteur", "année", "disponible", "emprunteur"]:
                        raise ValueError("Colonnes du fichier livres invalides.")
                    for ligne in reader:
                        if ligne["disponible"] not in ("True", "False"):
                            raise ValueError("Disponibilité invalide dans le CSV.")
                        disponible = ligne["disponible"] == "True"
                        nom = ligne["emprunteur"].strip()
                        if disponible == bool(nom):
                            raise ValueError("Disponibilité et emprunteur incohérents.")
                        livre = Livre(ligne["titre"], ligne["auteur"], ligne["année"], disponible, nom)
                        if not nouvelle.ajouter_livre(livre):
                            raise ValueError("Titre en double dans le CSV.")
                        if not disponible:
                            if nom not in nouvelle.utilisateurs:
                                nouvelle.ajouter_utilisateur(Utilisateur(nom))
                            # Restaurer un emprunt existant ne crée pas un nouvel emprunt.
                            nouvelle.utilisateurs[nom].emprunts.append(livre)
        except (KeyError, TypeError, AttributeError, csv.Error) as erreur:
            raise ValueError(f"CSV malformé : {erreur}") from erreur
        self.livres = nouvelle.livres
        self.utilisateurs = nouvelle.utilisateurs

    def rechercher_par_auteur(self, recherche):
        recherche = recherche.strip().casefold()
        return [livre for livre in self.livres.values()
                if recherche in livre.auteur.casefold()]

    def stats(self):
        return {
            "total": len(self.livres),
            "empruntes": sum(not livre.disponible for livre in self.livres.values()),
            "par_utilisateur": {nom: len(u.emprunts) for nom, u in self.utilisateurs.items()},
        }

    def exporter_json(self, chemin):
        donnees = {
            "livres": [vars(livre) for livre in self.livres.values()],
            "utilisateurs": [
                {"nom": u.nom, "limite_emprunts": u.limite_emprunts,
                 "emprunts": [l.titre for l in u.emprunts]}
                for u in self.utilisateurs.values()
            ],
        }
        chemin = Path(chemin)
        chemin.parent.mkdir(parents=True, exist_ok=True)
        chemin.write_text(json.dumps(donnees, ensure_ascii=False, indent=2), encoding="utf-8")
