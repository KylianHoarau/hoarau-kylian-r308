# TP1 - Partie A : Dictionnaire d'étudiants

# Création d'un dictionnaire contenant les étudiants et leurs notes
etudiants = {
    "Alice": 12.0,
    "Bob": 15.0,
    "Claire": 9.5
}

# Affichage du dictionnaire
print(etudiants)



# Fonction permettant d'ajouter ou de modifier un étudiant
def ajouter_etudiant(d, nom, note):
    # Ajoute l'étudiant ou met à jour sa note
    d[nom] = float(note)


# Ajout d'un nouvel étudiant
ajouter_etudiant(etudiants, "David", 14.0)

# Affichage du dictionnaire après l'ajout
print(etudiants)







# Fonction permettant de calculer la moyenne de la classe
def moyenne_classe(d):
    # Vérifie si le dictionnaire est vide
    if len(d) == 0:
        return 0.0

    # Calcule la somme des notes et la divise par le nombre d'étudiants
    moyenne = sum(d.values()) / len(d)

    # Renvoie la moyenne arrondie à 2 chiffres après la virgule
    return round(moyenne, 2)


# Affichage de la moyenne de la classe
print("Moyenne de la classe :", moyenne_classe(etudiants))








# Fonction permettant de trouver le meilleur étudiant
def meilleur_etudiant(d):
    # Vérifie si le dictionnaire est vide
    if len(d) == 0:
        return None

    # Recherche l'étudiant ayant la meilleure note
    nom = max(d, key=d.get)

    # Renvoie le nom et la note de l'étudiant
    return (nom, d[nom])


# Affichage du meilleur étudiant
print("Meilleur étudiant :", meilleur_etudiant(etudiants))









# Fonction permettant de sauvegarder les étudiants dans un fichier texte
def sauvegarder_etudiants(d, fichier):
    try:
        # Ouvre le fichier en mode écriture
        with open(fichier, "w", encoding="utf-8") as f:

            # Parcourt les étudiants et leurs notes
            for nom, note in d.items():

                # Écrit chaque étudiant au format nom:note
                f.write(f"{nom}:{note}\n")

        print("Sauvegarde effectuée avec succès.")

    # Gestion des erreurs d'écriture
    except OSError as erreur:
        print("Erreur lors de la sauvegarde :", erreur)


# Sauvegarde du dictionnaire dans un fichier texte
sauvegarder_etudiants(etudiants, "tp1/etudiants.txt")
















# Fonction permettant de charger les étudiants depuis un fichier texte
def charger_etudiants(fichier):

    # Création d'un dictionnaire vide
    d = {}

    try:
        # Ouverture du fichier en mode lecture
        with open(fichier, "r", encoding="utf-8") as f:

            # Parcours du fichier ligne par ligne
            for ligne in f:

                # Suppression des espaces et retours à la ligne
                ligne = ligne.strip()

                # Vérification du séparateur entre le nom et la note
                if ":" not in ligne:
                    continue

                # Séparation du nom et de la note
                nom, note = ligne.split(":", 1)

                try:
                    # Conversion de la note en nombre décimal
                    d[nom] = float(note)

                except ValueError:
                    # Affichage d'un message si la note est invalide
                    print("Note invalide pour :", nom)

    except OSError as erreur:
        # Gestion des erreurs de lecture du fichier
        print("Erreur lors du chargement :", erreur)

    # Renvoie le dictionnaire contenant les étudiants
    return d


# Chargement des étudiants depuis le fichier texte
etudiants_charges = charger_etudiants("tp1/etudiants.txt")

# Affichage du dictionnaire chargé
print("Étudiants chargés :", etudiants_charges)






# Test de chargement d'un fichier inexistant
print("Test avec un fichier inexistant :")

# Tentative de lecture d'un fichier qui n'existe pas
resultat = charger_etudiants("tp1/inexistant.txt")

# Affichage du résultat
print("Résultat :", resultat)






# Test avec un dictionnaire vide
print("Test avec un dictionnaire vide :")

# Création d'un dictionnaire sans étudiant
etudiants_vides = {}

# Vérification du calcul de la moyenne
print("Moyenne :", moyenne_classe(etudiants_vides))

# Vérification de la recherche du meilleur étudiant
print("Meilleur étudiant :", meilleur_etudiant(etudiants_vides))





# Test avec des notes invalides et des lignes mal formées
print("Test avec des notes invalides :")

# Chargement du fichier contenant des erreurs
etudiants_test = charger_etudiants("tp1/test_notes.txt")

# Affichage des étudiants correctement chargés
print("Étudiants valides :", etudiants_test)