# hoarau-kylian-r308

TP Python R3.08 - BUT RT2. Les travaux sont rangés dans un dossier par TP.

## TP1

Depuis la racine du dépôt :

```sh
python tp1/partie_A.py
```

## TP2 - Morpion

Python 3.10 ou plus, sans dépendance externe. Depuis la racine du dépôt :

```sh
python tp2/main.py
```

Le menu propose une partie contre une IA aléatoire ou maline, un mode à deux
humains, une simulation de 20 parties IA contre IA et les scores cumulés depuis
le lancement. Pour jouer, saisir `ligne colonne`, deux entiers entre 0 et 2.
Par exemple, `0 2` désigne la case en haut à droite. Une case occupée ou une
coordonnée hors grille est refusée ; le même joueur rejoue. Une saisie non
numérique redemande deux entiers.

L'IA maline cherche d'abord à gagner, puis à bloquer une victoire adverse,
puis choisit une case libre au hasard. Les scores sont gardés en mémoire pendant
la session ; ils ne sont pas sauvegardés entre deux lancements.

Pour lancer les tests du TP2 :

```sh
python -m unittest discover -s tp2 -p "test_*.py" -v
```

Ils couvrent les huit alignements gagnants, les cases occupées ou hors grille,
le tour conservé après un coup refusé, les exemples de l'IA maline et 20
parties IA contre IA. Le défi de championnat contre l'IA d'un voisin se joue
en salle avec un partenaire ; le mode à deux humains peut servir à le préparer.

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

