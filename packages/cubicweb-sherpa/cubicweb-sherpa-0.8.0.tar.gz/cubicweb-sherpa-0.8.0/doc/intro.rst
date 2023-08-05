Présentation
------------

Agape 2 est une application Web permettant de générer des profils SEDA_. Elle prend la suite de
l'application de bureau Agape_, en supportant la `version 2 du SEDA`_ et en ajoutant une dimension
collaborative.

Principales fonctionnalités :

* modèle de données compatible `SEDA 2`_,

* export des profils au format `SEDA 2`_ en utilisant le formalisme de schéma `Relax NG`_ (`XML
  Schema`_ est également partiellement disponible, mais ce formalisme ne permet pas d'exprimer
  totalement des profils),

* 2 interfaces disponibles pour la définition des profils : simple ou complet - la première
  facilitant l'appropriation du `SEDA 2`_ en restreignant le modèle et en s'approchant de celui de
  des version `1.0`_ et `0.2`_ de la norme,

* génération de documentation HTML_ pour les profils,

* coopération des utilisateurs (capacité à se créer un compte, voir/copier les profils des autres,
  etc).

Les profils simplifiés seront prochainement exportables vers les versions `0.2`_ et/ou `1.0`_.

L'application est publiée sous la licence `GPL v2`_. Son code source est disponible ici_ et vous
pouvez soumettre des anomalies ou des demandes de fonctionnalités là_.


.. _SEDA: http://www.archivesdefrance.culture.gouv.fr/gerer/archives-electroniques/standard/seda/
.. _Agape: http://agape.adullact.net/
.. _`version 2 du SEDA`: http://www.archivesdefrance.culture.gouv.fr/seda/
.. _`SEDA 2`: http://www.archivesdefrance.culture.gouv.fr/seda/
.. _`Relax NG`: https://fr.m.wikipedia.org/wiki/Relax_NG
.. _`XML Schema`: https://fr.m.wikipedia.org/wiki/XML_Schema
.. _`1.0`: http://www.archivesdefrance.culture.gouv.fr/seda/documentation/SEDA_description_standard_v1_0.pdf
.. _`0.2`: http://www.archivesdefrance.culture.gouv.fr/seda/documentation/archives_echanges_v0-2_description_standard_v1-2_revision1.pdf
.. _HTML: https://fr.m.wikipedia.org/wiki/Hypertext_Markup_Language
.. _`GPL v2`: https://fr.m.wikipedia.org/wiki/Licence_publique_g%C3%A9n%C3%A9rale_GNU
.. _ici: https://hg.logilab.org/review/cubes/agape2
.. _là: https://www.cubicweb.org/project/agape2