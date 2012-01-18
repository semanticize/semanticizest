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
