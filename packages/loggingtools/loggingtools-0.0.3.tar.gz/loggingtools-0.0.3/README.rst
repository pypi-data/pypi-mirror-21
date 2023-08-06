Python Tools for Setting up Logging
-----------------------------------
|Travis| |Appveoyr| |Codecov| |QuantifiedCode| |Pyup| |Gitter| |Readthedocs|


.. |Pyup| image:: https://pyup.io/repos/github/jaantollander/loggingtools/shield.svg
   :target: https://pyup.io/repos/github/jaantollander/loggingtools/
   :alt: Updates

.. |QuantifiedCode| image:: https://www.quantifiedcode.com/api/v1/project/2eae31e4b5ce4a96b01394a3337a9fde/badge.svg
   :target: https://www.quantifiedcode.com/app/project/2eae31e4b5ce4a96b01394a3337a9fde
   :alt: Code issues

.. |Travis| image:: https://travis-ci.org/jaantollander/loggingtools.svg?branch=master
   :target: https://travis-ci.org/jaantollander/loggingtools
   :alt: Travis continuous intergration

.. |Appveoyr| image:: https://ci.appveyor.com/api/projects/status/4ix406f1jpgj952t?svg=true
   :target: https://ci.appveyor.com/project/jaantollander/loggingtools
   :alt: Appveoyr continuous intergration

.. |Codecov| image:: https://codecov.io/gh/jaantollander/loggingtools/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/jaantollander/loggingtools
   :alt: Codecov coverage hosting

.. |Gitter| image:: https://badges.gitter.im/loggingtools/Lobby.svg
   :alt: Join the chat at https://gitter.im/loggingtools/Lobby
   :target: https://gitter.im/loggingtools/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

.. |Readthedocs| image:: https://readthedocs.org/projects/loggingtools/badge/?version=latest
   :target: http://loggingtools.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

Loggingtools
------------

``setup_logging``

.. code-block:: python

   import logging
   from loggingtools import setup_logging
   setup_logging('logging.yml')
   logger = logging.getLogger('<your_logger>')
   ...


``log_with``

.. code-block:: python

   import logging
   from loggingtools import log_with

   ...  # setup your loggers

   logger = logging.getLogger('<your_logger>')

   @log_with(logger)
   def function(arg, arg2):
       ...


Installation
------------
Loggingtools can be installed through ``pip`` using command

.. code-block:: bash

   pip install loggingtools


Command Line Client
-------------------
::

   loggingtools config

Command line arguments

-n, --filename=logging  Filename for logging configuration
-f, --fileformat=yml    Fileformat: {yml, json}


References
----------
- https://docs.python.org/3/library/logging.html
- https://github.com/borntyping/python-colorlog
