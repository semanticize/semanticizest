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
    Wishful thinking for now...

.. code:: python

    from semanticizest import Semanticizer, store_model, load_model

    # Read wikipedia dump, create model and store it in a file
    model = create_model('lawiki-20140931-pages-articles.xml.bz2')
    store_model(model, 'lawiki-20140931.model')

    # Load a stored model from file and initialize a semanticizer
    semanticizer = Semanticizer(model=load_model('lawiki-20140931.model'))

    # Semanticize text to get a list of links
    text = """Lorem ipsum, sic dolor amet..."""
    links = semanticizer.semanticize(text)


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

