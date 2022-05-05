"""Non-comprehensive overview of Kazakh morphology generation that handles vowel & consonant harmonies, using the 2017
Latin script for Kazakh. Supports affix combinations and assumes Kazakh input is valid. Based on the standard Kazakh
dialect (non-city dialect). Information retrieved from Z. Dutton & J. Wagner's "A Grammar of Kazakh". Due to some
unpredictability and/or lack of available data, tense marking was not included. Uses the Pynini library for operations
performed on input strings. Makes use of syntactical tags for input/output, a reference to which is given below.

Reference:
K. Gorman & R. Sproat. 2021. Finite-State Text Processing . Morgan & Claypool.

### Reference Table For Input Tags
| Tag Description                                   | Shorthand input   |
|---------------------------------------------------|-------------------|
| Plural                                            | +PLR              |
| 1person singular possessive                       | +1SING-POSS       |
| 1person plural possessive                         | +1PLR-POSS        |
| 2person singular possessive                       | +2SING-POSS       |
| 2person plural possessive                         | +2PLR-POSS        |
| 3person possessive                                | +3-POSS           |
| Negative                                          | +NEG              |
| Causative                                         | +CAUSE            |
| Passive                                           | +PASS             |
| Accusative                                        | +ACC              |
| Dative                                            | +DAT              |
| Genitive                                          | +GEN              |
| Ablative                                          | +ABL              |
| Locative                                          | +LOC              |
| Instrumental                                      | +INS              |
| Present Participle                                | +PRES-PTCP        |
| Past Participle                                   | +PAST-PTCP        |
"""

import pynini as pn
from pynini.lib import rewrite

# Kazakh alphabet
v = pn.union(
    "a", "o", "u", "y",
    "á", "e", "i", "o", "ó"
)
c = pn.union(
    "ý", "b", "d", "f",
    "g", "ǵ", "h", "ı",
    "j", "k", "l", "m",
    "n", "ń", "p", "q",
    "r", "s", "t", "v",
    "x", "z", "sh", "ch"
)
tag = pn.union(
    "A", "B", "C", "D",
    "E", "F", "G", "H",
    "I", "J", "K", "L",
    "M", "N", "O", "P",
    "Q", "R", "S", "T",
    "U", "V", "W", "X",
    "Y", "Z", "+", "1",
    "2", "3", "-", "^"
)
sigma_star = pn.union(v, c, tag).closure().optimize()

# Vowel classes -> used for vowel harmony
v_front = pn.union(
    "á", "e", "i", "ó", "ú", "[BOS]ı",
    "áı", "eı", "iı", "óı", "úı"
)
v_back = pn.union(
    "a", "o", "u", "y",
    "aı", "oı", "uı", "yı"
)
# Consonant classes -> used for consonant harmony
nasal = pn.union(
    "m", "n", "ń"
)
liquid = pn.union(
    "l", "ı", "ý"
)
vFric = pn.union(
    "z", "j", "v"
)
liquid_vFric = pn.union(
    "z", "j", "v", "r", "l", "ı", "ý"
)
sonorant_vFric = pn.union(
    "v", "ı", "ý", "r",
    "l", "m", "n", "ń",
    "z", "j"
)
voiceless = pn.union(
    # Note: List includes voiced consonants that would be devoiced in syllable-coda positions,
    # notwithstanding voiced consonants almost never appear in word-final positions
    "b", "p", "g", "k",
    "f", "h", "d", "p",
    "q", "s", "t", "x",
    "sh", "ch"
)


