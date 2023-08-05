==========
OVP News
==========

.. image:: https://img.shields.io/codeship/{uuid}/master.svg?style=flat-square
.. image:: https://img.shields.io/codecov/c/github/OpenVolunteeringPlatform/django-ovp-news.svg?style=flat-square
  :target: https://codecov.io/gh/OpenVolunteeringPlatform/django-ovp-news
.. image:: https://img.shields.io/pypi/v/ovp-news.svg?style=flat-square
  :target: https://pypi.python.org/pypi/ovp-news/

This module implements generic newsletter and digest emails for users and news.

Getting Started
---------------
Installing
""""""""""""""
1. Install django-ovp-news::

    pip install ovp-news

2. Add it to `INSTALLED_APPS` on `settings.py`

3. Add `rest_framework_jwt` to `INSTALLED_APPS`


Forking
""""""""""""""
If you have your own OVP installation and want to fork this module
to implement custom features while still merging changes from upstream,
take a look at `django-git-submodules <https://github.com/leonardoarroyo/django-git-submodules>`_.

Testing
---------------
To test this module

::

  python ovp_news/tests/runtests.py

Contributing
---------------
Please read `CONTRIBUTING.md <https://github.com/OpenVolunteeringPlatform/django-ovp-news/blob/master/CONTRIBUTING.md>`_ for details on our code of conduct, and the process for submitting pull requests to us.

Versioning
---------------
We use `SemVer <http://semver.org/>`_ for versioning. For the versions available, see the `tags on this repository <https://github.com/OpenVolunteeringPlatform/django-ovp-news/tags>`_. 

License
---------------
This project is licensed under the GNU AGPL License see the `LICENSE.md <https://github.com/OpenVolunteeringPlatform/django-ovp-news/blob/master/LICENSE.md>`_ file for details.
