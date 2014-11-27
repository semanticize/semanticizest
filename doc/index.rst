.. semanticizest documentation master file, created by
   sphinx-quickstart on Tue Nov 18 15:37:15 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to semanticizest's documentation!
=========================================

semanticizest (Semanticizer, STandalone) is a library for entity linking.


Quick usage
-----------

.. code:: bash
    # Read wikipedia dump, create model and store it in a file
    python -m semanticizest.parse_wikidump --download liwiki liwiki.xml.bz2 liwiki.model

Import the required modules::

    >>> import re
    >>> from semanticizest import Semanticizer
    >>> from semanticizest._wiki_dump_parser import load_model_from_file

Load the model from disk::

    >>> model = load_model_from_file('liwiki.model')
    >>> sem = Semanticizer(model)

Set up a piece of sample text and tokenize it::

    >>> text = """'ne Donjon is 'ne middeleëuwse, zjwaore, verdedigingstaore, meistal geboewd óp 'ne hoage heuvel, de opperhaof, dae deil oetmaak van 'n motte."""
    >>> toks = re.findall('\w+', text)

Feed the tokens to the semanticizer to get the candidates::

    >>> for cand in sem.all_candidates(toks):
    ...     print cand
    (7, 8, u'Taore (boewwerk)', 1.0)
    (13, 14, u'Heuvel', 1.0)
    (15, 16, u'Opperhaof', 1.0)
    (21, 22, u'Motte', 1.0)


Contents
========

.. toctree::
   :maxdepth: 2

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
