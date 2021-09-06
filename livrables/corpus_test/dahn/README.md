# Notes

On essaye d'appliquer un modèle de NER sur des données de nature différente de ce qu'on a en sortie d'HTR dans le projet LECTAUREP. Pour cela, on utilise un fichier du corpus du projet DAHN (https://github.com/FloChiff/DAHNProject ; https://digitalintellectuals.hypotheses.org/), plus précisément une lettre écrite par Paul d'Estournelles de Constant. Le type de langage, ici correspondant au genre épistolaire, est totalement différent de ce que l'on peut rencontrer dans les pages des répertoires de notaires. De plus, le texte ne contient pas de bruit comme on peut trouver dans les textes résultants de l'HTR.

On sélectionne la lettre 569 : https://github.com/FloChiff/DAHNProject/blob/master/Correspondence/Paul_d_Estournelles_de_Constant/Corpus/Lettre569_3octobre1919.xml

Après avoir récupéré le contenu de la balise `<text>`, un nettoyage à la main léger (suppression des sauts de lignes au sein des paragraphes, suppression des balises `<del>`) a été effectué pour avoir un texte exploitable.
