"""
MGA802 — Mini-Projet A : Chiffrement de César
Equipe 10 : Paul Serra, Axel Walraet-Triolet, Naïs Vigroux
"""
import argparse
import string
import unicodedata
import os
"""
import du dictionnaire pour le bruteforce
On le charge en début pour pouvoir l'utiliser sans avoir à le ré-ouvrir à chaque fois qu'on appelle la 
fonction force brute ou la fonction reconnaitre (ce qui alllège le programme)
"""
chemin = os.path.join(os.path.dirname(__file__), "dictionnaire_fr.txt")
with open(chemin, "r", encoding="utf-8") as f:
	dictionnaire = set(mot.lower() for mot in f.read().splitlines())

#Fonction qui supprime les accents de la chaîne de caractères fournie en paramètre et la retourne sans accent
def supprimer_accents(texte):
    forme_nfd = unicodedata.normalize('NFD', texte)
    texte_propre = "".join(c for c in forme_nfd if unicodedata.category(c) != 'Mn')
    return texte_propre

#Cette fonction extrait le texte dans un fichier dont le nom est donné en paramètre et le retourne en str
def recuperer_texte(texte):
    try:
        with open(texte, 'r', encoding='utf-8') as f:
            extraction = f.read()
    except FileNotFoundError:
        print("Fichier introuvable.")
        exit() # Cette ligne doit être alignée avec le print
    return extraction

"""Cette fonction chiffre en César avec un message et une clé
Elle vérifie si le texte donné est un texte ou le nom d'un fichier et récupère alors le texte du fichier
Elle fait appel à une fonction pour enlever les accents du texte
Elle chiffre selon la clé donnée en paramètrre"""
def chiffrer(message: str, cle: int):
	# Exigences visibles dans tests/test_caesar.py :
	# - test_cesar_officiel_cle_42
	# - test_cesar_officiel_cle_neg_42
	# - test_cesar_cle_zero_identite
	# Exemples attendus par les tests :
	# - chiffrer("Veni, vidi, vici!", 42) -> "Ludy, lyty, lysy!"
	# - chiffrer("Veni, vidi, vici!", -42) -> "Foxs, fsns, fsms!"
	# - chiffrer("Tout pareil.", 0) -> "Tout pareil."
	if message.endswith(".txt"):
		message=recuperer_texte(message)
	message_propre = supprimer_accents(message) #On retire les accents de la chaîne de caractères fournie
	alphabet = string.ascii_lowercase
	chiffrage=""  #Initialisation du résultat chiffré en une chaîne de caractères vide
	for i in range (0,len(message_propre)):
		#Vérification qu'il s'agit d'une lettre
		if message_propre[i].isalpha():
			est_majuscule=message_propre[i].isupper() #Enregistre si la lettre est une majuscule

			index=alphabet.find(message_propre[i].lower()) #Récupère l'index de la lettre (en minuscule)
			nouvel_index=(index + cle)%26 #Calcul du nouvel index avec la clé fournie et en s'assurant que l'on reste dans [0,26]

			if est_majuscule:
				chiffrage+=alphabet[nouvel_index].upper()#On met la lettre chiffrée en majuscule
			else:
				chiffrage+=alphabet[nouvel_index]
		else:
			chiffrage+=message_propre[i]
	return chiffrage

def dechiffrer(message: str, cle: int):
	# Exigence visible dans tests/test_caesar.py :
	# - test_cesar_round_trip
	# Le test vérifie que dechiffrer(chiffrer(msg, 7), 7) == msg.
	dechiffrage=chiffrer(message, -cle)
	return dechiffrage

def enigma_chiffrer(message: str, cles):
	chiffrage=""
	for position in range(len(message)):
		indice_cle=position%3 #permet d'identifier quelle clé du tuple cles il faut utiliser
		chiffrage+=chiffrer(message[position],cles[indice_cle]) #Chiffre la lettre du message avec la bonne clé
	return chiffrage
	# Exigence visible dans tests/test_caesar.py :
	# - test_enigma_officiel_maison
	# Exemple attendu par le test :
	# - enigma_chiffrer("MAISON", (7, 16, 9)) -> "TQRZEW"
	pass
def enigma_dechiffrer(message: str, cles):
	dechiffrage=""
	for position in range(len(message)):
		indice_cle=position%3 #permet d'identifier quelle clé du tuple cles il faut utiliser
		dechiffrage+=dechiffrer(message[position],cles[indice_cle]) #Chiffre la lettre du message avec la bonne clé
	return dechiffrage

def dechiffrer_force_brute(message, methode="caesar"):
	"""Décode un message par force brute en testant toutes les combinaisons.

	Si methode='caesar' : balaie 26 clés.
	Si methode='enigma' : balaie 17 576 combinaisons (3 boucles de 0 à 25).
	"""
	message_clair = ""

	if methode == "caesar":
		for cle in range(26):
			message_clair = dechiffrer(message, cle)
			if reconnaitre(message_clair):
				return message_clair

	elif methode == "enigma":
		# Triple boucle pour tester toutes les combinaisons de triplets (cle1, cle2, cle3)
		for c1 in range(26):
			for c2 in range(26):
				for c3 in range(26):
					cles_test = (c1, c2, c3)
					message_clair = enigma_dechiffrer(message, cles_test)

					if reconnaitre(message_clair):
						return message_clair

	return "Force brute echouée : aucun message lisible trouve."