'''Rules'''
#
# Plural
plr1 = pn.cdrewrite(pn.cross("+PLR", "ler"), v_front, "", sigma_star).optimize()
plr2 = pn.cdrewrite(pn.cross("+PLR", "lar"), v_back, "", sigma_star).optimize()
plr3 = pn.cdrewrite(pn.cross("+PLR", "der"), v_front + sonorant_vFric, "", sigma_star).optimize()
plr4 = pn.cdrewrite(pn.cross("+PLR", "dar"), v_back + sonorant_vFric, "", sigma_star).optimize()
plr5 = pn.cdrewrite(pn.cross("+PLR", "ter"), v_front + voiceless, "", sigma_star).optimize()
plr6 = pn.cdrewrite(pn.cross("+PLR", "tar"), v_back + voiceless, "", sigma_star).optimize()
plural = plr1 @ plr2 @ plr3 @ plr4 @ plr5 @ plr6

# Possessive
poss1 = pn.cdrewrite(pn.cross("+3-POSS", "si^"), v_front, "+LOC", sigma_star).optimize()
poss2 = pn.cdrewrite(pn.cross("+3-POSS", "sy^"), v_back, "+LOC", sigma_star).optimize()
poss3 = pn.cdrewrite(pn.cross("+3-POSS", "i^"), v_front + c, "+LOC", sigma_star).optimize()
poss4 = pn.cdrewrite(pn.cross("+3-POSS", "y^"), v_back + c, "+LOC", sigma_star).optimize()
poss5 = pn.cdrewrite(pn.cross("+3-POSS", "si^"), v_front, "+ABL", sigma_star).optimize()
poss6 = pn.cdrewrite(pn.cross("+3-POSS", "sy^"), v_back, "+ABL", sigma_star).optimize()
poss7 = pn.cdrewrite(pn.cross("+3-POSS", "i^"), v_front + c, "+ABL", sigma_star).optimize()
poss8 = pn.cdrewrite(pn.cross("+3-POSS", "y^"), v_back + c, "+ABL", sigma_star).optimize()
poss9 = pn.cdrewrite(pn.string_map([
    ("+1SING-POSS", "m^"),
    ("+2SING-POSS", "ń^"),
    ]),
    v, "+DAT",
    sigma_star).optimize()
poss10 = pn.cdrewrite(pn.string_map([
    ("+1PLR-POSS", "miz^"),
    ("+2PLR-POSS", "ńiz^"),
    ("+3-POSS", "si^"),
    ]),
    v_front, "+DAT",
    sigma_star).optimize()
poss11 = pn.cdrewrite(pn.string_map([
    ("+1PLR-POSS", "myz^"),
    ("+2PLR-POSS", "ńyz^"),
    ("+3-POSS", "sy^"),
    ]),
    v_back, "+DAT",
    sigma_star).optimize()
poss12 = pn.cdrewrite(pn.string_map([
    ("+1SING-POSS", "im^"),
    ("+1PLUR-POSS", "imiz^"),
    ("+2SING-POSS", "iń^"),
    ("+2PLR-POSS", "ińiz^"),
    ("+3-POSS", "i^"),
    ]),
    v_front + c, "+DAT",
    sigma_star).optimize()
poss13 = pn.cdrewrite(pn.string_map([
    ("+1SING-POSS", "ym^"),
    ("+1PLR-POSS", "ymyz^"),
    ("+2SING-POSS", "yń^"),
    ("+2PLR-POSS", "yńyz^"),
    ("+3-POSS", "y^"),
    ]),
    v_front + c, "+DAT",
    sigma_star).optimize()
poss14 = pn.cdrewrite(pn.string_map([
    ("+1SING-POSS", "m"),
    ("+2SING-POSS", "ń"),
    ]),
    v, "",
    sigma_star).optimize()
poss15 = pn.cdrewrite(pn.string_map([
    ("+1PLR-POSS", "miz"),
    ("+2PLR-POSS", "ńiz"),
    ("+3-POSS", "si"),
    ]),
    v_front, "",
    sigma_star).optimize()
poss16 = pn.cdrewrite(pn.string_map([
    ("+1PLR-POSS", "myz"),
    ("+2PLR-POSS", "ńyz"),
    ("+3-POSS", "sy"),
    ]),
    v_back, "",
    sigma_star).optimize()
