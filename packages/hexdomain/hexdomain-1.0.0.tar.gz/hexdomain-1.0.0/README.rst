hexdomain
=========

``hexdomain`` reads words from a `words file <https://en.wikipedia.org/wiki/Words_(Unix)>`_ and converts them to `hexspeak <https://en.wikipedia.org/wiki/Hexspeak>`_ domain names.

For example, "code" becomes ``c0.de`` and "coffee" becomes ``c0ff.ee``.

Usage
-----

By default, ``hexdomain`` reads words from ``/usr/share/dict/words``::

    hexdomain

You can specify an alternate word list as well::

    hexdomain /path/to/my/words

You can also provide custom substitutions instead of the built-in ones; see ``hexdomain -h`` for details.

Installation
------------

Install with pip::

    pip install hexdomain

Licence
-------

MIT
