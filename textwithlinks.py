import re

_UNWANTED = re.compile(r"""
  (:?
    # we must catch nested {{}} and {| |}; allow one level of nesting
    \{ [|{] (?: \{ [|{] .*? [|}] \} | .*? )* [|}] \}
  | <math> .*? </math>
  | <ref .*? > .*? </ref>
  | \[\[ [^][:]* : (\[\[.*?\]\]|.)*? \]\]   # media, categories
  | =+ .*? =+                               # headers
  | ''+
  )
""", re.DOTALL | re.MULTILINE | re.VERBOSE)


def clean_text(page):
    """Return the clean-ish running text parts of a page."""
    return re.sub(_UNWANTED, "", page)


_LINK_ANCHORS = re.compile(r"""
    (?:
        \[\[
        (?: [^|]* \|)?     # "target|" in [[target|anchor]]
    |
        \]\]
    )
""", re.DOTALL | re.MULTILINE | re.VERBOSE)


def remove_links(page):
    """Remove links from clean_text output."""
    page = re.sub(r'\]\]\[\[', ' ', page)       # hack hack hack, see test
    return re.sub(_LINK_ANCHORS, '', page)