poss17 = pn.cdrewrite(pn.string_map([
    ("+1SING-POSS", "im"),
    ("+1PLR-POSS", "imiz"),
    ("+2SING-POSS", "iń"),
    ("+2PLR-POSS", "ińiz"),
    ("+3-POSS", "i"),
    ]),
    v_front + c, "",
    sigma_star).optimize()
poss18 = pn.cdrewrite(pn.string_map([
    ("+1SING-POSS", "ym"),
    ("+1PLR-POSS", "ymyz"),
    ("+2SING-POSS", "yń"),
    ("+2PLR-POSS", "yńyz"),
    ("+3-POSS", "y"),
    ]),
    v_back + c, "",
    sigma_star).optimize()
poss = poss1 @ poss2 @ poss3 @ poss4 @ poss5 @ poss6 @ poss7 \
       @ poss8 @ poss9 @ poss10 @ poss11 @ poss12 @ poss13 \
       @ poss14 @ poss15 @ poss16 @ poss17 @ poss18

# Negative
neg1 = pn.cdrewrite(pn.cross("ý+NEG", "meý"), v_front | v_front + liquid, "", sigma_star).optimize()
neg2 = pn.cdrewrite(pn.cross("ý+NEG", "maý"), v_back | v_back + liquid, "", sigma_star).optimize()
neg3 = pn.cdrewrite(pn.cross("ý+NEG", "beý"), v_front + nasal | v_front + vFric, "", sigma_star).optimize()
neg4 = pn.cdrewrite(pn.cross("ý+NEG", "baý"), v_back + nasal | v_back + vFric, "", sigma_star).optimize()
neg5 = pn.cdrewrite(pn.cross("ý+NEG", "peý"), v_front + voiceless, "", sigma_star).optimize()
neg6 = pn.cdrewrite(pn.cross("ý+NEG", "paý"), v_back + voiceless, "", sigma_star).optimize()
neg = neg1 @ neg2 @ neg3 @ neg4 @ neg5 @ neg6

# Causative
cause1 = pn.cdrewrite(pn.cross("ý+CAUSE", "tý"), v, "", sigma_star).optimize()
cause2 = pn.cdrewrite(pn.cross("ý+CAUSE", "tirý"), v_front + voiceless, "", sigma_star).optimize()
cause3 = pn.cdrewrite(pn.cross("ý+CAUSE", "tyrý"), v_back + voiceless, "", sigma_star).optimize()
cause4 = pn.cdrewrite(pn.cross("ý+CAUSE", "dirý"), v_front + sigma_star, "", sigma_star).optimize()
cause5 = pn.cdrewrite(pn.cross("ý+CAUSE", "dyrý"), v_back + sigma_star, "", sigma_star). optimize()
cause = cause1 @ cause2 @ cause3 @ cause4 @ cause5

# Passive
pass1 = pn.cdrewrite(pn.cross("ý+PASS", "iný"), v_front + "l", "", sigma_star).optimize()
pass2 = pn.cdrewrite(pn.cross("ý+PASS", "yný"), v_back + "l", "", sigma_star).optimize()
pass3 = pn.cdrewrite(pn.cross("ý+PASS", "ilý"), v_front + sigma_star, "", sigma_star).optimize()
pass4 = pn.cdrewrite(pn.cross("ý+PASS", "ylý"), v_back + sigma_star, "", sigma_star).optimize()
passive = pass1 @ pass2 @ pass3 @ pass4

'''Cases'''
#
# Accusative
acc_poss = pn.cdrewrite(pn.cross("^+ACC", "n"), "", "[EOS]", sigma_star).optimize()
acc1 = pn.cdrewrite(pn.cross("+ACC", "ti"),
                    v_front + voiceless | v_front + sigma_star + voiceless, "", sigma_star).optimize()
