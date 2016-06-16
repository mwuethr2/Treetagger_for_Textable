####################################
Treetagger Widget
####################################

Signaux
=======

Input:

* ``Text Input``

  Segmentation contenant les segments à étiqueter

Output: 

* ``Text data``

  Segmentation en mots étiquetée par TreeTagger


Description
===========
Le widget Textable Treetagger répond au format Orange Canvas, il utilise Treetagger pour annoter un texte segmenté. 

Notre widget donne la possibilité de retourner un texte segmenté et analysé selon les critères Treetagger choisis.

Ce travail est effectué dans le cadre d'un cours universitaire d'informatique pour les sciences humaines, basé sur le logiciel Textable, spécialisé dans l'analyse textuelle. 

Interface
=========

Le widget demande le chemin vers treetagger. Si le chemin fourni par l'utilisateur est validé, il est possible d'utiliser le widget sinon un message d'erreur s'affiche. 

L'interface nous permet de choisir la langue (choix entre toutes les langues installées sur cet ordinateur).

  .. image:: img/Treetagger.png
  
  *[Remplacer par un screenshot]*

Fonctionnement
==============

Chaque token (mot) identifié par TreeTagger est placé dans un segment distinct et annoté avec les clés *lemma* (lemme) et *POS* (catégorie morphosytaxique).

Les annotations des segments entrants sont copiées sur les segments sortants.

Les options de TreeTagger utilisées sont: *[compléter svp]*