def reconnaitre(message):
	#Créer une fonction qui permet de valider à un certain degré de confiance que le message est déchiffré
	#Renvoie un boléen
	mots = message.lower().replace("'", " ").replace("'", " ").split() #remplace ' par un espace
	mots_nettoyes = [mot.strip(string.punctuation) for mot in mots] #il ne reste plus que les mots séparés par des " "
	mots_nettoyes = [mot for mot in mots_nettoyes if mot]  # retire les mots vides crées par la ponctuation vide
	if len(mots_nettoyes) == 0:
		return False
	mots_valide=0 #Nombre de mots valide (provenant du dictionnaire)
	compteur=0
	for mot in mots_nettoyes:
		compteur+=1
		if mot in dictionnaire:
			mots_valide+=1
		restant=len(mots_nettoyes)-compteur
		if (mots_valide+restant)/len(mots_nettoyes)<0.8:
			return False
	score=mots_valide/len(mots_nettoyes)
	return score>=0.8

def _parse_cle(texte: str):
	"""Convertit l'argument --cle en clé utilisable.

	Cette fonction analyse la clé fournie par l'utilisateur en ligne de commande
	et la transforme en type Python approprié :
	- César           : un entier, ex. "42" ou "-42"
	- Enigma César    : trois entiers séparés par des tirets, ex. "7-16-9" ou "-7--16-9"

	Paramètre :
		texte (str) : la chaîne saisie par l'utilisateur après --cle.

	Retour :
		int : une clé entière pour César
		tuple : un tuple de 3 entiers pour Enigma César
	"""
	# Nettoyage des espaces superflus autour de la chaîne
	texte = texte.strip()

	# Compter le nombre de tirets qui servent de séparateurs.
	# Un tiret est un séparateur s'il n'est pas au tout début de la chaîne
	# et s'il n'est pas précédé immédiatement par un autre tiret (cas d'un nombre négatif).
	nb_separateurs = 0
	for i in range(1, len(texte)):
		if texte[i] == '-' and texte[i - 1] != '-':
			nb_separateurs += 1

	# Si on détecte des tirets séparateurs, on traite comme une clé Enigma
	if nb_separateurs > 0:
		try:
			# Pour découper proprement malgré les nombres négatifs, on remplace d'abord
			# les tirets de séparation par des espaces, puis on sépare.
			# Un tiret est un séparateur s'il est précédé d'un chiffre.
			liste_caracteres = []
			for i in range(len(texte)):
				if i > 0 and texte[i] == '-' and texte[i - 1].isdigit():
					liste_caracteres.append(' ')
				else:
					liste_caracteres.append(texte[i])

			chaine_nettoyee = "".join(liste_caracteres)
			cles_elements = chaine_nettoyee.split()

			# Validation stricte : la clé Enigma doit contenir exactement 3 nombres
			if len(cles_elements) != 3:
				raise ValueError(f"Une cle Enigma doit contenir exactement 3 nombres. Recu : {len(cles_elements)}")

			return tuple(int(x) for x in cles_elements)

		except ValueError as e:
			# On propage l'erreur avec un message explicite
			raise ValueError(f"Format de cle Enigma invalide ('a-b-c'). Erreur : {e}")

	# Sinon, c'est une clé César simple (entière, positive ou négative)
	try:
		return int(texte)
	except ValueError:
		raise ValueError(f"La cle pour Cesar doit etre un entier valide (ex: 42 ou -42). Recu : '{texte}'")