acc2 = pn.cdrewrite(pn.cross("+ACC", "ty"),
                    v_back + voiceless | v_back + sigma_star + voiceless, "", sigma_star).optimize()
acc3 = pn.cdrewrite(pn.cross("+ACC", "ni"), v_front, "", sigma_star).optimize()
acc4 = pn.cdrewrite(pn.cross("+ACC", "ny"), v_back, "", sigma_star).optimize()
acc5 = pn.cdrewrite(pn.cross("+ACC", "di"), v_front + sigma_star.closure(), "", sigma_star).optimize()
acc6 = pn.cdrewrite(pn.cross("+ACC", "dy"), v_back + sigma_star.closure(), "", sigma_star).optimize()
acc = acc1 @ acc2 @ acc3 @ acc4 @ acc_poss @ acc5 @ acc6

# Genitive
gen1 = pn.cdrewrite(pn.cross("+GEN", "niń"), v_front | v_front + nasal, "", sigma_star).optimize()
gen2 = pn.cdrewrite(pn.cross("+GEN", "nyń"), v_back | v_back + nasal, "", sigma_star).optimize()
gen3 = pn.cdrewrite(pn.cross("+GEN", "diń"), v_front + liquid_vFric, "", sigma_star).optimize()
gen4 = pn.cdrewrite(pn.cross("+GEN", "dyń"), v_back + liquid_vFric, "", sigma_star).optimize()
gen5 = pn.cdrewrite(pn.cross("+GEN", "tiń"),
                    v_front + voiceless | v_front + sigma_star.closure(), "", sigma_star).optimize()
gen6 = pn.cdrewrite(pn.cross("+GEN", "tyń"),
                    v_back + voiceless | v_front + sigma_star.closure(), "", sigma_star).optimize()
gen = gen1 @ gen2 @ gen3 @ gen4 @ gen5 @ gen6

# Dative
dat1 = pn.cdrewrite(pn.cross("^+DAT", "ne"), v_front, "", sigma_star).optimize()
dat2 = pn.cdrewrite(pn.cross("^+DAT", "na"), v_back, "", sigma_star).optimize()
dat3 = pn.cdrewrite(pn.cross("^+DAT", "e"), v_front + sigma_star, "", sigma_star).optimize()
dat4 = pn.cdrewrite(pn.cross("^+DAT", "a"), v_back + sigma_star, "", sigma_star).optimize()
dat5 = pn.cdrewrite(pn.cross("+DAT", "ge"), v_front | v_front + sonorant_vFric, "", sigma_star).optimize()
dat6 = pn.cdrewrite(pn.cross("+DAT", "ǵa"), v_back | v_back + sonorant_vFric, "", sigma_star).optimize()
dat7 = pn.cdrewrite(pn.cross("+DAT", "ke"), v_front + c, "", sigma_star).optimize()
dat8 = pn.cdrewrite(pn.cross("+DAT", "qa"), v_back + c, "", sigma_star).optimize()
dat = dat1 @ dat2 @ dat3 @ dat4 @ dat5 @ dat6 @ dat7 @ dat8

# Locative
loc1 = pn.cdrewrite(pn.cross("^+LOC", "nde"), v_front, "", sigma_star).optimize()
loc2 = pn.cdrewrite(pn.cross("^+LOC", "nda"), v_back, "", sigma_star).optimize()
loc3 = pn.cdrewrite(pn.cross("+LOC", "te"), v_front + voiceless, "", sigma_star).optimize()
loc4 = pn.cdrewrite(pn.cross("+LOC", "ta"), v_back + voiceless, "", sigma_star).optimize()
loc5 = pn.cdrewrite(pn.cross("+LOC", "de"), v_front | v_front + sigma_star, "", sigma_star).optimize()
loc6 = pn.cdrewrite(pn.cross("+LOC", "da"), v_back | v_back + sigma_star, "", sigma_star).optimize()
loc = loc1 @ loc2 @ loc3 @ loc4 @ loc5 @ loc6

