"""Outline of Kazakh grapheme-to-phoneme conversion using the 2017 Latin
script for Kazakh. Based on the standard Kazakh dialect (non-city dialect).
Information retrieved from Z. Dutton & J. Wagner's "A Grammar of Kazakh", modeled
after Kyle Gorman's Spanish grapheme-to-phoneme converter.

Reference:
K. Gorman & R. Sproat. 2021. Finite-State Text Processing . Morgan & Claypool.
"""

import pynini as pn
from pynini.lib import rewrite

# Kazakh alphabet
grapheme = pn.union(
    "a", "o", "u", "y", "á", "e", "i", "ó",
    "ú", "ý", "b", "d", "g", "f", "ǵ", "h",
    "ı", "j", "k", "l", "m", "n", "ń", "p",
    "q", "r", "s", "t", "v", "x", "z", "sh", "ch"
)
# Kazakh phoneme inventory
phoneme = pn.union(
    "a", "æ", "b", "d", "e", "f", "g", "ɣ", "h",
    "ɪ", "j", "k", "l", "m", "n", "ŋ", "o", "œ",
    "p", "q", "ɾ", "s", "ʃ", "t", "tɕ", "u", "v",
    "χ", "y", "z", "ʒ", "ɯ", "w", "uw", "yw", "ɣʷ", "ɜʷ"
)

sigma_star = pn.union(grapheme, phoneme).closure().optimize()

# Vowel classes -> used to modify /ý/ for vowel harmony
back_vowel = pn.union("a", "o", "u", "y")
front_vowel = pn.union("á", "e", "i", "ó", "ú")

# g2p rewrite
gp = pn.cdrewrite(pn.string_map([
    ("y", "ɯ"),
    ("á", "æ"),
    ("i", "ɪ"),
    ("ó", "œ"),
    ("ú", "y"),
    ("ǵ", "ɣ"),
    ("ı", "j"),
    ("j", "ʒ"),
    ("ń", "ŋ"),
    ("r", "ɾ"),
    ("x", "χ"),
    ("sh", "ʃ"),
    ("ch", "tɕ")
    ]),
    "", "",
    sigma_star).optimize()

# Other rules (non-comprehensive)
r1 = pn.cdrewrite(pn.cross("ý", "uw"), back_vowel + sigma_star, "", sigma_star).optimize()
r2 = pn.cdrewrite(pn.cross("ý", "yw"), front_vowel + sigma_star, "", sigma_star).optimize()
r3 = pn.cdrewrite(pn.cross("ý", "w"), "[BOS]", "", sigma_star).optimize()
r4 = pn.cdrewrite(pn.cross("q", "qχ"), "[BOS]", "", sigma_star).optimize()
r5 = pn.cdrewrite(pn.cross("o", "ɣʷ"), "[BOS]", "", sigma_star).optimize()
r6 = pn.cdrewrite(pn.cross("œ", "ɜʷ"), "[BOS]", "", sigma_star).optimize()

rules = gp @ r1 @ r2 @ r3 @ r4 @ r5 @ r6
g2p = pn.closure(grapheme) @ rules @ pn.closure(phoneme)
g2p.optimize()


def to_phoneme(word: str) -> str:
    return rewrite.top_rewrite(word, g2p)
