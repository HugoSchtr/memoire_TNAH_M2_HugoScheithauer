# Command line interface - Batch evaluation with KaMI (évaluation par lots avec KaMI)

Création d'un [CLI python](https://gitlab.inria.fr/almanach/lectaurep/ner/-/blob/master/preprocessing/HTR_batch_evaluation/batch_evaluation_with_kami.py) pour évaluer par lot l'HTR avec [KaMI](https://gitlab.inria.fr/dh-projects/kami/kami-lib). 

A partir d'une vérité de terrain, évalue chaque PAGE XML disponible localement en :

1. Reconstituant les unités sémantiques de la colonne 5, sur laquelle porte l'expérience
2. Créant un JSON avec les scores des transcriptions obtenus grâce à KaMI, que l'on peut exploiter pour créer un set de candidats à l'annotation

## Installation

### Linux (Ubuntu/Debian) : 

* Cloner ce repository en local

* Installer un environnement virtuel avec Python3 :

   * Assurez-vous que votre version de Python est 3.x : ```python3 --version```
   * Créer un environnement virtuel dans le repository cloné, ou ailleurs en local : ```virtualenv -p python3 [NOM DE VOTRE ENVIRONNEMENT VIRTUEL]```

* Ouvrez un terminal et naviguer jusque dans le dossier courrant de votre environnement virtuel pour le sourcer : ```source env/bin/activate```

* Assurez-vous que vous êtes dans le repository cloné, installer les librairies python de requirements.txt : ```pip install -r requirements.txt```

## Fonctionnement

Ce CLI ne possède qu'une seule commande `evaluate`

Il prend deux arguments :

* un chemin vers un dossier contenant des PAGE XML constituant la vérité de terrain utilisée pour l'évaluation.
* un chemin vers un dossier contenant un ou des sous-répertoires contenant eux-mêmes des fichiers PAGE XML créées à partir de la transcription automatique de pages de répertoires de notaires.

Structure de l'input :

      input
        ├── document
          ├── document ground truth containing PAGE XML files
          └── HTR
              ├── document HTR resulting from model 𝑥
              └── ...
              
Dans chaque sous-répertoires de PAGE XML résultant de l'HTR est également un attendu un fichier `model_log.txt` contenant le nom du modèle d'HTR utilisé pour la transcription.

Depuis l'emplacement du script, vous pouvez le tester sur des données présentes autre part dans ce repository Gitlab selon le processus suivant :

* Cloner le repository gitlab de [KaMI](https://gitlab.inria.fr/dh-projects/kami/kami-lib)
* Suivre les consignes d'installation : https://gitlab.inria.fr/dh-projects/kami/kami-lib#developer-installation
* Copier/Coller le dossier docs\_for\_HTR\_evaluation\_with_kami dans le dossier cloné et le CLI `batch_evaluation_with_kami.py`
* Se déplacer dans le dossier cloné
* Lancer le script avec les commandes suivantes :

`python3 batch_evaluation_with_kami.py evaluate docs_for_HTR_evaluation_with_kami/doc_145/GT docs_for_HTR_evaluation_with_kami/doc_145/HTR`

et

`python3 batch_evaluation_with_kami.py evaluate docs_for_HTR_evaluation_with_kami/doc_156/GT docs_for_HTR_evaluation_with_kami/doc_156/HTR`

Le CLI crée en sortie un fichier JSON contenant l'évaluation par lots des sous-dossiers d'HTR.

Les fichiers JSON résultant de ce CLI peuvent être trouvés dans le dossier HTR\_scores\_with_kami

# get_pages_based_on_HTR_scores.py

Script permettant d'exploiter les fichiers JSON créés avec le CLI, pour récupérer, par exemple, tous les PAGE XML résultant de l'HTR ayant un score de CER choisi, en vue de sélectionner des candidats à annoter pour constituer des données d'entraînement NER. 

Le script doit être transformé en fonction dans le futur pour une utilisation plus simple. Cette version a été utilisée pour récupérer des transcriptions avec un score de CER de 15% ou moins. 

Les fichiers présents dans le dossier ner\_annotation\_candidates\_for_preprocessing ont été obtenus avec ce script.
