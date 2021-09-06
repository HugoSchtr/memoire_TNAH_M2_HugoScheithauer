# Mémoire de stage - Master Technologies numériques appliquées à l'histoire, École nationale des chartes

## La reconnaissance d’entités nomméesappliquées à des données issues de latranscription automatique dedocuments manuscrits patrimoniaux. Expérimentations et préconisations à partir duprojet LECTAUREP

Ce mémoire rend compte et problématise un stage de quatre mois effectué au sein de l'équipe ALMAnaCH - Inria, pour le projet LECTAUREP (INRIA - Archives nationales), actuellement dans la fin de sa troisième phase. Le projet a pour objectif de transcrire automatiquement les répertoires des notaires conservés au Département du Minutier Central des Archives nationales. Grâce à l'utilisation de la plate-forme eScriptorium et dans la mesure où des modèles de transcription d'écriture manuscrites ont été entraînés, des données textuelles peuvent être produites en masse. La reconnaissance d'entités nommées (REN) est une exploitation envisageable pour enrichir les transcriptions qui en sont faites, ainsi que pour fournir de nouvelles portes d'entrées aux documents sources par le biais des entités nommées qu'ils contiennent. L'existence de modèles génériques de REN facilite l'expérimentation, mais ceux-ci ne constituent pas forcément une solution clé en main. Le bruit des données générées par la REM et la perte de la structure logique suite à la REM perturbent en effet leurs performances. 

Ce travail a pour but de donner des préconisations pour appliquer des outils de REN dans le cadre d'une campagne de REM, du pré-traitement des données brutes en sortie de transcription, au signalement des entités dans un fichier XML-TEI, tout en veillant à étudier les enjeux métiers de la REN dans un contexte patrimonial. 

Le mémoire est disponible au format PDF et LaTeX.

## Livrables

Le travail produit durant ce stage a été stocké dans un sous-répertoire du projet Gitlab de LECTAUREP, accessible avec le lien suivant : https://gitlab.inria.fr/almanach/lectaurep/ner

Dans un soucis d'accessibilité, ces livrables ont été reproduits dans le dossier éponyme de ce répertoire. 

Ils prennent majoritairement la forme de notebooks Jupyter et sont visualisables directement en ligne. Ils peuvent également être exécutés localement, en téléchargeant le répertoire Gitlab et en reproduisant les environnements de tests, soit un environnement virtuel basique dont les dépendances sont indiquées dans un fichier *requirements.txt*, soit dans un environnement Anaconda, dont les dépendances apparaissent dans un fichier *environment.yml*. Ils permettent d'accéder rapidement aux expériences réalisées, à leurs déroulés et à leurs résultats.

* corpus_test : contient les fichiers PAGE XML et texte utilisés pour les tests de REN
* exemples_training_data_ner : contient un fichier exemple de données d'entraînement pour un modèle de REN
* ner_python : contient plusieurs notebooks rangés selon la librairie de TAL qui a été utilisée pour les tests
* preprocessing : contient un essai de chaîne de traitement pour pré-traiter les PAGE XML obtenu avec eScriptorium en vue de l'annotation de données d'entraînement pour un modèle de NER
* recherche : contient une fiche de lecture, réalisée au début du stage
* referentiels : contient des référentiels et un script ayant servi à constituer l'un d'eux
* ressources : contient des diagrammes illustrant des points spécifiques du travail de recherche
* test_NERVAL : contient un notebook de test pour la librairie d'évaluation NER [NERVAL (Teklia)](https://teklia.com/blog/202104-nerval/)

## Cite this repository

Hugo Scheithauer, *La reconnaissance d'entités nommées appliquées à des données issues de la transcription automatique de documents manuscrits patrimoniaux. Expérimentations et préconisations à partir du projet LECTAUREP*, mémoire de master "Technologies numériques appliquées à l'histoire", dir. Alix Chagué et Thibault Clérice, École nationale des chartes, 2021, https://github.com/HugoSchtr/memoire_TNAH_M2_HugoScheithauer.
