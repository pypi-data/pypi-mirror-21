===================================
Modèle de sécurité de l'application
===================================

Accès anonyme
-------------

Les utilisateurs anonymes peuvent voir toutes les données métiers mais ne peuvent rien modifier.


Utilisateurs "standards"
------------------------

.. warning::

  Hormis l'utilisateur dédié aux accès anonymes (en général "anon"), tous les utilisateurs doivent
  être dans le groupe "utilisateurs".

Un utilisateur standard (dans le groupe 'utilisateurs') peut ajouter et mettre à jour des notices
d'autorité, profils SEDA et unités documentaires.


Administrateurs
---------------

Les utilisateurs qui sont ajoutés dans le groupe "administrateurs" ont des droits supplémentaires
sur la plate-forme, notamment :

* ajouter et modifier des utilisateurs ;

* ajouter et modifier des vocabulaires.
