# Command line interface for rule based word segmentation and normalization

Création d'un [CLI Python](https://gitlab.inria.fr/almanach/lectaurep/ner/-/blob/master/preprocessing/word_segmentation/CLI_rule_based_word_segmenter.py) pour reconstruire la structure logique,  débruiter et normaliser les PAGE XML en sortie d'HTR, en vue de créer des données d'entraînement pour affiner un modèle de NER.

## Installation

### Linux (Ubuntu/Debian) : 

* Cloner ce repository en local

* Installer un environnement virtuel avec Python3 :

   * Assurez-vous que votre version de Python est 3.x : ```python3 --version```
   * Créer un environnement virtuel dans le repository cloné, ou ailleurs en local : ```virtualenv -p python3 [NOM DE VOTRE ENVIRONNEMENT VIRTUEL]```

* Ouvrez un terminal et naviguer jusque dans le dossier courrant de votre environnement virtuel pour le sourcer : ```source env/bin/activate```

* Assurez-vous que vous êtes dans le repository cloné, installer les librairies python de requirements.txt : ```pip install -r requirements.txt```

## Fonctionnement

Ce CLI ne possède qu'une seule commande `transform`

Il prend en argument un chemin vers un dossier contenant des fichiers PAGE XML créées à partir de la transcription automatique de pages de répertoires de notaires.

Depuis l'emplacement du script, vous pouvez le tester sur des données présentes autre part dans ce repository Gitlab avec la commande suivante :

`python3 CLI_rule_based_word_segmentation_and_normalization.py transform ../HTR_batch_evaluation/ner_annotation_candidates_for_preprocessing/CER_13%/doc_145`

et

`python3 CLI_rule_based_word_segmentation_and_normalization.py transform ../HTR_batch_evaluation/ner_annotation_candidates_for_preprocessing/CER_13%/doc_156`

La commande va créer un dossier `out` à l'emplacement de ce script, qui contiendra les fichiers transformé en texte et pré-traités.

# Notes

* ner\_annotation\_candidates_preprocessed : contient des fichiers texte pré-traités pour être annotés en vue de l'affinage d'un modèle de NER.
* referentiels : contient un référentiel d'abréviations utilisé pour essayer de normaliser les données textuelles
* test_symspellpy : contient un notebook de test de la librairie python symmspellpy, où on teste la segmentation automatique des mots.
