## Notes lors de l'annotation avec Inception

* L'annotation ne permet pas de segmenter des mots par défaut. Il faut régler l'annotation au niveau caractère : "character-level"

exemple : "épouseauguste Salonon" pour annoter "auguste Salonon"

* Inception onsidère "." comme une fin de phrase par défaut, et empêche d'annoter les caractères se trouvant après un point. Cela pose problème pour les abréviations.
Solution : effectuer les réglages dans "behavior" et cocher "allow crossing sentence boundaries"
