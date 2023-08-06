kotti_alert
***********

This is an extension to Kotti that allows you to add alerts and other notifications to your site.

|pypi|_
|downloads_month|_
|license|_
|build_status_stable|_

.. |pypi| image:: https://img.shields.io/pypi/v/kotti_alert.svg?style=flat-square
.. _pypi: https://pypi.python.org/pypi/kotti_alert/

.. |downloads_month| image:: https://img.shields.io/pypi/dm/kotti_alert.svg?style=flat-square
.. _downloads_month: https://pypi.python.org/pypi/kotti_alert/

.. |license| image:: https://img.shields.io/pypi/l/kotti_alert.svg?style=flat-square
.. _license: http://www.repoze.org/LICENSE.txt

.. |build_status_stable| image:: https://travis-ci.org/b4oshany/kotti_alert.svg?branch=master
.. _build_status_stable: https://travis-ci.org/b4oshany/kotti_alert

`Find out more about Kotti`_

Development happens at https://github.com/b4oshany/kotti_alert

.. _Find out more about Kotti: http://pypi.python.org/pypi/Kotti

Setup
=====

To enable the extension in your Kotti site, activate the configurator::

    kotti.configurators =
        kotti_alert.kotti_configure

Database upgrade
================

If you are upgrading from a previous version you might have to migrate your
database.  The migration is performed with `alembic`_ and Kotti's console script
``kotti-migrate``. To migrate, run
``kotti-migrate upgrade --scripts=kotti_alert:alembic``.

For integration of alembic in your environment please refer to the
`alembic documentation`_. If you have problems with the upgrade,
please create a new issue in the `tracker`_.

Development
===========

|build_status_master|_

.. |build_status_master| image:: https://img.shields.io/travis/b4oshany/kotti_alert/master.svg?style=flat-square
.. _build_status_master: http://travis-ci.org/b4oshany/kotti_alert

Contributions to kotti_alert are highly welcome.
Just clone its `Github repository`_ and submit your contributions as pull requests.

.. _alembic: http://pypi.python.org/pypi/alembic
.. _alembic documentation: http://alembic.readthedocs.org/en/latest/index.html
.. _tracker: https://github.com/b4oshany/kotti_alert/issues
.. _Github repository: https://github.com/b4oshany/kotti_alert
