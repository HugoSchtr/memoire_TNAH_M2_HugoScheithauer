# Notes

Fichiers textes au format d'annotation BIOES pour tester la librairie python NERVAL (Teklia).

La vérité de terrain NER résulte de l'annotation d'une page de répertoire transcrite manuellement sur la plateforme d'annotation Inception, de l'export des annotations au format CONLL 2002, et de la conversion du format CONLL 2002 au format d'annotation BIOES grâce à un script présent sur le repository Github [NCRFpp](https://github.com/jiesutd/NCRFpp). Voir ici : https://github.com/jiesutd/NCRFpp/blob/master/utils/tagSchemeConverter.py#L16

Le fichier texte FRAN\_0025\_5038\_L-0\_htr\_cer\_9_bioes.txt résulte de l'annotation NER réalisée avec la librairie python de NLP [Stanza](https://stanfordnlp.github.io/stanza/ner.html). Le fichier original résulte d'une évaluation par lot de la REM réalisée avec KaMI puis d'un pré-traitement visant à reconstituer la structure logique, segmenter les mots et normaliser le texte. Le CER de la transcription originale était de 9%.
