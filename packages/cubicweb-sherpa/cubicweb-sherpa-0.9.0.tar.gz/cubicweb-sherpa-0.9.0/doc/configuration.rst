Gestion de configuration
------------------------

L'application est construite sur le cadre applicatif CubicWeb_. À ce titre, c'est elle même un
"cube" (i.e. un composant CubicWeb), dont la structure générale est décrite ici_.

Elle s'appuie sur les composants logiciels suivants :

* le cadre applicatif CubicWeb_ lui-même (>= 3.24) ;

* `cubicweb-sherpa`_, l'application SHERPA proprement dite, agrégeant les différents composants
  ci-dessous ;

* `cubicweb-seda`_, cube implémentant le modèle de données SEDA 2, complet et simplifié, ainsi que
  les fonctions d'export ;

* `cubicweb-eac`_, cube implémentant le modèle de données EAC, et permettant notamment d'importer
  puis de réexporter les notices d'autorités ;

* `cubicweb-skos`_, cube implémentant le modèle de données SKOS, et permettant notamment d'importer
  puis de réexporter des vocabulaires au format SKOS_ pour la gestion des thésaurus et autres
  vocabulaires contrôlés ;

* `cubicweb-registration`_ , cube permettant de se créer un compte sur la plateforme sans passer par
  un administrateur ;

* `cubicweb-forgotpwd`_ , cube permettant de remettre à zéro son mot de passe en cas d'oubli ;

* `cubicweb-rememberme`_ , cube permettant de rester connecter d'une fois à l'autre.



.. _CubicWeb: https://cubicweb.org
.. _ici: http://cubicweb.readthedocs.io/en/3.23/book/devrepo/cubes/layout/
.. _`cadre applicatif CubicWeb`: https://www.cubicweb.org/project/cubicweb
.. _`cubicweb-sherpa`: https://www.cubicweb.org/project/cubicweb-sherpa
.. _`cubicweb-seda`: https://www.cubicweb.org/project/cubicweb-seda
.. _`cubicweb-eac`: https://www.cubicweb.org/project/cubicweb-eac
.. _`cubicweb-skos`: https://www.cubicweb.org/project/cubicweb-skos
.. _`cubicweb-forgotpwd`: https://www.cubicweb.org/project/cubicweb-forgotpwd
.. _`cubicweb-registration`: https://www.cubicweb.org/project/cubicweb-registration
.. _`cubicweb-rememberme`: https://www.cubicweb.org/project/cubicweb-rememberme
.. _`skos`: https://www.cubicweb.org/project/cubicweb-skos
.. _SKOS_: https://fr.m.wikipedia.org/wiki/Simple_Knowledge_Organization_System
