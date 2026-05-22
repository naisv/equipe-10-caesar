# Mini-Projet A : Chiffrement Cesar et Enigma Cesar

Ce projet a ete realise par l'Equipe 10 dans le cadre du cours MGA802. Il implemente un outil polyvalent permettant de chiffrer, dechiffrer et casser par force brute des messages en utilisant les methodes de Cesar et d'Enigma Cesar.

## Membres de l'equipe (Equipe 10)
* Paul Serra
* Axel Walraet-Triolet
* Naïs Vigroux

---

## Fonctionnalites

Le programme offre une double interface (ligne de commande et menu interactif) pour manipuler deux methodes de chiffrement :
1. Chiffrement de Cesar : Utilise une cle unique entiere (positive, negative ou nulle).
2. Chiffrement Enigma Cesar : Une variante qui applique un tuple de 3 cles entieres de maniere cyclique sur les caracteres du message.

### Atouts du code :
* Double Mode d'Exécution : Si le programme est lance sans arguments, un menu interactif guide l'utilisateur pas a pas. Si des arguments sont passes au terminal, le script s'execute directement sans interruption.
* Prise en charge des fichiers : Si l'argument ou l'entree fournie se termine par .txt, le programme extrait automatiquement le texte du fichier pour le traiter.
* Normalisation du texte : Suppression automatique des accents (conversion via la forme de normalisation NFD) avant le chiffrement.
* Respect de la casse et ponctuation : Les majuscules et les minuscules sont conservees lors du traitement, tandis que les caracteres non alphabetiques restent inchanges.
* Force Brute Automatique : Analyse automatique des textes dechiffres grace a un dictionnaire francais (dictionnaire_fr.txt). Le programme valide la pertinence du dechiffrement des qu'un seuil de 60% de mots valides est atteint.

---

## Installation et Configuration

### Prerequis
Assurez-vous d'avoir Python 3.x installe sur votre machine.

### 1. Cloner le depot
```bash
git clone https://github.com/naisv/equipe-10-caesar.git
cd equipe-10-caesar
```

### 2. Installer les dependances (pytest)
```bash
python3 -m pip install -r requirements.txt
```

## Utilisation

### Mode 1 : Menu Console Interactif
Lancez simplement le script sans aucun argument. Le programme vous demandera interactivement la methode, l'action, le message et la cle :
```bash
python main.py
```

### Mode 2 : Ligne de commande (Terminal)
Vous pouvez specifier l'ensemble des arguments directement dans le terminal selon la syntaxe suivante :
python main.py [caesar|enigma] [chiffrer|dechiffrer|bruteforce] "[message_ou_fichier]" -c [valeur_cle]
exemples : 
```bash
python main.py caesar chiffrer "Veni, vidi, vici!" -c 42
python main.py caesar dechiffrer "Ludy, lyty, lysy!" -c 42
python main.py enigma chiffrer "MAISON" -c 7-16-9
python main.py enigma bruteforce "TQRZEW" 
python main.py caesar chiffrer message.txt -c 15
```

## Structure du Code et Architecture
Le script main.py centralise la logique et la gestion des interfaces :

* supprimer_accents(texte) : Nettoie la chaine en separant les caracteres de leurs accents (NFD).

* recuperer_texte(texte) : Ouvre et lit les fichiers .txt specifies avec un encodage utf-8.

* chiffrer(message, cle) / dechiffrer(message, cle) : Algorithme Cesar exploitant l'arithmetique modulaire (% 26).

* enigma_chiffrer(message, cles) / enigma_dechiffrer(message, cles) : Applique une rotation cyclique (position % 3) des trois cles sur le message.

* dechiffrer_force_brute(message, methode) : Aligne une boucle simple (26 cles pour Cesar) ou une triple boucle imbriquee (17 576 combinaisons pour Enigma) pour retrouver le message clair.

* reconnaitre(message) : Nettoie le message des symboles de ponctuation et verifie la presence des mots dans dictionnaire_fr.txt pour calculer un score de confiance.

* _parse_cle(texte) : Analyse la chaine saisie pour la convertir en int (Cesar) ou en tuple d'entiers (Enigma), tout en gerant de maniere robuste les nombres negatifs et en validant le format requis.

## Tests Unitaires (pytest)
Le projet integre une suite de tests unitaires complete pour valider le comportement de chaque fonction. Pour executer les tests :
```bash
pytest -v
```
Les tests valident notamment la conservation de la casse, la suppression des accents, le modulo des tres grandes cles (positives et negatives), la detection et le rejet des cles Enigma mal formatees, ainsi que le succes des algorithmes de force brute.
