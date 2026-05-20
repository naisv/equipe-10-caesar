"""Tests pour le Mini-Projet A.

Ce fichier contient les chaînes de test officielles + quelques cas
limites. Ajoutez vos propres tests au fur et à mesure.

Pour lancer les tests :
    pip install pytest
    pytest -v
"""
import sys
from pathlib import Path
import pytest

# Permet d'importer main.py depuis le dossier parent
sys.path.insert(0, str(Path(__file__).parent.parent))
from main import chiffrer, dechiffrer, enigma_chiffrer, _parse_cle, enigma_dechiffrer # noqa: E402


# ---------- Chaînes de test officielles — César (spec §7) ----------

def test_cesar_officiel_cle_42():
    assert chiffrer("Veni, vidi, vici!", 42) == "Ludy, lyty, lysy!"


def test_cesar_officiel_cle_neg_42():
    assert chiffrer("Veni, vidi, vici!", -42) == "Foxs, fsns, fsms!"


# ---------- Chaîne de test officielle — Enigma César (spec §2.6) ----------

def test_enigma_officiel_maison():
    assert enigma_chiffrer("MAISON", (7, 16, 9)) == "TQRZEW"


# ---------- Cas standards (à compléter par votre équipe) ----------

def test_cesar_round_trip():
    """Chiffrer puis déchiffrer doit redonner le message original."""
    msg = "Bonjour le monde !"
    assert dechiffrer(chiffrer(msg, 7), 7) == msg


def test_cesar_cle_zero_identite():
    """Une clé de 0 ne doit rien changer."""
    assert chiffrer("Tout pareil.", 0) == "Tout pareil."

def test_parse_cle_cesar():
    """L'entrée d'un seul nombre doit renvoyer un entier"""
    cle="42"
    assert _parse_cle(cle) == 42

def test_parse_cle_cesar_neg():
    cle="-42"
    assert _parse_cle(cle) == -42

def test_parse_cle_enigma():
    cle="7-16-9"
    assert _parse_cle(cle) == (7,16,9)

def test_enigma_dechiffrer():
    mot="TQRZEW"
    cle=(7, 16, 9)
    assert enigma_dechiffrer(mot,cle) == "MAISON"

def test_parse_cle_enigma_valide():
    # Vérifie que la chaîne est bien convertie en tuple de 3 entiers
    assert _parse_cle("7-16-9") == (7, 16, 9)
    assert _parse_cle("-1-2-3") == (-1, 2, 3)

def test_enigma_rejet_cle_invalide():
    # Vérifie qu'une exception ValueError est levée si la clé n'a pas exactement 3 nombres
    # (Note : Si votre fonction _parse_cle ou enigma_chiffrer ne lève pas encore d'erreur,
    # ce test vous aidera à implémenter la validation avec un bloc try/except ou un assert)
    with pytest.raises(ValueError):
        cles_invalides = _parse_cle("7-16")
        enigma_chiffrer("TEST", cles_invalides)

    with pytest.raises(ValueError):
        cles_invalides = _parse_cle("1-2-3-4")
        enigma_chiffrer("TEST", cles_invalides)

# TODO : ajoutez vos propres tests ci-dessous
#  - test pour les majuscules
#  - test pour les caractères spéciaux (accents, ponctuation)
#  - test pour les très grandes clés (positives et négatives)
#  - test pour le brute-force (César ET Enigma César)
#  - test que enigma_chiffrer rejette une clé qui n'a pas 3 nombres
