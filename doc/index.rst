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

Output: 
.. code::
    (0, 2, u'Lorem ipsum', 1.0)
    (3, 4, u'Dolor', 1.0)

.. code:: python
    # A bit of a longer example
    text = """Insulae orientali sunt litora ardua, in occidentem versus loca planiora patent, a septentrionibus ad meridiem montes granitici insulam transeunt."""
    toks = re.findall('\w+', text)

    for cand in sem.all_candidates(toks):
       print cand

Output: 
.. code::
    (0, 1, u'Insulae (Venetia)', 0.07659574468085106)
    (0, 1, u'Insulae (provincia Romana)', 0.13617021276595745)
    (0, 1, u'Insulae (Aristophanes)', 0.1148936170212766)
    (0, 1, u'Insula (urbs) ', 0.11063829787234042)
    (0, 1, u'Socnopaei Insula', 0.1574468085106383)
    (0, 1, u'Insula (Francia)', 0.23404255319148937)
    (0, 1, u'Insula', 0.1702127659574468)
    (1, 2, u'Frisia orientalis', 0.21705426356589147)
    (1, 2, u'Europa Orientalis', 0.20930232558139536)
    (1, 2, u'Imperium Romanum Orientale', 0.17829457364341086)
    (1, 2, u'Africa Orientalis', 0.20155038759689922)
    (1, 2, u'Oriens', 0.1937984496124031)
    (3, 4, u'Litus', 1.0)
    (6, 7, u'Occidens', 1.0)
    (7, 8, u'Versus (musica popularis)', 0.09090909090909091)
    (7, 8, u'Versus', 0.9090909090909091)
    (11, 12, u'A', 1.0)
    (12, 13, u'Septentrio', 1.0)
    (14, 15, u'Meridies', 1.0)
    (15, 16, u'Mons', 0.5842696629213483)
    (15, 16, u'Montes', 0.23595505617977527)
    (15, 16, u'Pyrenaei', 0.1797752808988764)
    (16, 17, u'Granitum (lapis)', 1.0)
    (17, 18, u'Insula', 1.0)


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
