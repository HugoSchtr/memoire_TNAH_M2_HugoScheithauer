## Utilité du script

Script python écrit pour créer le référentiels des types d'acte

## Traitements

Pour chaque fichier XML d'un dossier donné :

* Parse le XML avec BeautifulSoup
* Reconstitue les types d'acte à partir des baselines. Pour cela, on s'appuie sur l'annotation sémantique d'eScriptorium où les baselines correspondant à un nouveau type d'acte ont été annotées avec la mention 'First_line'. Cela permet de reconstituer les unités réparties sur plusieurs lignes.
* Crée un fichier JSON indiquant le type d'acte et sa fréquence d'apparition dans les XML du dossier traité
* Crée un fichier texte log pour écrire les métadonnées 

