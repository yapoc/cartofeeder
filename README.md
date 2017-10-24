# But du script
Ce script prend une liste de domaines en paramètres et en s'appuyant sur ma version de la lib' `python-whois` extrait les informations dont j'ai besoin pour automatiser l'alimentation de la carto.

Les champs actuellement extraits sont : 
  * le domaine,
  * le registrat, 
  * le registrant,
  * la date de fin d'enregistrement (si dispo),
  * les serveurs de nomi (à alimenter depuis une requête DNS dans le futur?).


# Installation du script

Copier coller les commandes suivantes sans se poser de questions tant que ça fonctionne. Si ça fonctionne pas, tu peux toujours essayer de m'appeler.

  * Créer l'environnement virtuel `python` : 

```
python -m venv ENVIRONNEMENT_VIRTUEL
```

  * Cloner le dépôt `python-whois`

```
git clone https://github.com/yapoc/python-whois.git
```

  * Sourcer l'environnement virtuel

```
source ENVIRONNEMENT_VIRTUEL/bin/activate
```

  * Construire le paquet

```
cd python-whois
python setup.py build
python setupt.py install
```

  * Cloner le dépôt `cartofeeder` :

```
git clone https://github.com/yapoc/cartofeeder.git
```

# Utilisation du script

  * Sourcer l'environnement virtuel

```
source ENVIRONNEMENT_VIRTUEL/bin/activate
```

  * Lancer le script en indiquant en paramètre l'emplacement du fichier contenant la liste des domaines et l'emplacement du fichier CSV de sortie.

```
cd cartofeeder
./alimentation_carto.py -i <LISTE_DES_DOMAINES_À_ANALYSER>[ -o <CHEMIN_VERS_RAPPORT_CSV>]
```
