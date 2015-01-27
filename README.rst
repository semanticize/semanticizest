Semanticizer, standalone
========================

Semanticizest is a library for doing entity linking, also known as
semantic linking or semanticizing: you feed it text, and it outputs links
to pertinent Wikipedia concepts. You can use these links as a "semantic
representation" of the text for NLP or machine learning, or just to provide
some links to background info on the Wikipedia.


Installation
------------

* ``pip install -r requirements.txt``
* ``pip install .``


Usage
-----

To train a semanticizer, download a Wikipedia database dump from
``https://dumps.wikimedia.org/``. Then issue::

    python -m semanticizest.parse_wikidump <dump> <model-filename>

The result will be a semanticizer model (in SQLite 3 format, if you must know).

Alternatively, you can use the --download flag to instruct semanticizest to 
download the LATEST wikipedia dump. For example:

    python -m semanticizest.parse_wikidump --download scowiki sco.model

will download ``https://dumps.wikimedia.org/scowiki/latest/scowiki-latest-pages-articles.xml.bz2``
to ``scowiki.xml.bz2`` and construct the model from it.

Documentation
-------------

The documentation can be found at http://semanticizest.readthedocs.org/


Copyright and license
---------------------

Copyright 2014 University of Amsterdam/Netherlands eScience Center.
The license for the semanticizest is `Apache License, Version 2.0`_.
See the file LICENSE for details.

.. _`Apache License, Version 2.0`:
   http://www.apache.org/licenses/LICENSE-2.0.html
