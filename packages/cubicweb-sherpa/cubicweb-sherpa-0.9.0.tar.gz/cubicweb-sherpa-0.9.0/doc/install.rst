============
Installation
============

La doc suivante suppose que vous êtes sur une distribution Red-Hat / CentOS, mais cela pourrait
aussi être une distribution Debian / Ubuntu en utilisant ``apt-get`` plutôt que ``yum``. La
principale condition est d'utiliser un système avec une version récente de python (2.7) et ``pip``.

Le mieux est généralement de commencer par installer ``virtualenv`` avec ``pip`` afin d'avoir la
dernière version disponible : ::

  pip install --upgrade virtualenv


Configuration du serveur PostgreSQL
-----------------------------------

Si vous n'en n'avez pas encore un disponible, il faut commencer par installer un serveur PostgreSQL
(pas nécessairement sur la même machine que le référentiel). Sur une distribution Red-Hat / CentOS,
il faut commencer par installer les paquets suivants :

::

    yum install postgresql94-contrib
    yum install postgresql94-plpython
    yum install postgresql94-server
    yum install mailcap # pour /etc/mime.types

Créer et démarrer un *cluster* PostgreSQL

::

    service postgresql-9.4 initdb
    service postgresql-9.4 start

En tant qu'utilisateur ``postgres`` (par exemple ``su - postgres``),
créer un nouveau compte d'accès à Postgres :

::

    createuser --superuser --login --pwprompt cubicweb

De retour en ``root``, éditer le fichier ``/var/lib/pgsql/9.4/data/pg_hba.conf``
pour donner les droits d'accès à l'utilisateurs ``cubicweb`` fraichement créé :

::

    local   all   cubicweb    md5


.. warning::

    L'ordre des directives de ce fichier est important. La directive concernant
    l'utilisateur ``cubicweb`` doit précéder celles déjà présentes dans le
    fichier. Dans le cas contraire, elle sera ignorée.

Enfin, on relance PostgreSQL pour qu'il prenne en compte les modifications :

::

    service postgresql-9.4 reload

Pour s'assurer du bon fonctionnement de PostgreSQL et du rôle ``cubicweb``, la
commande suivante doit afficher le contenu du *cluster* sans erreur :

::

    psql -U cubicweb -l


Installation de l'application
-----------------------------

Nous recommandons d'installer le code du référentiel avec un utilisateur
standard (pas *root*) :

::

    adduser sherpa
    su - sherpa

et dans un virtualenv_, qu'il convient donc de créer puis d'activer :

::
    virtualenv sherpa-venv
    . sherpa-venv/bin/activate

Par la suite, nous supposerons que vous tapez les commandes indiquées en tant qu'utilisateur
`sherpa` et avec le *virtualenv* activé.

Installer le référentiel :

::

    pip install cubicweb-sherpa


Création de l'instance
----------------------

Une fois le cube sherpa et ses dépendances installées, il reste à créer une
instance de celui-ci :

::

  CW_MODE=user cubicweb-ctl create sherpa sherpa

.. note ::

    La phase finale de création prend quelques minutes, afin de remplir la base
    avec quelques données nécessaires au bon fonctionnement de l'application.

* Laisser le choix par défaut à toutes les questions sauf pour la question "Allow anonymous access"
  à laquelle il convient de répondre 'Y' pour autoriser l'accès site sans avoir à s'authentifier.

.. warning ::

    L'accès anonyme s'appuie sur un utilisateur en base, défini par les options ``anonymous-user``
    et ``anonymous-password`` du fichier ``all-in-one.conf`` de l'instance. Si vous souhaitez les
    modifier (par exemple modifier son mot de passe) il faut synchroniser l'utilisateur associé en
    base de données en fonction des valeurs données aux options dans le fichier (par exemple
    ``cnx.find('CWUser', login='anon').cw_set(upassword=u'new password')``)


* Choisir un login / mot de passe administrateur sécurisé (admin/admin est une
  mauvaise idée, nous recommandons d'installer le paquet ``pwgen`` et de
  générer un mot de passe aléatoire avec la commande ``pwgen 20``).

Selon votre configuration postgres, vous pouvez avoir à modifier le fichier sources pour y spécifier
les informations de connexion au serveur (hôte, port, utilisateur et mot de passe). Le plus simple
est de répondre non à la question "Run db-create to create the system database ?", d'éditer le
fichier `~/etc/cubicweb.d/sherpa/sources` puis de reprendre le processus d'initialisation en
tapant :

::

  CW_MODE=user cubicweb-ctl db-create sherpa

Vous pouvez maintenant lancer l'instance :

::

  CW_MODE=user cubicweb-ctl pyramid sherpa

L'instance est désormais lancée et disponible sur le port 8080.

Pour une instance de production, il est recommandé d'utilisé un serveur d'application WSGI tel que
`gunicorn`_ et un superviseur tel que `supervisor`_.


Mise à jour de l'instance
=========================

.. warning::

  Il y aura donc une interruption de service pendant cette opération

Lors qu'une nouvelle version est livrée, il faut commencer par mettre à jour le code de
l'application. Le plus simple pour cela est de supprimer le *virtualenv* et de le recréer. Si vous
avez installé le référentiel avec pip :

::

    # Ctrl-C pour couper l'instance qui tourne
    rm -rf sherpa-venv
    virtualenv sherpa-venv
    . sherpa-venv/bin/activate
    pip install cubicweb-sherpa

Puis il reste à mettre à jour l'instance CubicWeb. Pour une installation avec pip :

::

    CW_MODE=USER cubicweb-ctl upgrade sherpa
    CW_MODE=USER cubicweb-ctl pyramid sherpa

La commande `cubicweb-ctl upgrade` pose un certain nombre de questions, auxquelles il faut toujours
répondre par oui (en tapant 'y' ou Entrée directement). Un backup de la base de données est effectué
avant la migration afin de pouvoir rejouer une migration en cas de problement.

.. _pip: https://pip.pypa.io/
.. _virtualenv: https://virtualenv.pypa.io/
.. _gunicorn: http://gunicorn.org/
.. _supervisor: http://supervisord.org/
