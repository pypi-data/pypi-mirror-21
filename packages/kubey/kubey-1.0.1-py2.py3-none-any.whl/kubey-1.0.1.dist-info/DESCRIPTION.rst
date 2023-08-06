===============================
Kubey
===============================


.. image:: https://img.shields.io/pypi/v/kubey.svg
        :target: https://pypi.python.org/pypi/kubey

.. image:: https://img.shields.io/travis/bradrf/kubey.svg
        :target: https://travis-ci.org/bradrf/kubey

.. image:: https://readthedocs.org/projects/kubey/badge/?version=latest
        :target: https://kubey.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Simple wrapper to help find specific Kubernetes pods and containers and run asynchronous commands.


* Free software: MIT license
* Documentation: https://kubey.readthedocs.io.


Features
--------

* TODO

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


=======
History
=======

1.0.0 (2017-04-23)
------------------

* Refactor everything into real objects for cleaner separation of concerns.
* Add events report.
* Rework raw kubectl requests and usage.


0.4.0 (2017-04-14)
------------------

* Fix interactive
* Collect tabular output for each_pod


0.3.0 (2017-04-04)
------------------

* Fix health report
* Highlight "warning level" percentages in health
* Fix quoting to allow remote glob expansion


0.2.0 (2017-04-02)
------------------

* Refactor into object for coding w/ Kubey.
* Add initial tests.
* Add pass-thru calling.


0.1.0 (2017-03-18)
------------------

* First release on PyPI.


