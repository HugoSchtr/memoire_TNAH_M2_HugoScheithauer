# La reconnaissance d'entités nommées : exploration et expériences dans le contexte du projet LECTAUREP

Ce repository héberge le travail effectué durant mon stage dans l'équipe ALMAnaCH - INRIA, lors de mon M2 "Technologies numériques appliquées à l'histoire" à l'Ecole nationale des chartes.

## Structure du repository

```
├── corpus_test
│   ├── dahn
│   └── lectaurep
├── exemples_training_data_ner
├── ner_python
│   ├── ner_entityfishing
│   ├── ner_nltk
│   ├── ner_spacy
│   └── ner_stanza
├── preprocessing
│   ├── HTR_batch_evaluation
│   └── word_segmentation
├── recherche
├── referentiels
│   ├── data
│   └── script
├── ressources
└── test_NERVAL
    └── data
```

* corpus_test : contient les fichiers PAGE XML et texte utilisés pour les tests 
* exemples\_training\_data_ner : contient un fichier exemple de données d'entraînement pour un modèle de NER
* ner_python : contient plusieurs notebooks rangés selon la librairie de TAL qui a été utilisé pour les tests
* preprocessing : contient un essai de chaîne de traitement pour pré-traité les PAGE XML obtenu avec eScriptorium en vue de l'annotation de données d'entraînement pour un modèle de NER
* recherche : contient une fiche de lecture, réalisé au début du stage
* referentiels : contient des référentiels et un script ayant servi à constituer l'un d'eux
* ressources : contient des diagrammes illustrant des points spécifiques du travail de recherche
* test_NERVAL : contient un notebook de test pour la librairie d'évaluation NER nommée [NERVAL (Teklia)](https://teklia.com/blog/202104-nerval/)

## Environnements virtuels

Pour recréer les environnements virtuels lorsque cela est nécessaire, un fichier `environment.yml` est fourni pour les environnements Anaconda, ou fichier `requirements.txt` pour les environnements virtuels classiques. 
