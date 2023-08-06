Kibitzr - Personal Network Assistant
=====================================

Kibitzr is like a secret twin brother who does routine tasks and asks for nothing in return.

* :ref:`Install <install>` with ``pip install kibitzr`` (Works with both Python 2 and 3)
* :ref:`Configure <configuration>` recurrent checks in ``kibitzr.yml``
* Put credentials in ``kibitzr-creds.yml``
* Launch with ``kibitzr``
* Problems? Ask in Github issues_, or gitter_
* Fork_

Kibitzr is built with extendability in mind.

For simple HTTP requests it uses `Python requests`_.
And for complex browser interactions it offers headless Firefox with Selenium_ scenarios.
Or go wild with bash_ scripts (linux only).

Send notifications through e-mail, Slack or gitter (open issue_ for new notifier).
Or build your own notifier in Python_ or bash_.

.. _gitter: https://gitter.im/kibitzr/Lobby
.. _Python requests: http://docs.python-requests.org/en/master/
.. _issue: https://github.com/kibitzr/kibitzr/issues/new
.. _issues: https://github.com/kibitzr/kibitzr/issues/
.. _Python: https://www.python.org/
.. _bash: https://www.gnu.org/software/bash/
.. _Fork: https://github.com/kibitzr/kibitzr/
.. _Selenium: http://www.seleniumhq.org/

.. include:: overview.rst

.. toctree::
   :maxdepth: 1

   installation
   configuration
   usage
   transforms
   notifiers
   recipes
   contributing
