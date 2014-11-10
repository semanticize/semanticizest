Semanticizer, the Next Generation
=================================

Goal of the semanticizest is to have a working, maintainable,
librarized version of Daan's original semanticizer.


Usage
-----

To train a semanticizer, download a Wikipedia database dump from
``https://dumps.wikimedia.org/``. Then issue::

    python -m semanticizest.parse_wikidump <dump> <model-filename>

The result will be a semanticizer model (in SQLite 3 format, if you must know).


License
-------

The license for the semanticizest is `Apache License, Version 2.0`_.

.. _`Apache License, Version 2.0`:
   http://www.apache.org/licenses/LICENSE-2.0.html
