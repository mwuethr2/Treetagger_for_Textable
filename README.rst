####################################
Treetagger Widget
####################################

Signal:
============
Inputs: Texte brut via text field

Output:


Description:
=============
Le widget Textable Treetagger répond au format Orange Canvas, il utilise Treetagger pour annoter un texte segmenté. 

Notre widget donnera la possibilité de retourner un texte segmenté et analyser selon les critères Treetagger choisis.

Ce travail est effectué dans le cadre d'un cours universitaire d'informatique pour les sciences humaines, basé sur le logiciel Textable, spécialisé dans l'analyse textuelle. 

Interface de base
==================
Le widget teste la présence ou non de treetagger sur l'ordinateur. Si cette présence est vérifié, il est possible d'utiliser le widget sinon un message d'erreur s'affiche. 
L'interface de base nous permet de choisir la langue (entre toutes les langues communes).

Aperçu de l'interface:

*  Treetagger

  .. image:: img/Treetagger.png

•	Opérations du widget:
  1	Envoi l'information au logiciel treetagger
  
  2	Récupère l'information en segmentation
  
•	output: segments en mots annotées (annotation: TAG, annotation: segment d'entrée) segment 
1 PHRASE | --> | Mot 1 | annotation: segment: 1 | annotation: TAG: NOM |  segment 2 TEXTE |  

Output: 
Autant de segmentation que de tokens



Interface avancé
=================
Une option "advanced settings" apparaît sur notre widget, elle est pour le moment pas en fonction. A noter que treetagger remplace automatiquement par <unknow> les caractères non reconnus.

Messages
========