# Ablative
abl1 = pn.cdrewrite(pn.cross("^+ABL", "nen"), v_front, "", sigma_star).optimize()
abl2 = pn.cdrewrite(pn.cross("^+ABL", "nan"), v_back, "", sigma_star).optimize()
abl3 = pn.cdrewrite(pn.cross("+ABL", "den"), v_front | v_front + liquid_vFric, "", sigma_star).optimize()
abl4 = pn.cdrewrite(pn.cross("+ABL", "dan"), v_back | v_back + liquid_vFric, "", sigma_star).optimize()
abl5 = pn.cdrewrite(pn.cross("+ABL", "nen"), v_front + nasal, "", sigma_star).optimize()
abl6 = pn.cdrewrite(pn.cross("+ABL", "nan"), v_back + nasal, "", sigma_star).optimize()
abl7 = pn.cdrewrite(pn.cross("+ABL", "ten"),
                    v_front + voiceless | v_front + sigma_star.closure() + voiceless, "", sigma_star).optimize()
abl8 = pn.cdrewrite(pn.cross("+ABL", "tan"),
                    v_back + voiceless | v_back + sigma_star.closure() + voiceless, "", sigma_star).optimize()
abl = abl1 @ abl2 @ abl3 @ abl4 @ abl5 @ abl6 @ abl7 @ abl8

# Instrumental
ins1 = pn.cdrewrite(pn.cross("+INS", "men"), pn.union(v, nasal, "l", "r"), "", sigma_star).optimize()
ins2 = pn.cdrewrite(pn.cross("+INS", "ben"), pn.union("z", "j"), "", sigma_star).optimize()
ins3 = pn.cdrewrite(pn.cross("+INS", "pen"), voiceless, "", sigma_star).optimize()
ins = ins1 @ ins2 @ ins3

'''Participles'''
#
# Present
pres_ptcp1 = pn.cdrewrite(pn.cross("ý+PRES-PTCP", "ıetin"), v_front, "", sigma_star).optimize()
pres_ptcp2 = pn.cdrewrite(pn.cross("ý+PRES-PTCP", "ıatyn"), v_back, "", sigma_star).optimize()
pres_ptcp3 = pn.cdrewrite(pn.cross("ý+PRES-PTCP", "etin"), v_front + c, "", sigma_star).optimize()
pres_ptcp4 = pn.cdrewrite(pn.cross("ý+PRES-PTCP", "atyn"), v_back + c, "", sigma_star).optimize()
pres_ptcp = pres_ptcp1 @ pres_ptcp2 @ pres_ptcp3 @ pres_ptcp4

# Past
pst_ptcp1 = pn.cdrewrite(pn.cross("ý+PAST-PTCP", "gen"), v_front | v_front + sonorant_vFric, "", sigma_star).optimize()
pst_ptcp2 = pn.cdrewrite(pn.cross("ý+PAST-PTCP", "ǵan"), v_back | v_back + sonorant_vFric, "", sigma_star).optimize()
pst_ptcp3 = pn.cdrewrite(pn.cross("ý+PAST-PTCP", "ken"), v_front + voiceless, "", sigma_star).optimize()
pst_ptcp4 = pn.cdrewrite(pn.cross("ý+PAST-PTCP", "qan"), v_back + voiceless, "", sigma_star).optimize()
pst_ptcp = pst_ptcp1 @ pst_ptcp2 @ pst_ptcp3 @ pst_ptcp4

rules = plural @ poss @ neg @ cause @ passive @ acc @ dat @ gen @ loc @ abl @ ins @ pres_ptcp @ pst_ptcp
morph = pn.closure(sigma_star) @ rules @ pn.closure(sigma_star)
morph.optimize()


def inflect(word: str) -> str:
    return rewrite.top_rewrite(word, morph)
