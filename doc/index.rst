.. semanticizest documentation master file, created by
   sphinx-quickstart on Tue Nov 18 15:37:15 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to semanticizest's documentation!
=========================================

semanticizest (Semanticizer, STandalone) is a library for entity linking.


Quick usage
-----------

.. NOTE::
    Wishful thinking for now... (but it actually works!)

.. code:: bash
    # Read wikipedia dump, create model and store it in a file
    python -m semanticizest.parse_wikidump --download lawiki lawiki.xml.bz2 la.model

.. code:: python

    import re
    from semanticizest import Semanticizer
    from semanticizest._wiki_dump_parser import load_model_from_file

    # Load a stored model from file and initialize a semanticizer
    model = load_model_from_file('la.model')
    sem = Semanticizer(model)

    # Semanticize text to get a list of links
    text = """cogito ergo sum"""
    toks = re.findall('\w+', text)

    for cand in sem.all_candidates(toks):
       print cand

    # A bit of a longer example
    text = """Area 389.434 km² Naxos est maxima Cycladum insula. Insulae orientali sunt litora ardua, in occidentem versus loca planiora patent, a septentrionibus ad meridiem montes granitici insulam transeunt, qui usque ad 1000 metra surgunt; quorum summa cacumina sunt Mons Iovis et Coronus."""
    toks = re.findall('\w+', text)

    for cand in sem.all_candidates(toks):
       print cand

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
