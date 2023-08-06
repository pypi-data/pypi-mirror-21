Outil en ligne de commande pour intéragir avec le SAEM
------------------------------------------------------

`saemref-client` est un client en ligne de commande permettant d'intéragir avec
certains services web fournis par le référentiel SAEM. Son code source est
disponible sur framagit_.

.. _framagit: https://framagit.org/saemproject/saem-client/

Pour lister les commandes disponibles : ::

  ./saemref-client --help

ou pour obtenir les options spécifiques à une commande : ::

  ./saemref-client eac-download --help


Gestion des notices d'autorités
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pour récupérer les notices d'autorités : ::

  ./saemref-client eac-download https://demo.logilab.fr/saem-demo

Cette commande va rappatrier les notices d'autorités publiques du référentiels sous forme de
fichiers XML au format EAC qui seront mis dans le répertoire de travail.

Pour envoyer une nouvelle notice d'autorités au format EAC dans un fichier ``fichier-eac.xml`` : ::

  ./saemref-client eac-upload https://demo.logilab.fr/saem-demo fichier-eac.xml

Cette commande s'attend à trouver dans le répertoire de travail un fichier ``cubicweb.yaml``
comportant les identifiants de connexion au format YAML, par exemple : ::

  id: token-arkheia
  secret: 11e9ae06d7754a89a13d0e7245bc6132320cb081813b4d229a4d6

Gestion des vocabulaires
~~~~~~~~~~~~~~~~~~~~~~~~

Pour récupérer les concepts d'un vocabulaire : ::

  ./saemref-client skos-download https://demo.logilab.fr/saem-demo 23578/v000200007

Cette commande va récupérer les concepts du vocabulaire ayant l'identifiant ARK
``23578/v000200007``, sous forme de fic hier XML au format SKOS qui serons mis dans un
sous-répertoire ``23578-v000200007`` du répertoire de travail.

Installation
~~~~~~~~~~~~

Si vous avez une distribution python, vous pouvez simplement l'installer avec `pip` : ::

  pip install saemref-client

Sinon, sur Windows il suffit de télécharger et extraire l'archive
https://ci.appveyor.com/api/projects/logilab/saem-client/artifacts/saemref-client.zip
et de lancer `saemref-client\\saemref-client.exe`
