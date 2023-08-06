========================================
structlog: Structured Logging for Python
========================================

.. image:: https://readthedocs.org/projects/structlog/badge/?version=stable
   :target: https://structlog.readthedocs.io/en/stable/?badge=stable
   :alt: Documentation Status

.. image:: https://travis-ci.org/hynek/structlog.svg?branch=master
   :target: https://travis-ci.org/hynek/structlog

.. image:: https://codecov.io/github/hynek/structlog/branch/master/graph/badge.svg
  :target: https://codecov.io/github/hynek/structlog
  :alt: Test Coverage

.. image:: https://www.irccloud.com/invite-svg?channel=%23structlog&amp;hostname=irc.freenode.net&amp;port=6697&amp;ssl=1
   :target: https://www.irccloud.com/invite?channel=%23structlog&amp;hostname=irc.freenode.net&amp;port=6697&amp;ssl=1

.. begin

``structlog`` makes logging in Python less painful and more powerful by adding structure to your log entries.

It's up to you whether you want ``structlog`` to take care about the **output** of your log entries or whether you prefer to **forward** them to an existing logging system like the standard library's ``logging`` module.
*No* `monkey patching <https://en.wikipedia.org/wiki/Monkey_patch>`_ involved in either case.


Easier Logging
==============

You can stop writing prose and start thinking in terms of an event that happens in the context of key/value pairs:

.. code-block:: pycon

   >>> from structlog import get_logger
   >>> log = get_logger()
   >>> log.info("key_value_logging", out_of_the_box=True, effort=0)
   2016-04-20 16:20.13 key_value_logging              effort=0 out_of_the_box=True

Each log entry is a meaningful dictionary instead of an opaque string now!


Data Binding
============

Since log entries are dictionaries, you can start binding and re-binding key/value pairs to your loggers to ensure they are present in every following logging call:

.. code-block:: pycon

   >>> log = log.bind(user="anonymous", some_key=23)
   >>> log = log.bind(user="hynek", another_key=42)
   >>> log.info("user.logged_in", happy=True)
   2016-04-20 16:20.13 user.logged_in                 another_key=42 happy=True some_key=23 user='hynek'


Powerful Pipelines
==================

Each log entry goes through a `processor pipeline <http://www.structlog.org/en/stable/processors.html>`_ that is just a chain of functions that receive a dictionary and return a new dictionary that gets fed into the next function.
That allows for simple but powerful data manipulation:

.. code-block:: python

   def timestamper(logger, log_method, event_dict):
       """Add a timestamp to each log entry."""
       event_dict["timestamp"] = time.time()
       return event_dict

There are `plenty of processors <http://www.structlog.org/en/stable/api.html#module-structlog.processors>`_ for most common tasks coming with ``structlog``:

- Collectors of `call stack information <http://www.structlog.org/en/stable/api.html#structlog.processors.StackInfoRenderer>`_ ("How did this log entry happen?"),
- …and `exceptions <http://www.structlog.org/en/stable/api.html#structlog.processors.format_exc_info>`_ ("What happened‽").
- Unicode encoders/decoders.
- Flexible `timestamping <http://www.structlog.org/en/stable/api.html#structlog.processors.TimeStamper>`_.



Formatting
==========

``structlog`` is completely flexible about *how* the resulting log entry is emitted.
Since each log entry is a dictionary, it can be formatted to **any** format:

- A colorful key/value format for `local development <http://www.structlog.org/en/stable/development.html>`_,
- `JSON <http://www.structlog.org/en/stable/api.html#structlog.processors.JSONRenderer>`_ for easy parsing,
- or some standard format you have parsers for like nginx or Apache httpd.

Internally, formatters are processors whose return value (usually a string) is passed into loggers that are responsible for the output of your message.
``structlog`` comes with multiple useful formatters out of-the-box.


Output
======

``structlog`` is also very flexible with the final output of your log entries:

- A **built-in** lightweight printer like in the examples above.
  Easy to use and fast.
- Use the **standard library**'s or **Twisted**'s logging modules for compatibility.
  In this case ``structlog`` works like a wrapper that formats a string and passes them off into existing systems that won't ever know that ``structlog`` even exists.
  Or the other way round: ``structlog`` comes with a ``logging`` formatter that allows for processing third party log records.
