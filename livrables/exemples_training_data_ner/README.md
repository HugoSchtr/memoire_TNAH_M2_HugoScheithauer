# Notes

Dans ce dossier est stocké un fichier texte, issu d'une transcription d'une page du document 156 sur eScriptorium. Celui-ci a été pré-traité, en vue de l'annotation de données d'entraînement pour un modèle de NER. 

Ce fichier texte a été annoté à l'aide de la plateforme [Inception](https://inception-project.github.io/), et a été exporté au format CONLL 2002 et 2003, comme indiqué dans le nom des fichiers exportés. 

Le fichier `annotation_ner.md` rend compte de notes faites durant l'annotation. 


Enfin, la capture d'écran `annotation_avec_recommandeur_inception.png` illustre l'utilisation du recommandeur d'Inception lors de l'annotation. Le recommandeur préannote le texte selon des paramètres établis par l'utilisateur-ice. En l'occurence, un string-matcher. Si l'utilisateur-ice annote "Paris" en tant que "LOC" une fois, le recommandeur préannotera les autres occurences de "Paris" dans le texte en tant que "LOC", et il revient à l'utilisateur-ice d'accepter ou non la recommandation.
