kotti_google_analytics
************************

This extension allows Google Analytics to Kotti, in order to track users and sessions on your site.
In addition, it adds Google Analytics Visualizations for reporting by using
`Google Analytics Embed API`_.

Example of Google Analytics Visualization:
--------------------------------------------

.. image:: https://static.raymondcamden.com/images/wp-content/uploads/2015/07/shot11.png

This is an extension to Kotti that allows to add foo to your site.

|pypi|_
|downloads_month|_
|license|_
|build_status_stable|_


.. _Google Analytics Embed API: https://ga-dev-tools.appspot.com/

.. |pypi| image:: https://img.shields.io/pypi/v/kotti_google_analytics.svg?style=flat-square
.. _pypi: https://pypi.python.org/pypi/kotti_google_analytics/

.. |downloads_month| image:: https://img.shields.io/pypi/dm/kotti_google_analytics.svg?style=flat-square
.. _downloads_month: https://pypi.python.org/pypi/kotti_google_analytics/

.. |license| image:: https://img.shields.io/pypi/l/kotti_google_analytics.svg?style=flat-square
.. _license: http://www.repoze.org/LICENSE.txt

.. |build_status_stable| image:: https://img.shields.io/travis/b4oshany/kotti_google_analytics/production.svg?style=flat-square
.. _build_status_stable: http://travis-ci.org/b4oshany/kotti_google_analytics

`Find out more about Kotti`_

Development happens at https://github.com/b4oshany/kotti_google_analytics

.. _Find out more about Kotti: http://pypi.python.org/pypi/Kotti

Setup
=====


To enable the extension in your Kotti site, activate the configurator::

    kotti.configurators =
	    kotti_controlpanel.kotti_configure
        kotti_google_analytics.kotti_configure
        
    kotti_google_analytics.tracking_id = track_id_here


Database upgrade
================

If you are upgrading from a previous version you might have to migrate your
database.  The migration is performed with `alembic`_ and Kotti's console script
``kotti-migrate``. To migrate, run
``kotti-migrate upgrade --scripts=kotti_google_analytics:alembic``.

For integration of alembic in your environment please refer to the
`alembic documentation`_. If you have problems with the upgrade,
please create a new issue in the `tracker`_.

Development
===========

|build_status_master|_

.. |build_status_master| image:: https://img.shields.io/travis/b4oshany/kotti_google_analytics/master.svg?style=flat-square
.. _build_status_master: http://travis-ci.org/b4oshany/kotti_google_analytics

Contributions to kotti_google_analytics are highly welcome.
Just clone its `Github repository`_ and submit your contributions as pull requests.

.. _alembic: http://pypi.python.org/pypi/alembic
.. _alembic documentation: http://alembic.readthedocs.org/en/latest/index.html
.. _tracker: https://github.com/b4oshany/kotti_google_analytics/issues
.. _Github repository: https://github.com/b4oshany/kotti_google_analytics

Known Issues
==============

Pip can't install googleanalystics 0.22.3::

   pip install https://github.com/b4oshany/google-analytics/tarball/master#egg=googleanalytics-0.22.3
