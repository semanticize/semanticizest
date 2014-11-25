Algorithms & implementation details
===================================

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

- *Prior probability* determines how likely it is that anchor text :math:`a`
  links to Wikipedia article :math:`w`, also known as *commonness*, "the
  extent to which each sense is well-known" [Medelyan2008]_.

  .. math::

     P_{prior}(w|a) = \frac{|lnk_{a,w}|}{|lnk_a|}

  here :math:`w` is a Wikipedia article, :math:`a` is the anchor text,
  :math:`|.|` is (multi)set cardinality, :math:`lnk_{a,w}` is the multiset of
  links with anchor text :math:`a` and target :math:`w`,
  and :math:`lnk_a` is the multiset of links with anchor text :math:`a`.

- *Keyphraseness* "is defined as the number of Wikipedia articles that
  use it as an anchor, divided by the number of articles that mention
  it at all." [Milne2008]_ "[is an] estimate of the probability that a
  phrase is selected as a keyphrase for a document" [Mihalcea2007]_,
  "the probability of being a [link] candidate" [Medelyan2008]_

  .. math::

     P_{keyphrase}(a) = \frac{DF(lnk_a)}{DF(a)}

  where :math:`a` is the anchor text (an n-gram of one or more terms),
  :math:`DF(.)` denotes the document frequency in Wikipedia, :math:`DF(lnk_a)`
  is the number of Wikipedia articles where :math:`a` is used as the anchor
  text of a link and :math:`DF(a)` the number of Wikipedia articles
  containing the text :math:`a` at all.

- *Link probability* is the same as 'keyphraseness', except that link
  probability uses term frequencies instead of document frequencies
  ("we determine this probability based on all occurrences, also
  including multiple occurrences in an article" [Meij2012]_):

  .. math::

     P_{link}(a) = \frac{|lnk_a|}{|a|}

- *Sense probability* "an estimate for the probability that an n-gram
  is used as an anchor linking to Wikipedia article :math:`w`" [Odijk2013]_:

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