def main(argv=None):
	"""Point d'entrée principal du programme en ligne de commande.
	Contient aussi une interface console

	Cette fonction :
	1. Parse les arguments saisis par l'utilisateur (methode, action, message, clé)
	2. Convertit la clé en type approprié (int ou tuple)
	3. Appelle la fonction correspondante
	4. Affiche le résultat

	Paramètre :
		argv (list ou None) : si None, utilise sys.argv (arguments de la console).
		                      si list, utilise les arguments fournis (utile pour les tests).

	Exemples d'utilisation en terminal :
		python main.py ceasar chiffrer "Veni, vidi, vici!" --cle 42
		python main.py ceasar dechiffrer "Ludy, lyty, lysy!" --cle 42
		python main.py enigma chifrer "MAISON" --cle 7-16-9
		python main.py enigma dechifrer "TKQZYV" --cle 7--16-9
	"""
	# === ÉTAPE 1 : Créer et configurer le parseur d'arguments ===
	# argparse est un module qui aide à gérer les arguments en ligne de commande.
	# ArgumentParser crée un analyseur personnalisé pour notre programme.
	parser = argparse.ArgumentParser(
		description="Mini-Projet A : chiffrement de César / Enigma César.")

	# === ÉTAPE 2 : Définir les arguments attendus ===

	# Argument positionnel "methode" : l'opération à effectuer.
	# - Obligatoire (pas de -- devant)
	# - Doit être l'une des valeurs listées dans "choices"
	parser.add_argument(
		"methode",
		choices=["caesar", "enigma"],
		help="Type de chiffrage (ceasar ou enigma).")

	# Argument positionnel "action" : l'opération à effectuer.
	# - Obligatoire (pas de -- devant)
	# - Doit être l'une des valeurs listées dans "choices"
	parser.add_argument(
		"action",
		choices=["chiffrer", "dechiffrer","bruteforce"],
		help="Choix de l'action de chiffrage, de dechiffrage ou de bruteforce.")

	# Argument positionnel "message" : le texte à traiter.
	# - Obligatoire
	# - C'est la chaîne que nous allons chiffrer ou déchiffrer
	parser.add_argument(
		"message",
		help="Texte à traiter (mettez-le entre guillemets).")

	# Argument optionnel "--cle" (abréviation "-c") : la clé de chiffrement.
	# - Obligatoire via required=True
	# - Peut être un entier (César) ou trois entiers séparés par des tirets (Enigma César)
	parser.add_argument(
		"-c", "--cle", required=False,
		help="Clé : un entier (ex. '42') ou 'a-b-c' (ex. '7-16-9') pour Enigma.")

	# On regarde si aucun argument n'a ete passe au terminal
	import sys
	un_argument_est_present = (argv is not None and len(argv) > 0) or (argv is None and len(sys.argv) > 1)

	if not un_argument_est_present:
		# === MODE CONSOLE INTERACTIF ===
		print("=" * 50)
		print("       BIENVENUE DANS L'OUTIL DE CHIFFREMENT     ")
		print("=" * 50)

		# 1. Choix de la méthode
		print("\nChoisissez la methode :")
		print("1. Cesar (caesar)")
		print("2. Enigma Cesar (enigma)")
		choix_m = input("Votre choix (1 ou 2) : ").strip()
		while choix_m not in ["1","2"] :
			print("Erreur de saisie, veuillez choisir parmi 1 ou 2")
			choix_m = input("Votre choix (1 ou 2) : ").strip()
		methode = "caesar" if choix_m == "1" else "enigma"

		# 2. Choix de l'action
		print("\nChoisissez l'action :")
		print("1. Chiffrer")
		print("2. Dechiffrer")
		print("3. Force Brute (bruteforce)")
		choix_a = input("Votre choix (1, 2 ou 3) : ").strip()
		while choix_a not in ["1","2","3"] :
			print("Erreur de saisie, veuillez choisir parmi 1, 2 ou 3")
			choix_a = input("Votre choix (1, 2 ou 3) : ").strip()
		if choix_a == "1":
			action = "chiffrer"
		elif choix_a == "2":
			action = "dechiffrer"
		else:
			action = "bruteforce"

		# 3. Saisie du message
		message = input("\nEntrez votre message ou le nom du fichier (.txt) : ").strip()

		# 4. Saisie de la clé (sauf si brute force)
		if action != "bruteforce":
			if methode == "caesar":
				cle_texte = input("Entrez la cle (ex: 42) : ").strip()
				cle = _parse_cle(cle_texte)
			else :
				cle_texte = input("Entrez la cle (ex: 2-50--20) : ").strip()
				cle = _parse_cle(cle_texte)
		else:
			cle = None
	else:
		# === MODE COMMANDE TERMINAL (ARGPARSE) ===
		args = parser.parse_args(argv)

		# Validation rapide pour s'assurer que si le terminal est utilise, tout est fourni
		if not (args.methode and args.action and args.message):
			print("Erreur : En mode terminal, vous devez fournir --methode, --action et --message.")
			exit()

		methode = args.methode
		action = args.action
		message = args.message
		cle = _parse_cle(args.cle) if args.cle else None

	if methode == "caesar":
		if action == "chiffrer":
			resultat = chiffrer(message, cle)
		elif action == "dechiffrer":
			resultat = dechiffrer(message, cle)
		else:
			resultat = dechiffrer_force_brute(message, methode="caesar")
	else:
		if action == "chiffrer":
			resultat = enigma_chiffrer(message, cle)
		elif action == "dechiffrer":
			resultat = enigma_dechiffrer(message, cle)
		else:
			resultat = dechiffrer_force_brute(message, methode="enigma")


	# === ÉTAPE 6 : Afficher le résultat ===
	# print() affiche le résultat à l'écran pour que l'utilisateur le voie.
	print("\nResultat :")
	print(resultat)


if __name__ == "__main__":
	# Ce bloc s'exécute SEULEMENT si ce fichier est lancé directement depuis le terminal.
	# Exemple : python main.py chiffrer "Veni" --cle 42
	#
	# Il ne s'exécute PAS si on fait "import main" depuis un autre fichier Python.
	# Cela permet d'utiliser le code de main.py dans d'autres projets sans lancer main().
	# 
	# Pour les tests : pytest importe ce fichier mais ne lance pas main()
	# (car __name__ ne vaut pas "__main__" lors d'un import).
	main()
