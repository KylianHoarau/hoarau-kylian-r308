# hoarau-kylian-r308

TP Python R3.08 - BUT RT2. Les travaux sont rangés dans un dossier par TP.

## TP1

Depuis la racine du dépôt :

```sh
python tp1/partie_A.py
```

## TP3 - Gestion d'une bibliothèque

Python 3.10 ou plus, sans dépendance externe. Depuis la racine du dépôt :

```sh
python tp3/main.py
```

Sous Windows, `py -3 tp3/main.py` peut aussi être utilisé. Le menu permet
d'ajouter des livres et utilisateurs, d'emprunter et rendre un livre, d'afficher
le catalogue, les statistiques, de chercher par auteur et d'exporter en JSON.
Le choix 6 sauvegarde puis quitte. Le choix 9 est invalide, comme dans le jeu
d'essai de l'énoncé ; l'export JSON est au choix 10.

Les données CSV sont enregistrées dans `tp3/donnees/`. Les livres sont dans
`livres.csv` (titre, auteur, année, disponible, emprunteur). Le fichier
`livres_utilisateurs.csv` conserve aussi les utilisateurs sans emprunt et leur
limite. Le programme recharge automatiquement les données au démarrage. Un
fichier absent donne une bibliothèque vide ; un fichier illisible provoque un
message et n'est pas écrasé. L'export JSON est une copie et ne sert pas au
rechargement.

La limite par défaut est de trois emprunts par utilisateur. Seul l'emprunteur
peut rendre son livre. Les noms et titres sont uniques et sensibles à la casse.

Pour lancer les jeux d'essai et les cas piégés :

```sh
python -m unittest discover -s tp3 -p "test_*.py" -v
```

Pour la soutenance, tester un livre ou utilisateur inconnu, un emprunt double,
un retour par une autre personne, une année non numérique et un redémarrage
après sauvegarde. Les parties A à E du TP3 ont chacune leur commit ; le bonus
de tests a aussi son commit.

Le TP2 n'est pas présent dans ce dépôt.
