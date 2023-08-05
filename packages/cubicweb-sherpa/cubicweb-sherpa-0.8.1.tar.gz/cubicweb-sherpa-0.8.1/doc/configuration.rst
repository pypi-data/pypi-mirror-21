Gestion de configuration
------------------------

L'application est construite sur le cadre applicatif CubicWeb_. À ce titre, c'est elle même un
"cube" (i.e. un composant CubicWeb), dont la structure générale est décrite ici_.

Elle s'appuie sur les composants logiciels suivants :

* le `cadre applicatif CubicWeb`_ lui-même (>= 3.23) ;

* `cubicweb-seda`_, cube implémentant le modèle de données SEDA 2, complet et simplifié, ainsi que
  les fonctions d'export ;

* `cubicweb-registration`_, cube implémentant la création de compte sans passer par un
  administrateur ;

* `cubicweb-rememberme`_ , cube permettant de rester connecter d'une fois à l'autre.

Les dépendances de ces logiciels ne sont pas indiquées ici, mais comprennent notamment le cube
`skos`_ qui implémente le modèle de données et l'import / export du format SKOS_ qui est utilisé
pour la gestion des thésaurus et autres vocabulaires contrôlés.



.. _CubicWeb: https://cubicweb.org
.. _ici: http://cubicweb.readthedocs.io/en/3.23/book/devrepo/cubes/layout/
.. _`cadre applicatif CubicWeb`: https://www.cubicweb.org/project/cubicweb
.. _`cubicweb-seda`: https://www.cubicweb.org/project/cubicweb-seda
.. _`cubicweb-registration`: https://www.cubicweb.org/project/cubicweb-registration
.. _`cubicweb-rememberme`: https://www.cubicweb.org/project/cubicweb-rememberme
.. _`skos`: https://www.cubicweb.org/project/cubicweb-skos
.. _SKOS_: https://fr.m.wikipedia.org/wiki/Simple_Knowledge_Organization_System
