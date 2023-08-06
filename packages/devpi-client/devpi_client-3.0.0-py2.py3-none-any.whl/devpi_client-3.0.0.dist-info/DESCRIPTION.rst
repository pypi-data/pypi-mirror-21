devpi-client: commands for python packaging and testing
===============================================================

The "devpi" command line tool is typically used in conjunction
with `devpi-server <http://pypi.python.org/pypi/devpi-server>`_.
It allows to upload, test and install packages from devpi indexes.
See http://doc.devpi.net for quickstart and more documentation.

* `issue tracker <https://github.com/devpi/devpi/issues>`_, `repo
  <https://github.com/devpi/devpi>`_

* IRC: #devpi on freenode, `mailing list
  <https://mail.python.org/mm3/mailman3/lists/devpi-dev.python.org/>`_ 

* compatibility: {win,unix}-py{27,34,35,36,py}





Changelog
=========

3.0.0 (2017-04-23)
------------------

- add ``-r, --requirement`` option to `devpi install` to use requirements file.

- add ``--pip-set-trusted=[yes|no|auto]`` option to ``devpi use`` to add or
  remove ``trusted-host`` option to pip configuration when ``--set-cfg`` is
  also given. ``auto`` is the default and sets it for http servers and https
  which do not pass certificate validation.
  Thanks to Andrew Leech for the PR.

- add ``devpiclient_get_password`` hook which allows plugins to return a
  password based on username and server url.

- drop support for Python 2.6.

- drop support for devpi-server < 4.0.0.


2.7.0 (2016-10-14)
------------------

- fix issue268: upload of docs with PEP440 version strings now works

- fix issue362: close requests session, so all sockets are closed on exit

- add ``--no-upload`` option to ``devpi test`` to skip upload of tox results


2.6.4 (2016-07-15)
------------------

- fix issue337: ``devpi upload`` for packages that produce output during build
  now works.


2.6.3 (2016-05-13)
------------------

- update devpi-common requirement, so devpi-client can be installed in the same
  virtualenv as devpi-server 4.0.0.


2.6.2 (2016-04-28)
------------------

- ``devpi upload`` failed to use basic authentication and client certificate
  information.



