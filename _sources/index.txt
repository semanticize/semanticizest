.. semanticizest documentation master file, created by
   sphinx-quickstart on Tue Nov 18 15:37:15 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to semanticizest's documentation!
=========================================

semanticizest (Semanticizer, STandalone) is a library for entity
linking (also known as wikification.)


Quick usage
-----------

First we need to create a model for the semanticizer. The following
command will download and read a wikipedia dump (in this case the
Limburgish wiki) and subsequently create and store the corresponding
model.

.. code:: bash

    python -m semanticizest.parse_wikidump --download liwiki liwiki.model

Import the required modules::

    >>> import re
    >>> from semanticizest import Semanticizer

Load the model from disk::

    >>> sem = Semanticizer('liwiki.model')

Set up a piece of sample text and tokenize it::

    >>> text = """'ne Donjon is 'ne middeleëuwse, zjwaore, verdedigingstaore,
    ... meistal geboewd óp 'ne hoage heuvel, de opperhaof, dae deil oetmaak van 'n
    ... motte."""
    >>> tokens = re.findall('\w+', text)

Feed the tokens to the semanticizer to get the entity link
candidates::

    >>> for cand in sem.all_candidates(tokens):
    ...     print cand
    (7, 8, u'Taore (boewwerk)', 1.0)
    (13, 14, u'Heuvel', 1.0)
    (15, 16, u'Opperhaof', 1.0)
    (21, 22, u'Motte', 1.0)

As we can see, It finds four entity candidates in this short text. The
first entity found is 'Taore (boewwerk)', corresponding to the seventh
token: 'verdedigingstaore'.

Contents
========

.. toctree::
   :maxdepth: 2

   api
   algorithm



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Developed by
============

.. TODO find a better way of displaying these (in the theme?)

.. figure:: _static/logo_uva.png

   `ILPS, University of Amsterdam <http://ilps.science.uva.nl>`_

.. figure:: _static/logo_nlesc.png

   `Netherlands eScience Center <http://esciencecenter.nl>`_