- Don't format it to a string at all!
  ``structlog`` passes you a dictionary and you can do with it whatever you want.
  Reported uses cases are sending them out via network or saving them in a database.

.. -end-


Project Information
===================

``structlog`` is dual-licensed under `Apache License, version 2 <http://choosealicense.com/licenses/apache/>`_ and `MIT <http://choosealicense.com/licenses/mit/>`_, available from `PyPI <https://pypi.python.org/pypi/structlog/>`_, the source code can be found on `GitHub <https://github.com/hynek/structlog>`_, the documentation at http://www.structlog.org/.

``structlog`` targets Python 2.7, 3.4 and newer, and PyPy.

If you need any help, visit us on ``#structlog`` on `Freenode <https://freenode.net>`_!


Release Information
===================

17.1.0 (2017-04-24)
-------------------

The main features of this release are massive improvements in standard library's ``logging`` integration.
Have a look at the updated `standard library chapter <http://www.structlog.org/en/stable/standard-library.html>`_ on how to use them!
Special thanks go to
`Fabian Büchler <https://github.com/fabianbuechler>`_,
`Gilbert Gilb's <https://github.com/gilbsgilbs>`_,
`Iva Kaneva <https://github.com/if-fi>`_,
`insolite <https://github.com/insolite>`_,
and `sky-code <https://github.com/sky-code>`_,
that made them possible.


Backward-incompatible changes:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- The default renderer now is ``structlog.dev.ConsoleRenderer`` if you don't configure ``structlog``.
  Colors are used if available and human-friendly timestamps are prepended.
  This is in line with our backward `compatibility policy <http://www.structlog.org/en/stable/backward-compatibility.html>`_ that explicitly excludes default settings.


Changes:
^^^^^^^^

- Added ``structlog.stdlib.render_to_log_kwargs()``.
  This allows you to use ``logging``-based formatters to take care of rendering your entries.
  `#98 <https://github.com/hynek/structlog/issues/98>`_
- Added ``structlog.stdlib.ProcessorFormatter`` which does the opposite:
  This allows you to run ``structlog`` processors on arbitrary ``logging.LogRecords``.
  `#79 <https://github.com/hynek/structlog/issues/79>`_
  `#105 <https://github.com/hynek/structlog/issues/105>`_
- UNIX epoch timestamps from ``structlog.processors.TimeStamper`` are more precise now.
- Added *repr_native_str* to ``structlog.processors.KeyValueRenderer`` and ``structlog.dev.ConsoleRenderer``.
  This allows for human-readable non-ASCII output on Python 2 (``repr()`` on Python 2 haves like ``ascii()`` on Python 3 in that regard).
  As per compatibility policy, it's on (original behavior) in ``KeyValueRenderer`` and off (humand-friendly behavior) in ``ConsoleRenderer``.
  `#94 <https://github.com/hynek/structlog/issues/94>`_
- Added *colors* argument to ``structlog.dev.ConsoleRenderer`` and made it the default renderer.
  `#78 <https://github.com/hynek/structlog/pull/78>`_
- Fixed bug with Python 3 and ``structlog.stdlib.BoundLogger.log()``.
  Error log level was not reproductible and was logged as exception one time out of two.
  `#92 <https://github.com/hynek/structlog/pull/92>`_
- Positional arguments are now removed even if they are empty.
  `#82 <https://github.com/hynek/structlog/pull/82>`_

`Full changelog <http://www.structlog.org/en/stable/changelog.html>`_.

Authors
=======

``structlog`` is written and maintained by `Hynek Schlawack <https://hynek.me/>`_.
It’s inspired by previous work done by `Jean-Paul Calderone <http://as.ynchrono.us/>`_ and `David Reid <https://dreid.org/>`_.

The development is kindly supported by `Variomedia AG <https://www.variomedia.de/>`_.

A full list of contributors can be found on GitHub’s `overview <https://github.com/hynek/structlog/graphs/contributors>`_.
Some of them disapprove of the addition of thread local context data. :)


