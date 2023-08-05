wq.start: Project template and scaffolding tools
================================================

``wq.start`` provides a simple command-line interface (``wq start``) for
starting a new project with the `wq framework <https://wq.io/>`__, with
`wq.app <https://wq.io/wq.app>`__ for the front end and
`wq.db <https://wq.io/wq.db>`__ as the backend component. ``wq.start``
also provides commands for generating a default set of offline-capable
list, detail, and edit templates. The templates can be generated for
existing Django models (via ``wq maketemplates``), or both the models
and the templates can be generated from an ODK-style
`XLSForm <http://xlsform.org>`__ (via ``wq addform``).

|Latest PyPI Release| |Release Notes| |License| |GitHub Stars| |GitHub
Forks| |GitHub Issues|

|Travis Build Status| |Python Support| |Django Support|

Usage
~~~~~

.. code:: sh

    pip3 install wq
    wq start <projectname> [directory]
    cd <projectname>/db
    wq addform ~/my-odk-form.xlsx

See the `Getting Started <https://wq.io/docs/setup>`__ docs for more
information.

Commands
~~~~~~~~

-  ``wq start <projectname> [directory]``: Create a new Django project
   (from the `wq Django
   template <https://github.com/wq/wq-django-template>`__)
-  ``wq addform ~/myodk-form.xlsx``: Create a new Django app from the
   provided XLSForm (uses
   `xlsform-converter <https://github.com/wq/xlsform-converter>`__)
-  ``wq maketemplates``: Create templates for Django models registered
   with `wq.db.rest <https://wq.io/docs/about-rest>`__

.. |Latest PyPI Release| image:: https://img.shields.io/pypi/v/wq.start.svg
   :target: https://pypi.python.org/pypi/wq.start
.. |Release Notes| image:: https://img.shields.io/github/release/wq/wq.start.svg
   :target: https://github.com/wq/wq.start/releases
.. |License| image:: https://img.shields.io/pypi/l/wq.start.svg
   :target: https://wq.io/license
.. |GitHub Stars| image:: https://img.shields.io/github/stars/wq/wq.start.svg
   :target: https://github.com/wq/wq.start/stargazers
.. |GitHub Forks| image:: https://img.shields.io/github/forks/wq/wq.start.svg
   :target: https://github.com/wq/wq.start/network
.. |GitHub Issues| image:: https://img.shields.io/github/issues/wq/wq.start.svg
   :target: https://github.com/wq/wq.start/issues
.. |Travis Build Status| image:: https://img.shields.io/travis/wq/wq.start/master.svg
   :target: https://travis-ci.org/wq/wq.start
.. |Python Support| image:: https://img.shields.io/pypi/pyversions/wq.start.svg
   :target: https://pypi.python.org/pypi/wq.start
.. |Django Support| image:: https://img.shields.io/badge/Django-1.8%2C%201.9%2C%201.10-blue.svg
   :target: https://pypi.python.org/pypi/wq.start
