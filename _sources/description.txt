Semanticizest description
=========================


What's up with the name?
------------------------

Semanticize, semanticizer (previous version), semanticizest (current
(re-)implementation). Yes we're bad at coming up with names.


Usage
-----

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


Algorithms & Implementation Details
-----------------------------------

.. note:: Concepts that need explanation/clarification:

          - link
          - entity
          - concept
          - context
          - anchor
          - sense

Formulas for determining link candidates and ranking candidates. These
two steps correspond exactly to the baseline retrieval model of
[Odijk2013]_.

- *prior probability* determines how likely it is that anchor text 'a'
  links to Wikipedia article 'w', also known as *commonness*, "the
  extent to which each sense is well-known" [Medelyan2008]_.

  .. math::

     P_{prior}(w|a) = \frac{|lnk_{a,w}|}{|lnk_a|}

  here 'w' is a Wikipedia article, 'a' is the anchor text, :math:`|.|`
  is (multi)set cardinality, 'lnk_{a,w}' is the multiset of links with
  anchor text 'a' and target 'w', similarly 'lnk_a' is the multiset of
  links with anchor text 'a'.

- *keyphraseness* "is defined as the number of Wikipedia articles that
  use it as an anchor, divided by the number of articles that mention
  it at all." [Milne2008]_ "[is an] estimate of the probability that a
  phrase is selected as a keyphrase for a document" [Mihalcea2007]_,
  "the probability of being a [link] candidate" [Medelyan2008]_

  .. math::

     P_{keyphrase}(a) = \frac{DF(lnk_a)}{DF(a)}

  where 'a' is the anchor text (an n-gram of one or more terms),
  'DF(.)' denotes the document frequency in Wikipedia, 'DF(lnk_a)'
  is the number of Wikipedia articles where 'a' is used as the anchor
  text of a link and 'DF(a)' the number of Wikipedia articles
  containing the text 'a' at all.

- *link probability* is the same as 'keyphraseness', except that link
  probability uses term frequencies instead of document frequencies
  ("we determine this probability based on all occurrences, also
  including multiple occurrences in an article" [Meij2012]_)

  .. math::

     P_{link}(a) = \frac{|lnk_a|}{|a|}

- *sense probability* "an estimate for the probability that an n-gram
  is used as an anchor linking to Wikipedia article w." [Odijk2013]_

  .. math::

     P_{sense}(w|a) = \frac{|lnk_{a,w}|}{|a|}


.. [Mihalcea2007] Mihalcea, Rada, and Andras Csomai. "Wikify!: linking
                  documents to encyclopedic knowledge." Proceedings of
                  the sixteenth ACM conference on Conference on
                  information and knowledge management. ACM, 2007.
.. [Medelyan2008] Medelyan, Olena, Ian H. Witten, and David
                  Milne. "Topic indexing with Wikipedia." Proceedings
                  of the AAAI WikiAI workshop. 2008.
.. [Milne2008] Milne, David, and Ian H. Witten. "Learning to link with
               wikipedia." Proceedings of the 17th ACM conference on
               Information and knowledge management. ACM, 2008.
.. [Meij2012] Meij, Edgar, Wouter Weerkamp, and Maarten de
              Rijke. "Adding semantics to microblog posts." ACM, 2012.
.. [Odijk2013] Odijk, Daan, Edgar Meij, and Maarten De Rijke. "Feeding
               the second screen: Semantic linking based on
               subtitles." OAIR, 2013.
