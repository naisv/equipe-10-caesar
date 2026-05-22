# Mini-Projet A : Chiffrement Cesar et Enigma Cesar

Ce projet a ete realise par l'Equipe 10 dans le cadre du cours MGA802. Il implemente un outil en ligne de commande permettant de chiffrer, dechiffrer et casser par force brute des messages en utilisant les methodes de Cesar et d'Enigma Cesar.

## Membres de l'equipe (Equipe 10)
* Paul Serra
* Axel Walraet-Triolet
* Naïs Vigroux

---

## Fonctionnalites

Le programme offre une interface en ligne de commande pour manipuler deux methodes de chiffrement :
1. Chiffrement de Cesar : Utilise une cle unique entiere (positive, negative ou nulle).
2. Chiffrement Enigma Cesar : Une variante inspiree d'Enigma qui applique un tuple de 3 cles entieres de maniere cyclique sur les caracteres du message.

### Atouts du code :
* Prise en charge des fichiers : Si l'argument fourni se termine par .txt, le programme extrait automatiquement le texte du fichier pour le traiter.
* Normalisation du texte : Suppression automatique des accents (conversion via la forme de normalisation NFD) avant le chiffrement pour garantir la compatibilite avec l'alphabet standard.
* Respect de la casse : Les majuscules et les minuscules sont conservees lors du traitement, tandis que les caracteres non alphabetiques (espaces, ponctuation) restent inchanges.

