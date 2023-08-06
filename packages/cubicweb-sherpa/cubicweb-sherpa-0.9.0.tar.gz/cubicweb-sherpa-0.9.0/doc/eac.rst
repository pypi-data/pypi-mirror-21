=======
EAC-CPF
=======

Le référentiel fournit une implémentation de EAC-CPF_ relativement complète. Les notices d'autorités
peuvent être créés ou importés directement dans l'interface web ou bien importés en ligne de
commande. Pour le moment, l'interface utilisateur permet néanmoins d'éditer qu'un petit
sous-ensemble du modèles.

.. section sur les balises supportées ou non
.. include-url:: https://hg.logilab.org/review/cubes/eac/raw-file/tip/doc/supported.rst


Import de notices d'autorités en ligne de commande
==================================================

Pour importer un fichier EAC-CPF, vous pouvez utiliser la commande 'eac-import' de `cubicweb-ctl` :

::

    CW_MODE=user cubicweb-ctl eac-import sherpa fichier.rdf


Export des notices en EAC
=========================

Pour chaque forme du nom, l'attribute 'parties' est découpée selon le caractère ", " puis chaque
élément est inséré dans une balise ``part``. C'est le traitement symétrique à ce qui est fait durant
l'import (concaténation des différentes balises ``part`` avec le séparateur ", ")